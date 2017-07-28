from hudlegend import HudLegend
from zbarect import ZbaRect
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt, QRectF


# TODO record commentaries from other users
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("mainwindow.ui", self)

        # scene
        self.scene = QGraphicsScene(self)
        # origin
        self.originRect = QGraphicsRectItem(0, 0, 4, 4)
        self.originRect.setPos(-2, -2)
        self.scene.addItem(self.originRect)

    def initApp(self):
        self.ui.graphicsHudView.setScene(self.scene)

        self.ui.graphicsHudView.verticalScrollBar().valueChanged.connect(self.onHudViewScroll)
        # self.ui.graphicsHudView.verticalScrollBar().sliderMoved.connect(self.onHudViewScroll)
        self.ui.graphicsHudView.horizontalScrollBar().valueChanged.connect(self.onHudViewScroll)

    def resizeEvent(self, event):
        self.ui.graphicsHudView.resize(self.ui.graphicsHudView.size())
        # self.ui.graphicsHudView.fitInView(self.ui.graphicsHudView.frameRect(), Qt.KeepAspectRatio)
        super(MainWindow, self).resizeEvent(event)

    def onHudViewScroll(self, int):
        self.ui.graphicsHudView.hudOverlayScene.items()[0].update(0, 0, 50, 50)
        # self.ui.graphicsHudView.hudOverlayScene.update()

    def decodeRect(self, rect: ZbaRect, scale):
        return rect.pos[0]*scale, rect.pos[1]*scale, rect.size[0]*scale, rect.size[1]*scale

    def drawRects(self, rect_list):
        for r in rect_list:
            x, y, lx, ly = self.decodeRect(r, 50)
            rect = QGraphicsRectItem(0, 0, lx, ly)
            rect.setBrush(QBrush(QColor(Qt.gray)))
            self.scene.addItem(rect)
            rect.setPos(x, y)
        pass


