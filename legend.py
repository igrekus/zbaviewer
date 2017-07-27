from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainterPath


class Legend(QGraphicsItem):

    def __init__(self, parent=None, x=0, y=0, width=200, height=200):
        super(Legend, self).__init__(parent)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(0, 0, 20, 20)
        return path

    def paint(self, painter, option, widget=None):
        painter.drawLine(self.x, self.y, self.x, self.height)

    # QRectF boundingRect() const override;
    # QPainterPath shape() const override;
    # void paint(QPainter *painter, const QStyleOptionGraphicsItem *item, QWidget *widget) override;
