from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QColor


class HudLegend(QGraphicsItem):

    def __init__(self, parent=None, x=0, y=0, width=200, height=200):
        super(HudLegend, self).__init__(parent)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.px = 20
        self.py = 50

        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(0, 0, 20, 20)
        return path

    def paint(self, painter, option, widget=None):
        hudRect = self.scene().parent().frameGeometry()
        hudTopLeft = hudRect.topLeft()
        hudBottomRight = hudRect.bottomRight()
        hudw = self.scene().parent().frameGeometry().width()
        hudh = self.scene().parent().frameGeometry().height()
        sceneOrigin = self.scene().parent().scene().items(Qt.AscendingOrder)[0].mapToScene(2, 2)

        print(hudTopLeft.x(), hudTopLeft.y())
        print(hudBottomRight.x(), hudBottomRight.y())
        print(hudTopLeft.x() + hud)
        print(sceneOrigin)
        painter.save()

        # p = QPainter()
        # p.setPen()
        pen = QPen(QColor(Qt.black))
        pen.setWidth(2)

        painter.setPen(pen)

        hudx = self.scene().parent().frameGeometry().x()
        hudy = self.scene().parent().frameGeometry().y()


        painter.drawLine(hudx + self.px, hudy + 20,
                         hudx + self.px, hudy + hudh - self.py)
        painter.drawLine(hudx + self.px, hudy + hudh - self.py,
                         hudx + hudw - self.px, hudy + hudh - self.py)

        painter.restore()

    # QRectF boundingRect() const override;
    # QPainterPath shape() const override;
    # void paint(QPainter *painter, const QStyleOptionGraphicsItem *item, QWidget *widget) override;
