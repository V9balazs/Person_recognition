import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.uic import loadUi


def main():
    app = QApplication(sys.argv)
    window = loadUi("ui/main_window.ui")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
