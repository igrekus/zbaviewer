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
        # print("boundingRect() call")
        return self.itemRect
        # return QRectF(0, 0, 500, 500)

    def shape(self):
        # print("shape() call")
        path = QPainterPath()
        path.addRect(self.scene().sceneRect())
        return path

    def mousePressEvent(self, event):
        super(HudLegendItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # print(self.flags())
        # print("hud item mouse move event:", event.pos())
        self.mousePos = event.pos()
        # super(HudLegend, self).mouseMoveEvent(event)

    def paint(self, painter, option, widget=None):
        # TODO: make good names
        # TODO: optimize this
        hudRect = self.scene().parent().frameGeometry()
        hudw = hudRect.width()
        hudh = hudRect.height()
        sceneOrigin = self.scene().parent().scene().items(Qt.AscendingOrder)[0].mapToScene(2, 2)
        sceneOriginInView = self.scene().parent().mapFromScene(sceneOrigin)

        painter.save()

        # p = QPainter()
        # p.setPen()
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

        # pen.setColor(QColor(Qt.red))
        # painter.setPen(pen)

        ny = 10
        nx = 15
        dy = (hudh - 20 - self.py)/ny
        dx = (hudw - self.px - self.px - 20)/nx

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
        rect_origin_x = (sceneOriginInView.x() - axis_origin.x())
        rect_origin_y = (sceneOriginInView.y() - axis_origin.y())
        painter.drawText(axis_origin.x() - 15, axis_origin.y() + 15, str(rect_origin_x/self.zoom_scale) + ":" + str(rect_origin_y/self.zoom_scale))

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
        mp_x = (sceneOriginInView.x() - mp.x())
        mp_y = (sceneOriginInView.y() - mp.y())
        painter.drawText(hudx + hudw - 150, hudy + 20, "mouse pos: " + str(mp_x/self.zoom_scale) + ":" + str(mp_y/self.zoom_scale))

        self.itemRect = QRectF(0, 0, hudw, hudh)

        painter.restore()
