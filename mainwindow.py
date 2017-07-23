from zbarect import ZbaRect
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


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

    def initApp(self):
        self.ui.graphicsView.setScene(self.scene)

        txt = QGraphicsTextItem("Origin")
        txt.setPos(0, 0)
        self.scene.addItem(txt)
        self.scene.addRect(0, 0, 3, 3)

    def decodeRect(self, rect: ZbaRect, scale):
        return rect.pos[0]*scale, rect.pos[1]*scale, rect.size[0]*scale, rect.size[1]*scale

    def drawRects(self, rect_list):
        for r in rect_list:
            x, y, lx, ly = self.decodeRect(r, 50)
            rect = QGraphicsRectItem(x, y, lx, ly)
            rect.setBrush(QBrush(QColor(Qt.gray)))
            self.scene.addItem(rect)
            print(r)


