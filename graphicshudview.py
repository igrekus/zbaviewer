from hudlegend import HudLegend
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPointF

class GraphicsHudView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsHudView, self).__init__(parent)

        self.hudOverlayScene = QGraphicsScene(self)

        self.hudLegend = HudLegend()

        self.mousePos = QPointF()

        self.hudOverlayScene.addItem(self.hudLegend)

    def paintEvent(self, event):
        super(GraphicsHudView, self).paintEvent(event)
        if self.hudOverlayScene is not None:
            self.paintOverlay()

    def paintOverlay(self):
        p = QPainter(self.viewport())
        # p.setRenderHints(self.renderHints())
        self.hudOverlayScene.render(p)

    def mousePressEvent(self, event):
        self.mousePos = event.pos()
        super(GraphicsHudView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # print("view mouse move event")
        super(GraphicsHudView, self).mouseMoveEvent(event)
