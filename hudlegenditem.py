import math
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QColor


class HudLegendItem(QGraphicsItem):

    def __init__(self, parent=None, x=0, y=0, width=200, height=200, zoom=50, rect=None):
        super(HudLegendItem, self).__init__(parent)

        self.itemRect = QRectF(x, y, width, height)

        if rect is not None:
            self.itemRect = rect

        self.px = 20
        self.py = 50

        self.zoom_scale = zoom

        self.mousePos = QPointF()

        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setAcceptHoverEvents(True)

    def setZoomScale(self, scale):
        self.zoom_scale = scale

    def boundingRect(self):
        return self.itemRect

    def shape(self):
        path = QPainterPath()
        path.addRect(self.scene().sceneRect())
        return path

    def mousePressEvent(self, event):
        super(HudLegendItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.mousePos = event.pos()

    def paint(self, painter, option, widget=None):
        # TODO: make good names
        # TODO: optimize this
        # TODO: fix number display error, not in micrometers now
        # TODO: add line length
        hudRect = self.scene().parent().frameGeometry()
        hudw = hudRect.width()
        hudh = hudRect.height()
        sceneOriginInScene = self.scene().parent().scene().items(Qt.AscendingOrder)[0].mapToScene(2, 2)
        sceneOriginInView = self.scene().parent().mapFromScene(sceneOriginInScene)

        painter.save()

        pen = QPen(QColor(Qt.black))
        pen.setWidth(1)

        painter.setPen(pen)

        hudx = self.scene().parent().frameGeometry().x()
        hudy = self.scene().parent().frameGeometry().y()

        axis_origin = QPointF(hudx + self.px, hudy + hudh - self.py)

        painter.drawLine(hudx + self.px, hudy + 20,
                         axis_origin.x(), axis_origin.y())
        painter.drawLine(axis_origin.x(), axis_origin.y(),
                         hudx + hudw - self.px - 20, hudy + hudh - self.py)

        nx = 15
        ny = 10
        dx = (hudw - self.px - self.px - 20)/nx
        dy = (hudh - 20 - self.py)/ny

        # draw y markers
        for i in range(1, ny + 1):
            painter.drawLine(axis_origin.x(), axis_origin.y() - i * dy,
                             axis_origin.x() + 5, axis_origin.y() - i * dy)

        # draw x markers
        for i in range(1, nx + 1):
            painter.drawLine(axis_origin.x() + i * dx, axis_origin.y(),
                             axis_origin.x() + i * dx, axis_origin.y() + 5)

        # draw origin text
        font = painter.font()
        font.setPixelSize(10)
        painter.setFont(font)
        rect_origin_x = - (sceneOriginInView.x() - axis_origin.x())
        rect_origin_y = (sceneOriginInView.y() - axis_origin.y())
        painter.drawText(axis_origin.x() - 15, axis_origin.y() + 15, str(round(rect_origin_x/self.zoom_scale, 2)) + ":" + str(round(rect_origin_y/self.zoom_scale, 2)))

        # draw y marker text
        for i in range(1, ny + 1):
            rect_y = round((rect_origin_y + i * dy)/self.zoom_scale, 2)
            painter.drawText(axis_origin.x() + 10, axis_origin.y() + 3 - i * dy,
                             str(rect_y))

        # draw x marker text
        for i in range(1, nx + 1):
            rect_x = round((rect_origin_x + i * dx)/self.zoom_scale, 2)
            painter.drawText(axis_origin.x() - 15 + i * dx, axis_origin.y() + 15 + 10 * (i % 2),
                             str(rect_x))

        mp = self.mousePos
        mp_x = - (sceneOriginInView.x() - mp.x())
        mp_y = (sceneOriginInView.y() - mp.y())
        painter.drawText(hudx + hudw - 150, hudy + 20, "mouse pos: " + str(-mp_x/self.zoom_scale) + ":" + str(mp_y/self.zoom_scale))

        if self.scene().parent().hasRuler:
            rP1 = self.scene().parent().mapFromScene(self.scene().parent().rulerP1)
            rP2 = self.scene().parent().mapFromScene(self.scene().parent().rulerP2)
            rp1_x = -(sceneOriginInView.x() - rP1.x())/self.zoom_scale
            rp1_y = (sceneOriginInView.y() - rP1.y())/self.zoom_scale
            rp2_x = -(sceneOriginInView.x() - rP2.x())/self.zoom_scale
            rp2_y = (sceneOriginInView.y() - rP2.y())/self.zoom_scale

            painter.drawText(hudx + hudw - 150, hudy + 30, "ruler:")
            painter.drawText(hudx + hudw - 150, hudy + 40, "p1: " + str(rp1_x) + ":" + str(rp1_y))
            painter.drawText(hudx + hudw - 150, hudy + 50, "p2: " + str(rp2_x) + ":" + str(rp2_y))
            painter.drawText(hudx + hudw - 150, hudy + 60, "dx: " + str(round(abs(-(rp2_x - rp1_x)), 2)))
            painter.drawText(hudx + hudw - 150, hudy + 70, "dy: " + str(round(abs(rp2_y - rp1_y), 2)))
            painter.drawText(hudx + hudw - 150, hudy + 80,
                             "len: " + str(round(math.sqrt(pow(rp2_x - rp1_x, 2) + pow(rp2_y - rp1_y, 2)), 2)))

        self.itemRect = QRectF(0, 0, hudw, hudh)

        painter.restore()
