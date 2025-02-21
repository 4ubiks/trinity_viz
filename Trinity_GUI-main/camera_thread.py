import cv2
from threading import Thread
from PySide6.QtCore import QObject, Signal
import numpy as np

class CameraThread(QObject):
    frame_ready = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = None
        self.running = False

    def start_camera(self, url):
        if not self.running:
            self.cap = cv2.VideoCapture(url)
            self.running = True
            Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_ready.emit(frame)

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
