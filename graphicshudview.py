import random
from hudlegenditem import HudLegendItem
from hudoverlayscene import HudOverlayScene
from PyQt5.QtWidgets import QGraphicsView, QGraphicsLineItem
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF


class GraphicsHudView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsHudView, self).__init__(parent)

        self.setInteractive(True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.hudOverlayScene = HudOverlayScene(self)
        self.hudLegendItem = HudLegendItem(zoom=50, rect=QRectF(self.frameGeometry()))
        self.hudOverlayScene.addItem(self.hudLegendItem)

        self.mousePos = QPointF()
        self.setMouseTracking(True)

        self.rulerP1 = QPointF(0, 0)
        self.rulerP2 = QPointF(0, 0)
        self.rulerItem = QGraphicsLineItem()

        self.hasRuler = False
        self.isDrawingRuler = False
        self.isDragging = False

    def initView(self):
        self.scene().addItem(self.rulerItem)
        self.rulerItem.setVisible(False)

    def paintEvent(self, event):
        super(GraphicsHudView, self).paintEvent(event)
        # if self.hudOverlayScene is not None:
        self.paintOverlay()

    def paintOverlay(self):
        p = QPainter(self.viewport())
        p.setRenderHints(self.renderHints())
        self.hudOverlayScene.render(p)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if not self.hasRuler:
                pos = self.mapToScene(event.pos())
                self.scene().addItem(self.rulerItem)
                # self.rulerItem.setVisible(True)
                self.rulerItem.setLine(0, 0, 0, 0)
                self.rulerItem.setPos(pos.x(), pos.y())
                self.rulerP1 = pos
                self.isDrawingRuler = True
            else:
                # self.rulerItem.setVisible(False)
                self.scene().removeItem(self.rulerItem)
                self.hasRuler = False
        # elif event.buttons() == Qt.RightButton:
        #     self.isDragging = True

        super(GraphicsHudView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.isDrawingRuler:
                self.isDrawingRuler = False
                self.hasRuler = True
        # elif event.button() == Qt.RightButton:
        #     self.isDragging = False

        super(GraphicsHudView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        # print("mouse move", "ruler?", self.hasRuler, "drawing?", self.isDrawingRuler)
        self.hudOverlayScene.mouseMoveEvent(event)
        # TODO update only mouse-tracking stuff
        self.viewport().update()
        # self.scene().update()

        if self.isDrawingRuler and (event.buttons() & Qt.LeftButton):
            pos = self.mapToScene(event.pos())
            line = self.rulerItem.line()
            line.setP2(self.rulerItem.mapFromScene(pos))
            self.rulerItem.setLine(line)
            self.rulerP2 = pos

        if self.isDragging:
            pass

        super(GraphicsHudView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        from PyQt5.QtWidgets import QGraphicsScene
        # print("mouse wheel event")
        super().wheelEvent(event)

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
