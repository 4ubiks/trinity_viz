from PySide6.QtCore import QObject, Signal, Property

class RotationHandler(QObject):
    rotationChanged = Signal()

    def __init__(self):
        super().__init__()
        self._rotationX = 0
        self._rotationY = 0
        self._rotationZ = 0

    @Property(float, notify=rotationChanged)
    def rotationX(self):
        return self._rotationX

    @rotationX.setter
    def rotationX(self, value):
        if self._rotationX != value:
            self._rotationX = value
            self.rotationChanged.emit()

    @Property(float, notify=rotationChanged)
    def rotationY(self):
        return self._rotationY

    @rotationY.setter
    def rotationY(self, value):
        if self._rotationY != value:
            self._rotationY = value
            self.rotationChanged.emit()

    @Property(float, notify=rotationChanged)
    def rotationZ(self):
        return self._rotationZ

    @rotationZ.setter
    def rotationZ(self, value):
        if self._rotationZ != value:
            self._rotationZ = value
            self.rotationChanged.emit()
