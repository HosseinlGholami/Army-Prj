from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import pika

QUEUE= sys.argv[1]
# QUEUE= 'c2'

def decoding_time(x):
    return (128+x)/10000
def decoding_size(x):
    return x*8


class Signals(QWidget):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
class Rbmq(QThread):
    def __init__(self,Queue):
        super(Rbmq, self).__init__()
        self.signal=Queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=10)
        self.channel.basic_consume(queue=QUEUE,
                      on_message_callback=
                      lambda ch, method, properties, body:
                          self.dispatch(
                              ch, method, properties, body,self.signal
                              ),
                          auto_ack=True
                        )
        print('Waiting for message')
    def run(self):
        self.channel.start_consuming()
        
    def dispatch(self, channel, method, properties, body,Queue):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        self.signal.emit(frames)
        # channel.basic_ack(delivery_tag = method.delivery_tag)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        #
        self.Queue=Signals()
        #init the rabbitmq
        self.rbmq=Rbmq(self.Queue.change_pixmap_signal)
        # create the video capture thread
        self.Queue.change_pixmap_signal.connect(self.update_image)
        # start reading rabbit packet
        self.rbmq.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())