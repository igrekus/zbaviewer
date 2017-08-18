from zbadocument import ZbaDocument
from zbarect import ZbaRect
import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.initApp()
    w.show()

    # with open("data/apr1.txt") as f:
    # with open("data/gk41.txt") as f:
    # with open("data/pln1-.001") as f:
    # with open("data/pln1-.002") as f:
    # # with open("data/c10c1.d") as f:
    #     content = ''.join(f.readlines())

    # doc = ZbaDocument.from_string(content)
    # print(doc)

    with open("data/test.txt") as f:
        txt = ''.join(f.readlines())

    # txt = "R0,0,.5,5;R1,0,.5,5;R2,0,.5,5;R3,0,.5,5;R4,0,.5,5;R5,0,.5,5;R6,0,.5,5;R7,0,.5,5;R8,0,.5,5;R9,0,.5,5;R0,5,.5,5;R1,5,.5,5;R2,5,.5,5;R3,5,.5,5;R4,5,.5,5;R5,5,.5,5;R6,5,.5,5;R7,5,.5,5;R8,5,.5,5;R9,5,.5,5;"

    rectlist = [ZbaRect.from_string("R" + s) for s in txt.strip("R").split("R")]

    w.drawRects(rectlist)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
