from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPainter

class GraphicsHudView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsHudView, self).__init__(parent)

        self.hudOverlayScene = QGraphicsScene(self)

        text = QGraphicsTextItem("HUD OVERLAY TEXT")
        text.setScale(2)
        text.setFlag(QGraphicsTextItem.ItemIgnoresTransformations)
        self.hudOverlayScene.addItem(text)
        self.hudOverlayScene.addRect(0, 0, 100, 100)

    def paintEvent(self, event):
        super(GraphicsHudView, self).paintEvent(event)
        if self.hudOverlayScene is not None:
            self.paintOverlay()

    def paintOverlay(self):
        p = QPainter(self.viewport())
        p.setRenderHints(self.renderHints())
        self.hudOverlayScene.render(p)

