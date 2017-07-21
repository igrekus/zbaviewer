from zbadocument import ZbaDocument
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
    with open("data/c10c1.d") as f:
        content = ''.join(f.readlines())

    doc = ZbaDocument.from_string(content)
    print(sys.getsizeof(doc))
    print(doc)

    print("--- AF ---")
    print(doc.afield_list[0])
    print("--- TF ---")
    print(doc.afield_list[0].tfield_list[0])
    print("--- RECTs ---")

    # w.drawRects(doc.afield_list[0].tfield_list[0].ufield_list[0].rect_list)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
