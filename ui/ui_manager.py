from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from camera import CameraManager


class UIManager:
    # UI inicializálása
    def __init__(self, main_window_path="ui/main_window.ui"):
        self.window = QMainWindow()
        loadUi(main_window_path, self.window)

        # UI elemek könnyebb elérése
        self.camera_display = self.window.camera_display
        self.recognized_number_people = self.window.recognized_number_people
        self.start_api_button = self.window.start_api
        self.stop_api_button = self.window.stop_api

        # Alapértelmezett értékek beállítása
        self.camera_display.setText("")
        self.recognized_number_people.setText("0")

        self.camera_manager = CameraManager()

        # Eseménykezelők beállítása
        self.setup_event_handlers()

    # Eseménykezelők beállítása
    def setup_event_handlers(self):
        # Egyelőre csak placeholder funkciók
        self.start_api_button.clicked.connect(self.on_start_api_clicked)
        self.stop_api_button.clicked.connect(self.on_stop_api_clicked)

    # API indítása gomb eseménykezelője
    def on_start_api_clicked(self):
        print("Start API gomb megnyomva")
        # Itt később meghívhatod a tényleges API indító funkciót

    # API leállítása gomb eseménykezelője
    def on_stop_api_clicked(self):
        print("Stop API gomb megnyomva")
        # Itt később meghívhatod a tényleges API leállító funkciót

    # Kamera képének frissítése
    def update_camera_display(self, image):
        scaled_image = image.scaled(
            self.camera_display.width(),
            self.camera_display.height(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
        )

        # Konvertálás QPixmap-pá és megjelenítés
        pixmap = QPixmap.fromImage(scaled_image)
        self.camera_display.setPixmap(pixmap)

    # Felismert emberek számának frissítése
    def update_people_count(self, count):
        self.recognized_number_people.setText(str(count))

    # Ablak megjelenítése
    def show(self):
        self.window.show()

    # Kamera leállítása bezáráskor
    def close_event(self, event):

        self.camera_manager.stop()
        event.accept()
