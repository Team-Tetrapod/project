# import open source
import sys
import datetime
import time
import os
# import com_helper as ch

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5.QAxContainer import *
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
        frame = rcnn_video(fname)

def rcnn_video(video_name):

    video = video_name
    weights = "C:/Users/Kyujin/Desktop/Project/project/0. 개인자료/도영/com_helper/yolov3-computer.weights"
    config = "C:/Users/Kyujin/Desktop/Project/project/0. 개인자료/도영/com_helper/yolov3-computer.cfg"
    argclasses = "C:/Users/Kyujin/Desktop/Project/project/0. 개인자료/도영/com_helper/yolov3-computer.txt"
    cap_video = cv2.VideoCapture(video)

    count = 0

    while True:
        ret, frame = cap_video.read()
        frame = cv2.resize(frame, (512, 512))
        if ret == False:
            break
        count += 1
        if int(cap_video.get(1) % 10 == 0):
            image = frame

            Width = image.shape[1]
            Height = image.shape[0]
            print(Width, Height)
            scale = 0.00392

            classes = None

            with open(argclasses, 'r') as f:
                classes = [line.strip() for line in f.readlines()]

            COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

            net = cv2.dnn.readNet(weights, config)

            blob = cv2.dnn.blobFromImage(image, scale, (512, 512), (0, 0, 0), True, crop=False)

            net.setInput(blob)

            outs = net.forward(get_output_layers(net))

            class_ids = []
            confidences = []
            boxes = []
            conf_threshold = 0.5
            nms_threshold = 0.4

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * Width)
                        center_y = int(detection[1] * Height)
                        w = int(detection[2] * Width)
                        h = int(detection[3] * Height)
                        x = center_x - w / 2
                        y = center_y - h / 2
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])

            indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

            for i in indices:
                i = i[0]
                box = boxes[i]
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
            frame = image

            return frame

                # cv2.imshow("object detection", frame)
                # cv2.waitKey(1)
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