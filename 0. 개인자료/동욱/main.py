import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import numpy as np

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
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


class ShowVideo(QtCore.QObject):

    flag = 0

    video = "0001.mp4"
    weights ="yolov3-computer.weights"
    config = "yolov3-computer.cfg"
    argclasses = "yolov3-computer.txt"

    cap_video = cv2.VideoCapture(video)

    ret, image = cap_video.read()
    height, width = image.shape[:2]

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)

    

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image
        global classes
        global COLORS

        run_video = True
        
        while run_video:
            ret, image = self.cap_video.read()
            # image = cv2.resize(image, (256,256))
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)


            if self.flag:
                if int(self.cap_video.get(1) % 10 == 0):
                    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    Width = image.shape[1]
                    Height = image.shape[0]
                    print(Width, Height)
                    scale = 0.00392

                    classes = None

                    with open(ShowVideo.argclasses, 'r') as f:
                        classes = [line.strip() for line in f.readlines()]

                    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

                    net = cv2.dnn.readNet(ShowVideo.weights, ShowVideo.config)

                    blob = cv2.dnn.blobFromImage(image, scale, (512,512), (0,0,0), True, crop=False)

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
                        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
                    ###########################

                    qt_image2 = QtGui.QImage(image.data,
                                            self.width,
                                            self.height,
                                            image.strides[0],
                                            QtGui.QImage.Format_Grayscale8)

                    self.VideoSignal2.emit(qt_image2)


            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    @QtCore.pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


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

    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Canny')
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.canny)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    horizontal_layout.addWidget(image_viewer2)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())