import cv2 
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import numpy as np


video = "MSI.mp4"
videoFile1 ="Result.avi"
weights = "yolov3-computer.weights"
config = "yolov3-computer.cfg"
argclasses = "yolov3-computer.txt"

net = cv2.dnn.readNetFromDarknet(config, weights)


classes = None
COLORS = None


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    global classes
    global COLORS

    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


class ShowVideo(QtCore.QObject):
    flag = 0   
    
    cap_video = cv2.VideoCapture(video)

    ret, image = cap_video.read()
    image = cv2.resize(image, (512,512))
    height, width = image.shape[:2]

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)
   
    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image
        global video, videoFile1, weights, config, argclasses,net, classes, COLORS
       
        run_video = True

        while run_video:
            ret, frame = self.cap_video.read()
            if not ret:
                break
            frame = cv2.resize(frame, (512,512))

            qt_image1 = QtGui.QImage(frame.data,
                                     self.width,
                                     self.height,
                                     frame.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)
            
        
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit)  # 25 ms
            loop.exec_()

        # if self.flag:
        #     ObjectDetection()

           



    @QtCore.pyqtSlot()
    def ObjectDetection(self):
        self.flag = 1 - self.flag
        global video, videoFile1, weights, config, argclasses,net, classes, COLORS
        vs= cv2.VideoCapture(video) # TODO: 삭제해도 될 부분??
        writer= None
        classes = None
        with open(argclasses, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


        while True:
            (ret, image) = vs.read()
            if not ret:
                break
            image = cv2.resize(image, (512, 512))
            
            height, width = image.shape[:2]
            
            
            blob = cv2.dnn.blobFromImage(image, 1/255.0,(512, 512), (0, 0, 0), crop=False)
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
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = center_x - w / 2
                        y = center_y - h / 2
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])
            idx= cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

            if len(idx) > 0:
                for i in idx:
                    i = i[0]
                    box = boxes[i]
                    x = box[0]
                    y = box[1]
                    w = box[2]
                    h = box[3]
                    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w),
                                    round(y + h))
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(videoFile1, fourcc, 30, (image.shape[1], image.shape[0]), True)
            writer.write(image)
        writer.release()
        vs.release()
        

    
    def yolo(self):
        global videoFile1
        result = cv2.VideoCapture(videoFile1)
        run_video = True

        while run_video:
            ret, frame = result.read()
            if not ret:
                break
            frame = cv2.resize(frame, (512,512))

            qt_image2 = QtGui.QImage(frame.data,
                                     self.width,
                                     self.height,
                                     frame.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal2.emit(qt_image2)


           

class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    image_viewer1 = ImageViewer()
    image_viewer2 = ImageViewer()

    vid.VideoSignal1.connect(image_viewer1.setImage)
    vid.VideoSignal2.connect(image_viewer2.setImage)

    push_button1 = QtWidgets.QPushButton('원본')
    push_button2 = QtWidgets.QPushButton('Object Detection')
    push_button3 = QtWidgets.QPushButton('yolo')
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.ObjectDetection)
    push_button3.clicked.connect(vid.yolo)


    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    horizontal_layout.addWidget(image_viewer2)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)
    vertical_layout.addWidget(push_button3)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())