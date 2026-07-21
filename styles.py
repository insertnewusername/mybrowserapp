STYLE = """
QMainWindow {
    background-color: #eef1f5;
}

QWidget#sidebar {
    background: #1e2430;
    border-right: 1px solid #141820;
}

QLabel#sidebarRailHint {
    color: #8b95a8;
    font-size: 18px;
    font-weight: 700;
    padding: 8px 0;
}

QLabel#sidebarTitle {
    color: #8b95a8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    padding: 0 4px 4px 4px;
}

QListWidget#groupList {
    background: transparent;
    border: none;
    outline: none;
    color: #d7dce5;
    font-size: 13px;
}

QListWidget#groupList::item {
    padding: 10px 12px;
    border-radius: 8px;
    margin: 2px 0;
}

QListWidget#groupList::item:selected {
    background: #2f6fed;
    color: #ffffff;
}

QListWidget#groupList::item:hover:!selected {
    background: #2a3140;
}

QPushButton#sidebarButton {
    background: #2a3140;
    border: 1px solid #3a4356;
    border-radius: 8px;
    color: #d7dce5;
    font-size: 12px;
    font-weight: 600;
    padding: 8px 10px;
}

QPushButton#sidebarButton:hover {
    background: #343d50;
    border-color: #4a556d;
}

QPushButton#sidebarButton:pressed {
    background: #252b38;
}

QToolBar#navbar {
    background: #ffffff;
    border: none;
    border-bottom: 1px solid #d8dee8;
    padding: 8px 12px;
    spacing: 6px;
}

QToolBar#navbar QToolButton {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    color: #3c4454;
    font-size: 13px;
    font-weight: 600;
    padding: 7px 12px;
}

QToolBar#navbar QToolButton:hover {
    background: #f1f4f8;
    border-color: #d8dee8;
}

QToolBar#navbar QToolButton:pressed {
    background: #e7ebf2;
}

QToolBar#navbar::separator {
    background: #d8dee8;
    width: 1px;
    margin: 4px 8px;
}

QLineEdit#urlBar {
    background: #f5f7fa;
    border: 1px solid #d8dee8;
    border-radius: 18px;
    color: #1f2937;
    font-size: 14px;
    min-height: 18px;
    padding: 8px 16px;
    selection-background-color: #2f6fed;
}

QLineEdit#urlBar:focus {
    background: #ffffff;
    border-color: #2f6fed;
}

QTabWidget#tabWidget::pane {
    border: none;
    background: #ffffff;
    top: -1px;
}

QTabWidget#tabWidget QTabBar {
    background: #f5f7fa;
    border-bottom: 1px solid #d8dee8;
}

QTabWidget#tabWidget QTabBar::tab {
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: #5c667a;
    font-size: 12px;
    font-weight: 600;
    margin: 0;
    min-width: 120px;
    padding: 10px 18px;
}

QTabWidget#tabWidget QTabBar::tab:selected {
    background: #ffffff;
    border-bottom: 2px solid #2f6fed;
    color: #1f2937;
}

QTabWidget#tabWidget QTabBar::tab:hover:!selected {
    background: #eef1f5;
    color: #3c4454;
}

QTabWidget#tabWidget QTabBar::close-button {
    image: none;
    subcontrol-position: right;
}

QTabWidget#tabWidget QTabBar::close-button:hover {
    background: #e7ebf2;
    border-radius: 4px;
}

QMenu {
    background: #ffffff;
    border: 1px solid #d8dee8;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    border-radius: 6px;
    color: #1f2937;
    padding: 8px 24px 8px 16px;
}

QMenu::item:selected {
    background: #eef3ff;
    color: #2f6fed;
}

QInputDialog, QMessageBox {
    background: #ffffff;
}

QScrollBar:vertical {
    background: transparent;
    border: none;
    margin: 0;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #c5ccd8;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #aab3c2;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""
