from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene
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
        self.scene.addText("Test")
        self.scene.addRect(0, 0, 10, 10)
