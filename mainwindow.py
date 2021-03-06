# import copy
# from zbatfield import ZbaTfield
# from zbaufield import ZbaUfield
# from zbarect import ZbaRect
# # from PyQt5 import uic
# # from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsRectItem
# # from PyQt5.QtGui import QBrush, QColor
# # from PyQt5.QtCore import Qt
#
#
# class MainWindow(QMainWindow):
#
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#
#         self.setAttribute(Qt.WA_QuitOnClose)
#         self.setAttribute(Qt.WA_DeleteOnClose)
#
#         # create instance variables
#         # ui
#         self.ui = uic.loadUi("mainwindow.ui", self)
#
#         # scene
#         self.scene = QGraphicsScene(self)
#
#         # origin
#         self.originRect = QGraphicsRectItem(0, 0, 4, 4)
#         self.originRect.setPos(-2, -2)
#         self.scene.addItem(self.originRect)
#
#         # setup signals
#         self.ui.btnZoomIn.clicked.connect(self.onBtnZoomInClicked)
#         self.ui.btnZoomOut.clicked.connect(self.onBtnZoomOutClicked)
#
#     def initApp(self):
#         self.ui.graphicsHudView.setScene(self.scene)
#         self.ui.graphicsHudView.setSceneRect(0, 0, 2000000, 2000000)
#         self.ui.graphicsHudView.centerOn(self.originRect)
#         # self.ui.graphicsHudView.initView()
#
#         # self.ui.graphicsHudView.verticalScrollBar().valueChanged.connect(self.onHudViewScroll)
#         # self.ui.graphicsHudView.verticalScrollBar().sliderMoved.connect(self.onHudViewScroll)
#         # self.ui.graphicsHudView.horizontalScrollBar().valueChanged.connect(self.onHudViewScroll)
#
#     def resizeEvent(self, event):
#         self.ui.graphicsHudView.resize(self.ui.graphicsHudView.size())
#         self.ui.graphicsHudView.hudOverlayScene.setSceneRect(
#             self.ui.graphicsHudView.hudOverlayScene.items()[0].boundingRect())
#         super(MainWindow, self).resizeEvent(event)
#
#     def onHudViewScroll(self, int):
#         # self.ui.graphicsHudView.hudOverlayScene.items()[0].update(0, 0, 50, 50)
#         # self.ui.graphicsHudView.hudOverlayScene.update()
#         pass
#
#     def onBtnZoomInClicked(self):
#         self.ui.graphicsHudView.centerOn(0, 0)
#         print("zoom in")
#
#     def onBtnZoomOutClicked(self):
#         print("zoom out")
#
#     def decodeUfield(self, tfpos: list, uf: ZbaUfield, scale: int):
#         self.ui.graphicsHudView.hudLegendItem.zoom_scale = scale
#         for p in uf.pos_list:
#             for r in uf.rect_list:
#                 tr = ZbaRect.fromCopy(r)
#                 tr.setBrush(QBrush(QColor(Qt.gray)))
#                 tr.scaleRect(scale)
#                 tr.setPos((tfpos[0] + p[0])*scale + tr.posx,
#                           -(tfpos[1] + p[1])*scale - tr.posy - tr.rect().height())
#                 self.scene.addItem(tr)
#
#     def decodeTfield(self, tf: ZbaTfield, scale: int):
#         self.ui.graphicsHudView.hudLegendItem.zoom_scale = scale
#         for p in tf.pos_list:
#             for u in tf.ufield_list:
#                 self.decodeUfield(p, u, scale)
#         # for u in tf.ufield_list:
#         #     print(u)
#         #     for r in u.rect_list:
#         #         print(r)
