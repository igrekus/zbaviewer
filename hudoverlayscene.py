from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF


class HudOverlayScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(HudOverlayScene, self).__init__(parent)

    def mouseMoveEvent(self, event):
        # super(HudOverlayScene, self).mouseMoveEvent(event)
        self.items()[-1].mouseMoveEvent(event)

