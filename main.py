import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from ui.ui_manager import UIManager


def main():
    # High DPI támogatás
    # QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # UI Manager létrehozása és megjelenítése
    ui_manager = UIManager()
    ui_manager.show()

    # Ablak bezárási esemény kezelése
    ui_manager.window.closeEvent = ui_manager.close_event

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
