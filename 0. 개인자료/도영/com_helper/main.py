# import open source
import sys
import datetime
import time
import os
import com_helper as ch

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QThread, pyqtSignal
from threading import Thread

from pandas import DataFrame
import pandas as pd
import cv2


class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("Main.ui")
        
       
        # 함수 바인딩 부분
        self.ui.btnStart.clicked.connect(self.start) # 영상 실행 버튼 연결
        self.ui.btnEnd.clicked.connect(self.end) # 영상 종료 버튼 연결
      
        self.ui.actionFileOpen.triggered.connect(self.fileopen)

        self.ui.show()

        # self.ui.previewSmall.setPixmap(QPixmap('cat04_256.png'))
    
    def start(self):
        global fname
        setImage(frame)

    def end(self):
        pass
    def fileopen(self):
        global fname
        fname = QFileDialog.getOpenFileName()
        fname=fname[0]
        frame=ch.rcnn_video(fname)

    # @QtCore.pyqtSlot(QtGui.QImage)
    # def setImage(self, image):
    #     if image.isNull():
    #         print("Viewer Dropped frame!")

    #     self.image = image
    #     if image.size() != self.size():
    #         self.cv2.setFixedSize(image.size())
    #     self.QWidget.update()


        






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())