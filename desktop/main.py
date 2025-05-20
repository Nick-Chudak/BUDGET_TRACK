import sys
from PyQt6.QtWidgets import QApplication
from desktop.ui.dashboard import DashboardWindow

def main():
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()