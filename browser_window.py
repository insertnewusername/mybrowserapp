import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from group_manager import GroupManager, DEFAULT_URL
from styles import STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyBrowser")
        self.setStyleSheet(STYLE)

        self.manager = GroupManager()
        self._loading_group = False
        self._browsers = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        navbar = QToolBar()
        navbar.setObjectName("navbar")
        navbar.setMovable(False)
        navbar.setIconSize(QSize(16, 16))
        self.addToolBar(navbar)

        def make_action(label, slot, shortcut=None):
            act = QAction(label, self)
            act.triggered.connect(slot)
            if shortcut:
                act.setShortcut(shortcut)
            navbar.addAction(act)
            return act

        make_action("Back", lambda: self.current_browser().back())
        make_action("Forward", lambda: self.current_browser().forward())
        make_action("Reload", lambda: self.current_browser().reload())
        navbar.addSeparator()
        make_action("New Tab", self.add_tab, "Ctrl+T")

        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("urlBar")
        self.url_bar.setPlaceholderText("Search or enter address")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tabWidget")
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        layout.addWidget(self.tab_widget)

        # -------------------- GROUPS OVERLAY (left rail) --------------------
        self.sidebar_collapsed_width = 44
        self.sidebar_expanded_width = 260
        self.target_width = self.sidebar_collapsed_width

        self.sidebar = QWidget(central)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(self.sidebar_collapsed_width)
        self.sidebar.raise_()

        shadow = QGraphicsDropShadowEffect(self.sidebar)
        shadow.setBlurRadius(24)
        shadow.setOffset(4, 0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.sidebar.setGraphicsEffect(shadow)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 12, 8, 12)
        sidebar_layout.setSpacing(8)

        self.groups_label = QLabel("Groups")
        self.groups_label.setObjectName("sidebarTitle")
        sidebar_layout.addWidget(self.groups_label)

        self.rail_hint = QLabel("G")
        self.rail_hint.setObjectName("sidebarRailHint")
        self.rail_hint.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.rail_hint)

        self.group_list = QListWidget()
        self.group_list.setObjectName("groupList")
        self.group_list.itemClicked.connect(self.on_group_selected)
        self.group_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.group_list.customContextMenuRequested.connect(self.show_group_context_menu)
        sidebar_layout.addWidget(self.group_list)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)
        self.add_btn = QPushButton("New")
        self.add_btn.setObjectName("sidebarButton")
        self.add_btn.setToolTip("New Group")
        self.add_btn.clicked.connect(self.add_group)
        self.del_btn = QPushButton("Delete")
        self.del_btn.setObjectName("sidebarButton")
        self.del_btn.setToolTip("Delete Group")
        self.del_btn.clicked.connect(self.delete_group)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)
        sidebar_layout.addLayout(btn_layout)

        self.sidebar.installEventFilter(self)
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.animate_sidebar)
        self.anim_step = 12

        self.populate_group_list()
        self.load_group(self.manager.current_group)
        self.update_sidebar_geometry()
        self.update_sidebar_visibility()

        self.showMaximized()

    # -------------------- SIDEBAR OVERLAY --------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_sidebar_geometry()

    def update_sidebar_geometry(self):
        central = self.centralWidget()
        if not central or not hasattr(self, "sidebar"):
            return
        self.sidebar.setGeometry(0, 0, self.sidebar.width(), central.height())
        self.sidebar.raise_()

    def update_sidebar_visibility(self):
        expanded = self.sidebar.width() > self.sidebar_collapsed_width + 20
        self.groups_label.setVisible(expanded)
        self.group_list.setVisible(expanded)
        self.add_btn.setVisible(expanded)
        self.del_btn.setVisible(expanded)
        self.rail_hint.setVisible(not expanded)

    def eventFilter(self, obj, event):
        if obj == self.sidebar:
            if event.type() == QEvent.Enter:
                self.target_width = self.sidebar_expanded_width
                if not self.anim_timer.isActive():
                    self.anim_timer.start(10)
            elif event.type() == QEvent.Leave:
                self.target_width = self.sidebar_collapsed_width
                if not self.anim_timer.isActive():
                    self.anim_timer.start(10)
        return super().eventFilter(obj, event)

    def animate_sidebar(self):
        current = self.sidebar.width()
        diff = self.target_width - current
        if abs(diff) <= self.anim_step:
            self.sidebar.setFixedWidth(self.target_width)
            self.anim_timer.stop()
        else:
            step = self.anim_step if diff > 0 else -self.anim_step
            self.sidebar.setFixedWidth(current + step)
        self.update_sidebar_geometry()
        self.update_sidebar_visibility()

    # -------------------- GROUP UI --------------------
    def populate_group_list(self):
        self.group_list.blockSignals(True)
        self.group_list.clear()
        for name in self.manager.group_names():
            count = len(self.manager.get_urls(name))
            item = QListWidgetItem(f"{name}  ({count})")
            item.setData(Qt.UserRole, name)
            self.group_list.addItem(item)

        for i in range(self.group_list.count()):
            if self.group_list.item(i).data(Qt.UserRole) == self.manager.current_group:
                self.group_list.setCurrentRow(i)
                break
        self.group_list.blockSignals(False)

    def add_group(self):
        name, ok = QInputDialog.getText(self, "New Group", "Enter group name:")
        if ok and name.strip():
            self.save_current_tabs()
            if self.manager.add_group(name.strip()):
                self.populate_group_list()
                self.load_group(name.strip())
            else:
                QMessageBox.warning(self, "Error", "Group already exists.")

    def delete_group(self):
        if len(self.manager.group_names()) <= 1:
            QMessageBox.warning(self, "Error", "Cannot delete the last group.")
            return
        current = self.group_list.currentItem()
        if not current:
            return
        group_name = current.data(Qt.UserRole)
        reply = QMessageBox.question(
            self,
            "Delete Group",
            f"Delete group '{group_name}' and all its tabs?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.save_current_tabs()
            if self.manager.delete_group(group_name):
                self.populate_group_list()
                self.load_group(self.manager.current_group)

    def rename_group(self):
        current = self.group_list.currentItem()
        if not current:
            return
        old_name = current.data(Qt.UserRole)
        new_name, ok = QInputDialog.getText(
            self, "Rename Group", "New name:", text=old_name
        )
        if ok and new_name.strip() and new_name != old_name:
            self.save_current_tabs()
            if self.manager.rename_group(old_name, new_name.strip()):
                self.populate_group_list()
            else:
                QMessageBox.warning(self, "Error", "Name already exists or invalid.")

    def show_group_context_menu(self, pos):
        menu = QMenu(self)
        rename_act = QAction("Rename Group", self)
        rename_act.triggered.connect(self.rename_group)
        menu.addAction(rename_act)
        menu.exec_(self.group_list.mapToGlobal(pos))

    def on_group_selected(self, item):
        group_name = item.data(Qt.UserRole)
        if group_name != self.manager.current_group:
            self.save_current_tabs()
            self.manager.current_group = group_name
            self.manager.save()
            self.load_group(group_name)

    # -------------------- LOAD / SAVE TABS --------------------
    def clear_all_tabs(self):
        self.tab_widget.blockSignals(True)
        while self.tab_widget.count() > 0:
            widget = self.tab_widget.widget(0)
            self.tab_widget.removeTab(0)
            if widget:
                widget.deleteLater()
        self.tab_widget.blockSignals(False)
        self._browsers.clear()

    def load_group(self, group_name):
        self._loading_group = True
        try:
            self.clear_all_tabs()
            urls = self.manager.get_urls(group_name)
            for url in urls:
                self.add_tab_to_widget(url, activate=False)
            if self.tab_widget.count() > 0:
                self.tab_widget.setCurrentIndex(0)
                browser = self.tab_widget.currentWidget()
                if browser:
                    self.url_bar.setText(browser.url().toString())
        finally:
            self._loading_group = False

        self.populate_group_list()

    def save_current_tabs(self):
        if self._loading_group:
            return
        urls = []
        for i in range(self.tab_widget.count()):
            browser = self.tab_widget.widget(i)
            if browser:
                urls.append(browser.url().toString())
        if self.manager.current_group in self.manager.groups:
            self.manager.set_urls(self.manager.current_group, urls)

    def add_tab_to_widget(self, url, activate=True):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.urlChanged.connect(self.on_browser_url_changed)
        browser.titleChanged.connect(
            lambda title, b=browser: self.on_browser_title_changed(b, title)
        )
        self._browsers.append(browser)

        title = self.get_tab_title(url)
        idx = self.tab_widget.addTab(browser, title)
        if activate:
            self.tab_widget.setCurrentIndex(idx)
        return browser

    def get_tab_title(self, url):
        qurl = QUrl(url)
        host = qurl.host().lower()
        if host in ("www.google.com", "google.com"):
            return "Google"
        if host:
            return host.removeprefix("www.")
        return "New Tab"

    def browser_index(self, browser):
        for i in range(self.tab_widget.count()):
            if self.tab_widget.widget(i) is browser:
                return i
        return -1

    def on_browser_url_changed(self, qurl):
        if self._loading_group:
            return
        idx = self.tab_widget.currentIndex()
        browser = self.tab_widget.currentWidget()
        if browser and browser.url() == qurl:
            self.url_bar.setText(qurl.toString())
            self.tab_widget.setTabText(idx, self.get_tab_title(qurl.toString()))
        self.save_current_tabs()

    def on_browser_title_changed(self, browser, title):
        if self._loading_group or not title:
            return
        idx = self.browser_index(browser)
        if idx >= 0:
            self.tab_widget.setTabText(idx, title[:28])

    # -------------------- TAB OPERATIONS --------------------
    def add_tab(self):
        self.add_tab_to_widget(DEFAULT_URL)
        self.save_current_tabs()
        self.populate_group_list()

    def close_tab(self, index):
        if self.tab_widget.count() == 1:
            browser = self.tab_widget.widget(index)
            if browser:
                browser.setUrl(QUrl(DEFAULT_URL))
            self.save_current_tabs()
            return

        widget = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        if widget:
            if widget in self._browsers:
                self._browsers.remove(widget)
            widget.deleteLater()
        self.save_current_tabs()
        self.populate_group_list()

    def on_tab_changed(self, index):
        if index >= 0 and not self._loading_group:
            browser = self.tab_widget.widget(index)
            if browser:
                self.url_bar.setText(browser.url().toString())

    def current_browser(self):
        if self.tab_widget.count() == 0:
            self.add_tab()
        return self.tab_widget.currentWidget()

    # -------------------- NAVIGATION --------------------
    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        if " " in text and "." not in text:
            text = "https://www.google.com/search?q=" + text.replace(" ", "+")
        elif not text.startswith(("http://", "https://")):
            if "." in text:
                text = "https://" + text
            else:
                text = "https://www.google.com/search?q=" + text.replace(" ", "+")
        browser = self.current_browser()
        if browser:
            browser.setUrl(QUrl(text))

    def closeEvent(self, event):
        self.save_current_tabs()
        self.manager.save()
        event.accept()
