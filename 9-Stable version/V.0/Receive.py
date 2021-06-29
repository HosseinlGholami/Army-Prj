import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
import cv2
from ReceiveUI import Ui_MainWindow
import pika
import numpy as np


QUEUE= sys.argv[1]
blF=int(sys.argv[2])
rF =int(sys.argv[3])
gF =int(sys.argv[4])
bF =int(sys.argv[5])

# QUEUE= 'Cam1'
# blF=False
# rF =False
# gF =True
# bF =False


def decoding_time(x):
    return (128+x)/10000
def decoding_size(x):
    return x*8


class Signals(QWidget):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
class Rbmq(QThread):
    def __init__(self,Queue,Channel):
        super(Rbmq, self).__init__()
        self.signal=Queue
        self.channel = Channel
        #self.channel.basic_qos(prefetch_count=10)
        self.channel.basic_consume(queue=QUEUE,
                      on_message_callback=
                      lambda ch, method, properties, body:
                          self.dispatch(
                              ch, method, properties, body,self.signal
                              ),
                          consumer_tag="ct_test",
                        #   auto_ack=True
                        )
        print('Waiting for message')
    def run(self):
        self.channel.start_consuming()
        
    def dispatch(self, channel, method, properties, body,Queue):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        self.signal.emit(frames)
        channel.basic_ack(delivery_tag = method.delivery_tag)


class RunDesignerGUI():
    def __init__(self,blF,rF,gF,bF):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        
        self.blur=blF
        self.red=rF
        self.green=gF
        self.blue=bF
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.widget_action()
        self.control_server_and_signals()
        
        
        self.MainWindow.show()
        sys.exit(app.exec_())
    def control_server_and_signals(self):
        self.credentials = pika.PlainCredentials('guest', 'guest')
        self.parameters  = pika.ConnectionParameters('localhost',
                                       5672,
                                        '/',
                                        self.credentials)
        self.connection=pika.BlockingConnection(self.parameters)
        self.channel=self.connection.channel()
        self.Queue=Signals()
        #init the rabbitmq
        self.rbmq=Rbmq(self.Queue.change_pixmap_signal,self.channel)
        # create the video capture thread
        self.Queue.change_pixmap_signal.connect(self.update_image)
        # start reading rabbit packet
        self.rbmq.start()
        
    def closeEvent(self, event):
        self.channel.stop_consuming("ct_test")
        self.connection.close()
        event.accept()
        
    def widget_action(self):
        self.ui.actionBlur_Filter.triggered.connect(self.blurF)
        self.ui.actionRed_Filter.triggered.connect(self.redF)
        self.ui.actionGreen_Filter.triggered.connect(self.greenF)
        self.ui.actionBlue_Filter.triggered.connect(self.blueF)
        
        
    def blurF(self):
        self.blur=not(self.blur)
    def redF(self):
        self.red=not(self.red)
    def greenF(self):
        self.green=not(self.green)
    def blueF(self):
        self.blue=not(self.blue)
    # @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.image_label.setPixmap(qt_img)
        
        
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
        if self.blur:
            rgb_image = cv2.blur(rgb_image,(5,5))
            print('.')
        if self.red:
            red_img  = np.full(rgb_image.shape, (255,0,0), np.uint8)
            rgb_image = cv2.addWeighted(rgb_image, 0.8, red_img, 0.2, 0)
        if self.blue:
            blue_img  = np.full(rgb_image.shape, (0,0,255), np.uint8)
            rgb_image = cv2.addWeighted(rgb_image, 0.8, blue_img, 0.2, 0)
        if self.green:
            green_img  = np.full(rgb_image.shape, (0,255,0), np.uint8)
            rgb_image = cv2.addWeighted(rgb_image, 0.8, green_img, 0.2, 0)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.ui.image_label.width(), self.ui.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__ == "__main__":
    RunDesignerGUI(blF,rF,gF,bF)