from zbadocument import ZbaDocument
from zbarect import ZbaRect
import sys
# from PyQt5.QtWidgets import QApplication
# from mainwindow import MainWindow
from zbatfield import ZbaTfield
from zbaufield import ZbaUfield

def main():
    # app = QApplication(sys.argv)
    # w = MainWindow()
    # w.initApp()
    # w.show()
    pass

    # txt ="TW:0,0,20,0,40,0;UW:0,0.6,0,1.2,0,1.8,0,2.4,0,3,0,3.6,0,4.2,0,4.8,0,5.4,0,6,0,6.6,0,7.2,0,7.8,0,8.4,0,9,0,9.6,0,10.2,0,10.8,0,11.4,0,12,0,12.6,0,13.2,0,13.8,0,14.4,0,15,0,15.6,0,16.2,0,16.8,0,17.4,0,18,0,18.6,0,19.2,0.1,0,0.1,19.8,1,0.6,1,1.2,1,1.8,1,2.4,1,3,1,3.6,1,4.2,1,4.8,1,5.4,1,6,1,6.6,1,7.2,1,7.8,1,8.4,1,9,1,9.6,1,10.2,1,10.8,1,11.4,1,12,1,12.6,1,13.2,1,13.8,1,14.4,1,15,1,15.6,1,16.2,1,16.8,1,17.4,1,18,1,18.6,1,19.2,1.1,0,1.1,19.8,2,0.6,2,1.2,2,1.8,2,2.4,2,3,2,3.6,2,4.2,2,4.8,2,5.4,2,6,2,6.6,2,7.2,2,7.8,2,8.4,2,9,2,9.6,2,10.2,2,10.8,2,11.4,2,12,2,12.6,2,13.2,2,13.8,2,14.4,2,15,2,15.6,2,16.2,2,16.8,2,17.4,2,18,2,18.6,2,19.2,2.1,0,2.1,19.8,3,0.6,3,1.2,3,1.8,3,2.4,3,3,3,3.6,3,4.2,3,4.8,3,5.4,3,6,3,6.6,3,7.2,3,7.8,3,8.4,3,9,3,9.6,3,10.2,3,10.8,3,11.4,3,12,3,12.6,3,13.2,3,13.8,3,14.4,3,15,3,15.6,3,16.2,3,16.8,3,17.4,3,18,3,18.6,3,19.2,3.1,0,3.1,19.8,4,0.6,4,1.2,4,1.8,4,2.4,4,3,4,3.6,4,4.2,4,4.8,4,5.4,4,6,4,6.6,4,7.2,4,7.8,4,8.4,4,9,4,9.6,4,10.2,4,10.8,4,11.4,4,12,4,12.6,4,13.2,4,13.8,4,14.4,4,15,4,15.6,4,16.2,4,16.8,4,17.4,4,18,4,18.6,4,19.2,4.1,0,4.1,19.8,5,0.6,5,1.2,5,1.8,5,2.4,5,3,5,3.6,5,4.2,5,4.8,5,5.4,5,6,5,6.6,5,7.2,5,7.8,5,8.4,5,9,5,9.6,5,10.2,5,10.8,5,11.4,5,12,5,12.6,5,13.2,5,13.8,5,14.4,5,15,5,15.6,5,16.2,5,16.8,5,17.4,5,18,5,18.6,5,19.2,5.1,0,5.1,19.8,6,0.6,6,1.2,6,1.8,6,2.4,6,3,6,3.6,6,4.2,6,4.8,6,5.4,6,6,6,6.6,6,7.2,6,7.8,6,8.4,6,9,6,9.6,6,10.2,6,10.8,6,11.4,6,12,6,12.6,6,13.2,6,13.8,6,14.4,6,15,6,15.6,6,16.2,6,16.8,6,17.4,6,18,6,18.6,6,19.2,6.1,0,6.1,19.8,7,0.6,7,1.2,7,1.8,7,2.4,7,3,7,3.6,7,4.2,7,4.8,7,5.4,7,6,7,6.6,7,7.2;R0,0,1,0.2;@UW:7,7.8,7,8.4,7,9,7,9.6,7,10.2,7,10.8,7,11.4,7,12,7,12.6,7,13.2,7,13.8,7,14.4,7,15,7,15.6,7,16.2,7,16.8,7,17.4,7,18,7,18.6,7,19.2,7.1,0,7.1,19.8,8,0.6,8,1.2,8,1.8,8,2.4,8,3,8,3.6,8,4.2,8,4.8,8,5.4,8,6,8,6.6,8,7.2,8,7.8,8,8.4,8,9,8,9.6,8,10.2,8,10.8,8,11.4,8,12,8,12.6,8,13.2,8,13.8,8,14.4,8,15,8,15.6,8,16.2,8,16.8,8,17.4,8,18,8,18.6,8,19.2,8.1,0,8.1,19.8,9,0.6,9,1.2,9,1.8,9,2.4,9,3,9,3.6,9,4.2,9,4.8,9,5.4,9,6,9,6.6,9,7.2,9,7.8,9,8.4,9,9,9,9.6,9,10.2,9,10.8,9,11.4,9,12,9,12.6,9,13.2,9,13.8,9,14.4,9,15,9,15.6,9,16.2,9,16.8,9,17.4,9,18,9,18.6,9,19.2,9.1,0,9.1,19.8,10,0.6,10,1.2,10,1.8,10,2.4,10,3,10,3.6,10,4.2,10,4.8,10,5.4,10,6,10,6.6,10,7.2,10,7.8,10,8.4,10,9,10,9.6,10,10.2,10,10.8,10,11.4,10,12,10,12.6,10,13.2,10,13.8,10,14.4,10,15,10,15.6,10,16.2,10,16.8,10,17.4,10,18,10,18.6,10,19.2,10.1,0,10.1,19.8,11,0.6,11,1.2,11,1.8,11,2.4,11,3,11,3.6,11,4.2,11,4.8,11,5.4,11,6,11,6.6,11,7.2,11,7.8,11,8.4,11,9,11,9.6,11,10.2,11,10.8,11,11.4,11,12,11,12.6,11,13.2,11,13.8,11,14.4,11,15,11,15.6,11,16.2,11,16.8,11,17.4,11,18,11,18.6,11,19.2,11.1,0,11.1,19.8,12,0.6,12,1.2,12,1.8,12,2.4,12,3,12,3.6,12,4.2,12,4.8,12,5.4,12,6,12,6.6,12,7.2,12,7.8,12,8.4,12,9,12,9.6,12,10.2,12,10.8,12,11.4,12,12,12,12.6,12,13.2,12,13.8,12,14.4,12,15,12,15.6,12,16.2,12,16.8,12,17.4,12,18,12,18.6,12,19.2,12.1,0,12.1,19.8,13,0.6,13,1.2,13,1.8,13,2.4,13,3,13,3.6,13,4.2,13,4.8,13,5.4,13,6,13,6.6,13,7.2,13,7.8,13,8.4,13,9,13,9.6,13,10.2,13,10.8,13,11.4,13,12,13,12.6,13,13.2,13,13.8,13,14.4,13,15,13,15.6,13,16.2,13,16.8,13,17.4,13,18,13,18.6,13,19.2,13.1,0,13.1,19.8,14,0.6,14,1.2,14,1.8,14,2.4,14,3,14,3.6,14,4.2,14,4.8,14,5.4,14,6,14,6.6,14,7.2,14,7.8,14,8.4,14,9,14,9.6,14,10.2,14,10.8,14,11.4,14,12,14,12.6,14,13.2,14,13.8,14,14.4;R0,0,1,0.2;@UW:14,15,14,15.6,14,16.2,14,16.8,14,17.4,14,18,14,18.6,14,19.2,14.1,0,14.1,19.8,15,0.6,15,1.2,15,1.8,15,2.4,15,3,15,3.6,15,4.2,15,4.8,15,5.4,15,6,15,6.6,15,7.2,15,7.8,15,8.4,15,9,15,9.6,15,10.2,15,10.8,15,11.4,15,12,15,12.6,15,13.2,15,13.8,15,14.4,15,15,15,15.6,15,16.2,15,16.8,15,17.4,15,18,15,18.6,15,19.2,15.1,0,15.1,19.8,16,0.6,16,1.2,16,1.8,16,2.4,16,3,16,3.6,16,4.2,16,4.8,16,5.4,16,6,16,6.6,16,7.2,16,7.8,16,8.4,16,9,16,9.6,16,10.2,16,10.8,16,11.4,16,12,16,12.6,16,13.2,16,13.8,16,14.4,16,15,16,15.6,16,16.2,16,16.8,16,17.4,16,18,16,18.6,16,19.2,16.1,0,16.1,19.8,17,0.6,17,1.2,17,1.8,17,2.4,17,3,17,3.6,17,4.2,17,4.8,17,5.4,17,6,17,6.6,17,7.2,17,7.8,17,8.4,17,9,17,9.6,17,10.2,17,10.8,17,11.4,17,12,17,12.6,17,13.2,17,13.8,17,14.4,17,15,17,15.6,17,16.2,17,16.8,17,17.4,17,18,17,18.6,17,19.2,17.1,0,17.1,19.8,18,0.6,18,1.2,18,1.8,18,2.4,18,3,18,3.6,18,4.2,18,4.8,18,5.4,18,6,18,6.6,18,7.2,18,7.8,18,8.4,18,9,18,9.6,18,10.2,18,10.8,18,11.4,18,12,18,12.6,18,13.2,18,13.8,18,14.4,18,15,18,15.6,18,16.2,18,16.8,18,17.4,18,18,18,18.6,18,19.2,18.1,0,18.1,19.8,19,0.6,19,1.2,19,1.8,19,2.4,19,3,19,3.6,19,4.2,19,4.8,19,5.4,19,6,19,6.6,19,7.2,19,7.8,19,8.4,19,9,19,9.6,19,10.2,19,10.8,19,11.4,19,12,19,12.6,19,13.2,19,13.8,19,14.4,19,15,19,15.6,19,16.2,19,16.8,19,17.4,19,18,19,18.6,19,19.2;R0,0,1,0.2;@UW:19.1,0.1,19.1,19.8;R0,0,0.9,0.1;@UW:19.1,0,19.1,19.9;R0,0,0.8,0.1;@UW:0,0.2,0,0.8,0,1.4,0,2,0,2.6,0,3.2,0,3.8,0,4.4,0,5,0,5.6,0,6.2,0,6.8,0,7.4,0,8,0,8.6,0,9.2,0,9.8,0,10.4,0,11,0,11.6,0,12.2,0,12.8,0,13.4,0,14,0,14.6,0,15.2,0,15.8,0,16.4,0,17,0,17.6,0,18.2,0,18.8,0,19.4,0.6,0.2,0.6,0.8,0.6,1.4,0.6,2,0.6,2.6,0.6,3.2,0.6,3.8,0.6,4.4,0.6,5,0.6,5.6,0.6,6.2,0.6,6.8,0.6,7.4,0.6,8,0.6,8.6,0.6,9.2,0.6,9.8,0.6,10.4,0.6,11,0.6,11.6,0.6,12.2,0.6,12.8,0.6,13.4,0.6,14,0.6,14.6,0.6,15.2,0.6,15.8,0.6,16.4,0.6,17,0.6,17.6,0.6,18.2,0.6,18.8,0.6,19.4,1.2,0.2,1.2,0.8,1.2,1.4,1.2,2,1.2,2.6,1.2,3.2,1.2,3.8,1.2,4.4,1.2,5,1.2,5.6,1.2,6.2,1.2,6.8,1.2,7.4,1.2,8,1.2,8.6,1.2,9.2,1.2,9.8,1.2,10.4,1.2,11,1.2,11.6,1.2,12.2,1.2,12.8,1.2,13.4,1.2,14,1.2,14.6,1.2,15.2,1.2,15.8,1.2,16.4,1.2,17,1.2,17.6,1.2,18.2,1.2,18.8,1.2,19.4,1.8,0.2,1.8,0.8,1.8,1.4,1.8,2,1.8,2.6,1.8,3.2,1.8,3.8,1.8,4.4,1.8,5,1.8,5.6,1.8,6.2,1.8,6.8,1.8,7.4,1.8,8,1.8,8.6,1.8,9.2,1.8,9.8,1.8,10.4,1.8,11,1.8,11.6,1.8,12.2,1.8,12.8,1.8,13.4,1.8,14,1.8,14.6,1.8,15.2,1.8,15.8,1.8,16.4,1.8,17,1.8,17.6,1.8,18.2,1.8,18.8,1.8,19.4,2.4,0.2,2.4,0.8,2.4,1.4,2.4,2,2.4,2.6,2.4,3.2,2.4,3.8,2.4,4.4,2.4,5,2.4,5.6,2.4,6.2,2.4,6.8,2.4,7.4,2.4,8,2.4,8.6,2.4,9.2,2.4,9.8,2.4,10.4,2.4,11,2.4,11.6,2.4,12.2,2.4,12.8,2.4,13.4,2.4,14,2.4,14.6,2.4,15.2,2.4,15.8,2.4,16.4,2.4,17,2.4,17.6,2.4,18.2,2.4,18.8,2.4,19.4,3,0.2,3,0.8,3,1.4,3,2,3,2.6,3,3.2,3,3.8,3,4.4,3,5,3,5.6,3,6.2,3,6.8,3,7.4,3,8,3,8.6,3,9.2,3,9.8,3,10.4,3,11,3,11.6,3,12.2,3,12.8,3,13.4,3,14,3,14.6,3,15.2,3,15.8,3,16.4,3,17,3,17.6,3,18.2,3,18.8,3,19.4,3.6,0.2,3.6,0.8,3.6,1.4,3.6,2,3.6,2.6,3.6,3.2,3.6,3.8,3.6,4.4,3.6,5,3.6,5.6,3.6,6.2,3.6,6.8,3.6,7.4,3.6,8,3.6,8.6,3.6,9.2,3.6,9.8,3.6,10.4,3.6,11,3.6,11.6,3.6,12.2,3.6,12.8,3.6,13.4,3.6,14,3.6,14.6,3.6,15.2,3.6,15.8,3.6,16.4,3.6,17,3.6,17.6,3.6,18.2,3.6,18.8,3.6,19.4,4.2,0.2,4.2,0.8,4.2,1.4,4.2,2,4.2,2.6,4.2,3.2,4.2,3.8,4.2,4.4,4.2,5,4.2,5.6,4.2,6.2,4.2,6.8,4.2,7.4,4.2,8,4.2,8.6,4.2,9.2,4.2,9.8,4.2,10.4,4.2,11;R0,0,0.2,0.4;@UW:4.2,11.6,4.2,12.2,4.2,12.8,4.2,13.4,4.2,14,4.2,14.6,4.2,15.2,4.2,15.8,4.2,16.4,4.2,17,4.2,17.6,4.2,18.2,4.2,18.8,4.2,19.4,4.8,0.2,4.8,0.8,4.8,1.4,4.8,2,4.8,2.6,4.8,3.2,4.8,3.8,4.8,4.4,4.8,5,4.8,5.6,4.8,6.2,4.8,6.8,4.8,7.4,4.8,8,4.8,8.6,4.8,9.2,4.8,9.8,4.8,10.4,4.8,11,4.8,11.6,4.8,12.2,4.8,12.8,4.8,13.4,4.8,14,4.8,14.6,4.8,15.2,4.8,15.8,4.8,16.4,4.8,17,4.8,17.6,4.8,18.2,4.8,18.8,4.8,19.4,5.4,0.2,5.4,0.8,5.4,1.4,5.4,2,5.4,2.6,5.4,3.2,5.4,3.8,5.4,4.4,5.4,5,5.4,5.6,5.4,6.2,5.4,6.8,5.4,7.4,5.4,8,5.4,8.6,5.4,9.2,5.4,9.8,5.4,10.4,5.4,11,5.4,11.6,5.4,12.2,5.4,12.8,5.4,13.4,5.4,14,5.4,14.6,5.4,15.2,5.4,15.8,5.4,16.4,5.4,17,5.4,17.6,5.4,18.2,5.4,18.8,5.4,19.4,6,0.2,6,0.8,6,1.4,6,2,6,2.6,6,3.2,6,3.8,6,4.4,6,5,6,5.6,6,6.2,6,6.8,6,7.4,6,8,6,8.6,6,9.2,6,9.8,6,10.4,6,11,6,11.6,6,12.2,6,12.8,6,13.4,6,14,6,14.6,6,15.2,6,15.8,6,16.4,6,17,6,17.6,6,18.2,6,18.8,6,19.4,6.6,0.2,6.6,0.8,6.6,1.4,6.6,2,6.6,2.6,6.6,3.2,6.6,3.8,6.6,4.4,6.6,5,6.6,5.6,6.6,6.2,6.6,6.8,6.6,7.4,6.6,8,6.6,8.6,6.6,9.2,6.6,9.8,6.6,10.4,6.6,11,6.6,11.6,6.6,12.2,6.6,12.8,6.6,13.4,6.6,14,6.6,14.6,6.6,15.2,6.6,15.8,6.6,16.4,6.6,17,6.6,17.6,6.6,18.2,6.6,18.8,6.6,19.4,7.2,0.2,7.2,0.8,7.2,1.4,7.2,2,7.2,2.6,7.2,3.2,7.2,3.8,7.2,4.4,7.2,5,7.2,5.6,7.2,6.2,7.2,6.8,7.2,7.4,7.2,8,7.2,8.6,7.2,9.2,7.2,9.8,7.2,10.4,7.2,11,7.2,11.6,7.2,12.2,7.2,12.8,7.2,13.4,7.2,14,7.2,14.6,7.2,15.2,7.2,15.8,7.2,16.4,7.2,17,7.2,17.6,7.2,18.2,7.2,18.8,7.2,19.4,7.8,0.2,7.8,0.8,7.8,1.4,7.8,2,7.8,2.6,7.8,3.2,7.8,3.8,7.8,4.4,7.8,5,7.8,5.6,7.8,6.2,7.8,6.8,7.8,7.4,7.8,8,7.8,8.6,7.8,9.2,7.8,9.8,7.8,10.4,7.8,11,7.8,11.6,7.8,12.2,7.8,12.8,7.8,13.4,7.8,14,7.8,14.6,7.8,15.2,7.8,15.8,7.8,16.4,7.8,17,7.8,17.6,7.8,18.2,7.8,18.8,7.8,19.4,8.4,0.2,8.4,0.8,8.4,1.4,8.4,2,8.4,2.6,8.4,3.2,8.4,3.8,8.4,4.4,8.4,5,8.4,5.6,8.4,6.2,8.4,6.8,8.4,7.4,8.4,8,8.4,8.6,8.4,9.2,8.4,9.8,8.4,10.4,8.4,11,8.4,11.6,8.4,12.2,8.4,12.8,8.4,13.4,8.4,14,8.4,14.6,8.4,15.2,8.4,15.8,8.4,16.4,8.4,17,8.4,17.6,8.4,18.2,8.4,18.8,8.4,19.4,9,0.2,9,0.8,9,1.4,9,2,9,2.6;R0,0,0.2,0.4;@UW:9,3.2,9,3.8,9,4.4,9,5,9,5.6,9,6.2,9,6.8,9,7.4,9,8,9,8.6,9,9.2,9,9.8,9,10.4,9,11,9,11.6,9,12.2,9,12.8,9,13.4,9,14,9,14.6,9,15.2,9,15.8,9,16.4,9,17,9,17.6,9,18.2,9,18.8,9,19.4,9.6,0.2,9.6,0.8,9.6,1.4,9.6,2,9.6,2.6,9.6,3.2,9.6,3.8,9.6,4.4,9.6,5,9.6,5.6,9.6,6.2,9.6,6.8,9.6,7.4,9.6,8,9.6,8.6,9.6,9.2,9.6,9.8,9.6,10.4,9.6,11,9.6,11.6,9.6,12.2,9.6,12.8,9.6,13.4,9.6,14,9.6,14.6,9.6,15.2,9.6,15.8,9.6,16.4,9.6,17,9.6,17.6,9.6,18.2,9.6,18.8,9.6,19.4,10.2,0.2,10.2,0.8,10.2,1.4,10.2,2,10.2,2.6,10.2,3.2,10.2,3.8,10.2,4.4,10.2,5,10.2,5.6,10.2,6.2,10.2,6.8,10.2,7.4,10.2,8,10.2,8.6,10.2,9.2,10.2,9.8,10.2,10.4,10.2,11,10.2,11.6,10.2,12.2,10.2,12.8,10.2,13.4,10.2,14,10.2,14.6,10.2,15.2,10.2,15.8,10.2,16.4,10.2,17,10.2,17.6,10.2,18.2,10.2,18.8,10.2,19.4,10.8,0.2,10.8,0.8,10.8,1.4,10.8,2,10.8,2.6,10.8,3.2,10.8,3.8,10.8,4.4,10.8,5,10.8,5.6,10.8,6.2,10.8,6.8,10.8,7.4,10.8,8,10.8,8.6,10.8,9.2,10.8,9.8,10.8,10.4,10.8,11,10.8,11.6,10.8,12.2,10.8,12.8,10.8,13.4,10.8,14,10.8,14.6,10.8,15.2,10.8,15.8,10.8,16.4,10.8,17,10.8,17.6,10.8,18.2,10.8,18.8,10.8,19.4,11.4,0.2,11.4,0.8,11.4,1.4,11.4,2,11.4,2.6,11.4,3.2,11.4,3.8,11.4,4.4,11.4,5,11.4,5.6,11.4,6.2,11.4,6.8,11.4,7.4,11.4,8,11.4,8.6,11.4,9.2,11.4,9.8,11.4,10.4,11.4,11,11.4,11.6,11.4,12.2,11.4,12.8,11.4,13.4,11.4,14,11.4,14.6,11.4,15.2,11.4,15.8,11.4,16.4,11.4,17,11.4,17.6,11.4,18.2,11.4,18.8,11.4,19.4,12,0.2,12,0.8,12,1.4,12,2,12,2.6,12,3.2,12,3.8,12,4.4,12,5,12,5.6,12,6.2,12,6.8,12,7.4,12,8,12,8.6,12,9.2,12,9.8,12,10.4,12,11,12,11.6,12,12.2,12,12.8,12,13.4,12,14,12,14.6,12,15.2,12,15.8,12,16.4,12,17,12,17.6,12,18.2,12,18.8,12,19.4,12.6,0.2,12.6,0.8,12.6,1.4,12.6,2,12.6,2.6,12.6,3.2,12.6,3.8,12.6,4.4,12.6,5,12.6,5.6,12.6,6.2,12.6,6.8,12.6,7.4,12.6,8,12.6,8.6,12.6,9.2,12.6,9.8,12.6,10.4,12.6,11,12.6,11.6,12.6,12.2,12.6,12.8,12.6,13.4,12.6,14,12.6,14.6,12.6,15.2,12.6,15.8,12.6,16.4,12.6,17,12.6,17.6,12.6,18.2,12.6,18.8,12.6,19.4,13.2,0.2,13.2,0.8,13.2,1.4,13.2,2,13.2,2.6,13.2,3.2,13.2,3.8,13.2,4.4,13.2,5,13.2,5.6,13.2,6.2,13.2,6.8,13.2,7.4,13.2,8,13.2,8.6,13.2,9.2,13.2,9.8,13.2,10.4,13.2,11,13.2,11.6,13.2,12.2,13.2,12.8,13.2,13.4,13.2,14;R0,0,0.2,0.4;@UW:13.2,14.6,13.2,15.2,13.2,15.8,13.2,16.4,13.2,17,13.2,17.6,13.2,18.2,13.2,18.8,13.2,19.4,13.8,0.2,13.8,0.8,13.8,1.4,13.8,2,13.8,2.6,13.8,3.2,13.8,3.8,13.8,4.4,13.8,5,13.8,5.6,13.8,6.2,13.8,6.8,13.8,7.4,13.8,8,13.8,8.6,13.8,9.2,13.8,9.8,13.8,10.4,13.8,11,13.8,11.6,13.8,12.2,13.8,12.8,13.8,13.4,13.8,14,13.8,14.6,13.8,15.2,13.8,15.8,13.8,16.4,13.8,17,13.8,17.6,13.8,18.2,13.8,18.8,13.8,19.4,14.4,0.2,14.4,0.8,14.4,1.4,14.4,2,14.4,2.6,14.4,3.2,14.4,3.8,14.4,4.4,14.4,5,14.4,5.6,14.4,6.2,14.4,6.8,14.4,7.4,14.4,8,14.4,8.6,14.4,9.2,14.4,9.8,14.4,10.4,14.4,11,14.4,11.6,14.4,12.2,14.4,12.8,14.4,13.4,14.4,14,14.4,14.6,14.4,15.2,14.4,15.8,14.4,16.4,14.4,17,14.4,17.6,14.4,18.2,14.4,18.8,14.4,19.4,15,0.2,15,0.8,15,1.4,15,2,15,2.6,15,3.2,15,3.8,15,4.4,15,5,15,5.6,15,6.2,15,6.8,15,7.4,15,8,15,8.6,15,9.2,15,9.8,15,10.4,15,11,15,11.6,15,12.2,15,12.8,15,13.4,15,14,15,14.6,15,15.2,15,15.8,15,16.4,15,17,15,17.6,15,18.2,15,18.8,15,19.4,15.6,0.2,15.6,0.8,15.6,1.4,15.6,2,15.6,2.6,15.6,3.2,15.6,3.8,15.6,4.4,15.6,5,15.6,5.6,15.6,6.2,15.6,6.8,15.6,7.4,15.6,8,15.6,8.6,15.6,9.2,15.6,9.8,15.6,10.4,15.6,11,15.6,11.6,15.6,12.2,15.6,12.8,15.6,13.4,15.6,14,15.6,14.6,15.6,15.2,15.6,15.8,15.6,16.4,15.6,17,15.6,17.6,15.6,18.2,15.6,18.8,15.6,19.4,16.2,0.2,16.2,0.8,16.2,1.4,16.2,2,16.2,2.6,16.2,3.2,16.2,3.8,16.2,4.4,16.2,5,16.2,5.6,16.2,6.2,16.2,6.8,16.2,7.4,16.2,8,16.2,8.6,16.2,9.2,16.2,9.8,16.2,10.4,16.2,11,16.2,11.6,16.2,12.2,16.2,12.8,16.2,13.4,16.2,14,16.2,14.6,16.2,15.2,16.2,15.8,16.2,16.4,16.2,17,16.2,17.6,16.2,18.2,16.2,18.8,16.2,19.4,16.8,0.2,16.8,0.8,16.8,1.4,16.8,2,16.8,2.6,16.8,3.2,16.8,3.8,16.8,4.4,16.8,5,16.8,5.6,16.8,6.2,16.8,6.8,16.8,7.4,16.8,8,16.8,8.6,16.8,9.2,16.8,9.8,16.8,10.4,16.8,11,16.8,11.6,16.8,12.2,16.8,12.8,16.8,13.4,16.8,14,16.8,14.6,16.8,15.2,16.8,15.8,16.8,16.4,16.8,17,16.8,17.6,16.8,18.2,16.8,18.8,16.8,19.4,17.4,0.2,17.4,0.8,17.4,1.4,17.4,2,17.4,2.6,17.4,3.2,17.4,3.8,17.4,4.4,17.4,5,17.4,5.6,17.4,6.2,17.4,6.8,17.4,7.4,17.4,8,17.4,8.6,17.4,9.2,17.4,9.8,17.4,10.4,17.4,11,17.4,11.6,17.4,12.2,17.4,12.8,17.4,13.4,17.4,14,17.4,14.6,17.4,15.2,17.4,15.8,17.4,16.4,17.4,17,17.4,17.6,17.4,18.2,17.4,18.8,17.4,19.4,18,0.2,18,0.8,18,1.4,18,2,18,2.6,18,3.2,18,3.8,18,4.4,18,5,18,5.6;R0,0,0.2,0.4;@UW:18,6.2,18,6.8,18,7.4,18,8,18,8.6,18,9.2,18,9.8,18,10.4,18,11,18,11.6,18,12.2,18,12.8,18,13.4,18,14,18,14.6,18,15.2,18,15.8,18,16.4,18,17,18,17.6,18,18.2,18,18.8,18,19.4,18.6,0.2,18.6,0.8,18.6,1.4,18.6,2,18.6,2.6,18.6,3.2,18.6,3.8,18.6,4.4,18.6,5,18.6,5.6,18.6,6.2,18.6,6.8,18.6,7.4,18.6,8,18.6,8.6,18.6,9.2,18.6,9.8,18.6,10.4,18.6,11,18.6,11.6,18.6,12.2,18.6,12.8,18.6,13.4,18.6,14,18.6,14.6,18.6,15.2,18.6,15.8,18.6,16.4,18.6,17,18.6,17.6,18.6,18.2,18.6,18.8,18.6,19.4,19.2,0.2,19.2,0.8,19.2,1.4,19.2,2,19.2,2.6,19.2,3.2,19.2,3.8,19.2,4.4,19.2,5,19.2,5.6,19.2,6.2,19.2,6.8,19.2,7.4,19.2,8,19.2,8.6,19.2,9.2,19.2,9.8,19.2,10.4,19.2,11,19.2,11.6,19.2,12.2,19.2,12.8,19.2,13.4,19.2,14,19.2,14.6,19.2,15.2,19.2,15.8,19.2,16.4,19.2,17,19.2,17.6,19.2,18.2,19.2,18.8,19.2,19.4,19.8,0.2,19.8,0.8,19.8,1.4,19.8,2,19.8,2.6,19.8,3.2,19.8,3.8,19.8,4.4,19.8,5,19.8,5.6,19.8,6.2,19.8,6.8,19.8,7.4,19.8,8,19.8,8.6,19.8,9.2,19.8,9.8,19.8,10.4,19.8,11,19.8,11.6,19.8,12.2,19.8,12.8,19.8,13.4,19.8,14,19.8,14.6,19.8,15.2,19.8,15.8,19.8,16.4,19.8,17,19.8,17.6,19.8,18.2,19.8,18.8,19.8,19.4;R0,0,0.2,0.4;@UW:0,0.1,0,19.8;R0,0,0.1,0.1;@"
    # rectlist = [ZbaRect.from_string("R" + s) for s in txt.strip("R").split("R")]

    # uf = ZbaUfield.from_string(txt)
    # w.decodeUfield([0, 0], uf, 100)

    # tf = ZbaTfield.from_string(txt)
    # w.decodeTfield(tf, 100)
    #
    # sys.exit(app.exec_())

def parse_header():
    text = '                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ODB:GK41   .OL,  TX, E, AF 3200*3200, M 1, GF 6.0, KR 0.2, IV 10,10,10,10,10,10,10,10;                                                                                                                                                                                                                                                                                                                                                                                                                                         @'

    odb_mark = Suppress('ODB:')
    file_name = Combine(Word(alphanums) + Suppress(ZeroOrMore(' ')) + '.' + Word(alphanums))('file_name')
    comma = Suppress(',')
    file_format = oneOf('TX', 'BI')('file_format')
    data_type = Suppress(oneOf('E', 'P'))('data_type')
    af_size = Group(Suppress('AF') + ppc.integer + Suppress('*') + ppc.integer)('af_size')
    m_mark = (Suppress('M') + ppc.integer)('wafer_factor')
    max_fig = (Suppress('GF') + ppc.real)('max_fig')
    max_alias = (Suppress('KR') + ppc.real)('max_alias')
    dose_table = Group(Suppress('IV') + (ppc.integer + comma) * 7 + ppc.integer)('dose_table')
    semicolon = Suppress(';')
    at_mark = Suppress('@')

    zba_header = odb_mark + file_name + comma + file_format + comma + data_type + comma + af_size + comma + m_mark + \
                 comma + max_fig + comma + max_alias + comma + dose_table + semicolon + at_mark

    res = zba_header.parseString(text)

    print(res.dump())


if __name__ == '__main__':
    # Word(nums, exact=N)   # exact number of digits
    # Combine()             # combine tokens in a single entity
    # setDefaultWhitespaceChars   # set custom whitespace
    # setName()             # display pattern name in debug
    # parseString(str, parseAll=True)   # force to parse whole string
    # scanString('aaabaaaa', overlap=False)   # scan whole string for all matches, return matches with start end locs

    from pyparsing import *

    # text = 'R0,.2,5.7,0.2,*2;'
    # text = 'R0,.2,5.7,0.2;'
    # text = 'R3,0,.7,.1;2.1,0,.7,.1;4.2,0,.7,.1;6.3,0,.7,.1;8.4,0,.7,.1;'
    # text = 'R.0,.2,5.7,.2;R.0,.4,1.9,.2;R.0,.2,5.7,.2;R.0,.4,1.9,.2;'

    # uw_text = 'UW:19,11,19,12,19,13,19,14,19,15;R0,0,.5,5;1,0,.5,5;2,0,.5,5;3,0,.5,5;4,0,.5,5;@'
    uw_text = 'UW:19,11,19,12,19,13,19,14,19,15;R.0,.2,5.7,.2;R.0,.4,1.9,.2;R.0,.2,5.7,.2;R.0,.4,1.9,.2;@'
    ut_text = 'UT:0,0;R0,0,6.4,6.4;R6.4,6.4,6.4,6.4;@'
    ur_text = 'UR:0,0,1.3,25.6,3,3;R0,0,0.7,25.6;@'
    um_text = 'UM:0,0,10,10,20,20,0000000000000111111100000000000001111111000000000000001111110000000000000011111100000000000000011111000000000000000111110000000000000000111100000000000000001111000000000000000001110000000000000000011100000000000000000011000000000000000000110000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000;R0,0,.5,5;1,0,.5,5;2,0,.5,5;3,0,.5,5;4,0,.5,5;5,0,.5,5;@'
    # um_text = 'UM:0,0,10,10,20,20;R0,0,.5,5;1,0,.5,5;2,0,.5,5;3,0,.5,5;4,0,.5,5;5,0,.5,5;@'

    rect_mark = Suppress('R')
    comma = Suppress(',')
    zba_real = Combine(ZeroOrMore(Word(nums)) + '.' + Word(nums)) ^ Word(nums)
    rect_coords = (zba_real + comma) * 3 + zba_real
    dose = Suppress(',*') + Word('01234567', exact=1)
    semicolon = Suppress(';')
    rect_stub = Group(rect_coords + Optional(dose, default='1') + semicolon)
    # rect_stub.setParseAction(lambda s, l, t: ZbaRect.from_string_list(t[0]))

    tri_mark = Suppress('D')

    zba_rect_array = OneOrMore(rect_mark + rect_stub)
    zba_rect_list = rect_mark + rect_stub + ZeroOrMore(rect_stub)

    uf_coords = Group(zba_real + comma + zba_real + ZeroOrMore((comma + zba_real) * 2))
    at_mark = Suppress('@')

    uw_mark = Suppress('UW:')
    uw_field = uw_mark + uf_coords + semicolon + (zba_rect_list ^ zba_rect_array) + at_mark
    # uw_field.setParseAction(ZbaUfield.from_uw_string_list)

    ut_mark = Suppress('UT:')
    ut_field = ut_mark + uf_coords + semicolon + (zba_rect_list ^ zba_rect_array) + at_mark
    # ut_field.setParseAction(ZbaUfield.from_ut_string_list)

    ur_mark = Suppress('UR:')
    ur_field = ur_mark + uf_coords + semicolon + (zba_rect_list ^ zba_rect_array) + at_mark
    # ur_field.setParseAction(ZbaUfield.from_ur_string_list)

    um_mark = Suppress('UM:')
    um_matrix = Word('10')
    um_field = um_mark + uf_coords + Optional(comma + um_matrix, default='full') + semicolon + (zba_rect_list ^ zba_rect_array) + at_mark
    um_field.setParseAction(ZbaUfield.from_um_string_list)

    # res = ut_field.parseString(ut_text, parseAll=True)
    # res = uw_field.parseString(uw_text, parseAll=True)
    # res = ur_field.parseString(ur_text, parseAll=True)
    res = um_field.parseString(um_text, parseAll=True)
    print(res)

# TODO try regex parsing
# https://www.accelebrate.com/blog/pyparseltongue-parsing-text-with-pyparsing/


# http://www.ptmcg.com/geo/python/howtousepyparsing.html
# http://www.ccp4.ac.uk/dist/checkout/pyparsing-2.0.1/HowToUsePyparsing.html
# http://infohost.nmt.edu/~shipman/soft/pyparsing/web/index.html


# https://arxiv.org/pdf/1603.02720.pdf
# http://uol.de/physik/forschung/ehf/lcp/optisim/
# https://pypi.org/project/pyLuminous/
# https://github.com/sbyrnes321/tmm
# https://pypi.org/project/tmm/



