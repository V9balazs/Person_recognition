import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap


class CameraThread(QThread):
    """Külön szálban futó kamera kezelő osztály"""

    update_frame = pyqtSignal(QImage)
    error_occurred = pyqtSignal(str)

    def __init__(self, camera_id=0):
        super().__init__()
        self.camera_id = camera_id
        self.running = False
        self.cap = None

    def run(self):
        """Kamera képkockák folyamatos olvasása"""
        self.running = True
        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():
            self.error_occurred.emit(f"Hiba: A kamera (index: {self.camera_id}) nem nyitható meg")
            return

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self.error_occurred.emit("Hiba: Nem sikerült képkockát olvasni a kamerából")
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
            self.msleep(33)  # ~30 FPS

        self.cleanup()

    def cleanup(self):
        """Erőforrások felszabadítása"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("Kamera erőforrások felszabadítva")

    def stop(self):
        """Kamera leállítása"""
        self.running = False
        self.wait()


class CameraManager:
    """Kamera kezelő osztály"""

    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.camera_thread = None
        self.available_cameras = self.detect_cameras()

    def detect_cameras(self):
        """Elérhető kamerák detektálása"""
        available_cameras = []

        # Próbáljuk meg az első 5 kamera indexet
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()

        print(f"Elérhető kamerák: {available_cameras}")
        return available_cameras

    def start(self, frame_update_callback, error_callback=None):
        # Ellenőrizzük, hogy van-e elérhető kamera
        if not self.available_cameras:
            error_msg = "Hiba: Nem található elérhető kamera"
            print(error_msg)
            if error_callback:
                error_callback(error_msg)
            return False

        # Ha a megadott kamera index nem elérhető, használjuk az első elérhetőt
        if self.camera_id not in self.available_cameras:
            self.camera_id = self.available_cameras[0]
            print(f"A megadott kamera index nem elérhető, használjuk a {self.camera_id}-s indexűt")

        if self.camera_thread is None or not self.camera_thread.running:
            self.camera_thread = CameraThread(self.camera_id)
            self.camera_thread.update_frame.connect(frame_update_callback)

            if error_callback:
                self.camera_thread.error_occurred.connect(error_callback)

            self.camera_thread.start()
            return True
        return False

    def stop(self):
        """Kamera leállítása"""
        if self.camera_thread and self.camera_thread.running:
            self.camera_thread.stop()
            return True
        return False

    def get_available_cameras(self):
        """Elérhető kamerák listájának visszaadása"""
        return self.available_cameras
