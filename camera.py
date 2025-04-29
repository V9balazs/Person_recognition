import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap


class CameraThread(QThread):
    """Külön szálban futó kamera kezelő osztály"""

    update_frame = pyqtSignal(QImage)

    def __init__(self, camera_id=0):
        super().__init__()
        self.camera_id = camera_id
        self.running = False

    def run(self):
        """Kamera képkockák folyamatos olvasása"""
        self.running = True
        cap = cv2.VideoCapture(self.camera_id)

        if not cap.isOpened():
            print("Hiba: A kamera nem nyitható meg")
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            # OpenCV BGR -> RGB konverzió
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Konvertálás QImage-be
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            # Jelzés küldése a frissített képkockával
            self.update_frame.emit(qt_image)

            # Kis késleltetés a CPU terhelés csökkentésére
            self.msleep(30)  # ~33 FPS

        cap.release()

    def stop(self):
        """Kamera leállítása"""
        self.running = False
        self.wait()


class CameraManager:
    """Kamera kezelő osztály"""

    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.camera_thread = None

    def start(self, frame_update_callback):
        """
        Kamera indítása

        Args:
            frame_update_callback: Függvény, amely meghívódik új képkocka esetén
        """
        if self.camera_thread is None or not self.camera_thread.running:
            self.camera_thread = CameraThread(self.camera_id)
            self.camera_thread.update_frame.connect(frame_update_callback)
            self.camera_thread.start()
            return True
        return False

    def stop(self):
        """Kamera leállítása"""
        if self.camera_thread and self.camera_thread.running:
            self.camera_thread.stop()
            return True
        return False
