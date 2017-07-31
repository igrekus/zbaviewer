import random
from hudlegenditem import HudLegendItem
from hudoverlayscene import HudOverlayScene
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPointF, QRectF, Qt


class GraphicsHudView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsHudView, self).__init__(parent)

        self.hudOverlayScene = HudOverlayScene(self)
        self.hudLegendItem = HudLegendItem(zoom=50, rect=QRectF(self.frameGeometry()))
        self.hudOverlayScene.addItem(self.hudLegendItem)

        self.mousePos = QPointF()
        self.setMouseTracking(True)

    def paintEvent(self, event):
        super(GraphicsHudView, self).paintEvent(event)
        # if self.hudOverlayScene is not None:
        self.paintOverlay()

    def paintOverlay(self):
        p = QPainter(self.viewport())
        p.setRenderHints(self.renderHints())
        self.hudOverlayScene.render(p)

    def mousePressEvent(self, event):
        # print("view mouse press event")
        super(GraphicsHudView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # print("view mouse move event:", event.pos())
        # self.mousePos = event.pos()
        self.hudOverlayScene.mouseMoveEvent(event)
        super(GraphicsHudView, self).mouseMoveEvent(event)
        # TODO update only mouse-tracking stuff
        self.viewport().update()
        # self.scene().update()

    def keyPressEvent(self, event):
        key = event.key()
        # if key in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Right, Qt.Key_Left):
        if key == Qt.Key_Up:
            self.scene().setSceneRect(self.scene().sceneRect().adjusted(0, +10, 0, 0))
        elif key == Qt.Key_Down:
            self.scene().setSceneRect(self.scene().sceneRect().adjusted(0, -10, 0, 0))
        elif key == Qt.Key_Left:
            self.scene().setSceneRect(self.scene().sceneRect().adjusted(+10, 0, 0, 0))
        elif key == Qt.Key_Right:
            self.scene().setSceneRect(self.scene().sceneRect().adjusted(-10, 0, 0, 0))

            # self.translate(0, 10)
            # self.scene().addRect(random.randint(0, 200), -random.randint(0, 200), 10, 10)
        super(GraphicsHudView, self).keyPressEvent(event)

