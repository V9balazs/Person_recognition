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
        self.camera_display.setText("Kamera nem aktív")
        self.recognized_number_people.setText("0")

        self.camera_manager = CameraManager()

        self.is_camera_running = False

        self.update_button_states()

        # Eseménykezelők beállítása
        self.setup_event_handlers()

    # Eseménykezelők beállítása
    def setup_event_handlers(self):
        self.start_api_button.clicked.connect(self.on_start_api_clicked)
        self.stop_api_button.clicked.connect(self.on_stop_api_clicked)

    # API indítása gomb eseménykezelője
    def on_start_api_clicked(self):
        if not self.is_camera_running:
            # Kamera indítása
            success = self.camera_manager.start(
                frame_update_callback=self.update_camera_display, error_callback=self.handle_camera_error
            )

            if success:
                self.is_camera_running = True
                print("Kamera sikeresen elindítva")

                # Status bar frissítése (ha van)
                if hasattr(self.window, "statusBar"):
                    self.window.statusBar().showMessage("Kamera aktív - Felismerés folyamatban...")

                # Gomb állapotok frissítése
                self.update_button_states()

                # Emberek számának nullázása új session kezdetekor
                self.update_people_count(0)
            else:
                print("Hiba: A kamera nem indítható el")
                self.handle_camera_error("A kamera nem indítható el")
        else:
            print("A kamera már fut")

    # API leállítása gomb eseménykezelője
    def on_stop_api_clicked(self):
        print("Stop API gomb megnyomva")

        if self.is_camera_running:
            # Kamera leállítása
            success = self.camera_manager.stop()

            if success:
                self.is_camera_running = False
                print("Kamera sikeresen leállítva")

                # Kamera display tisztítása
                self.camera_display.clear()
                self.camera_display.setText("Kamera leállítva")

                # Status bar frissítése
                if hasattr(self.window, "statusBar"):
                    self.window.statusBar().showMessage("Kamera leállítva")

                # Gomb állapotok frissítése
                self.update_button_states()

                # Emberek számának nullázása
                self.update_people_count(0)
            else:
                print("Hiba: A kamera nem állítható le")

                # Status bar frissítése hiba esetén
                if hasattr(self.window, "statusBar"):
                    self.window.statusBar().showMessage("Hiba: A kamera nem állítható le", 3000)
        else:
            print("A kamera már le van állítva")

    def handle_camera_error(self, error_message):
        """Kamera hibák kezelése"""
        print(f"Kamera hiba: {error_message}")

        # UI visszaállítása hiba esetén
        self.is_camera_running = False
        self.camera_display.clear()
        self.camera_display.setText(f"Kamera hiba:\n{error_message}")

        # Status bar frissítése
        if hasattr(self.window, "statusBar"):
            self.window.statusBar().showMessage(f"Kamera hiba: {error_message}", 5000)

        # Gomb állapotok frissítése
        self.update_button_states()

    def update_button_states(self):
        # Gomb állapotok frissítése a kamera állapota alapján
        if self.is_camera_running:
            # Kamera fut: Start gomb letiltása, Stop gomb engedélyezése
            self.start_api_button.setEnabled(False)
            self.start_api_button.setText("Futó...")
            self.stop_api_button.setEnabled(True)
            self.stop_api_button.setText("Stop API")
        else:
            # Kamera nem fut: Start gomb engedélyezése, Stop gomb letiltása
            self.start_api_button.setEnabled(True)
            self.start_api_button.setText("Start API")
            self.stop_api_button.setEnabled(False)
            self.stop_api_button.setText("Leállítva")

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
