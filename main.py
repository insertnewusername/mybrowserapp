import sys
from PyQt5.QtWidgets import QApplication
from browser_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Group Browser")
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()