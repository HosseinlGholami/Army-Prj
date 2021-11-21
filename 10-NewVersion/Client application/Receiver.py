import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
import cv2
import pika
import numpy as np
import time 
import redis
import json
import requests

from ui.ReceiveUI import Ui_MainWindow  as UI_MainWindow

# USERNAME=sys.argv[1]
# PASSWORD=sys.argv[2]
# EXCHANGE_NAME= sys.argv[3]

CAM_NAME='c1'

REDIS_USER="new_guest"
REDIS_PASS="1234"
REDIS_PORT=6379

INPUT_EXCAHNGE= 'ex_'+CAM_NAME

USER_ACCESS_LEVEL=1

RABBIT_USERNAME='guest'
RABBIT_PASSWORD='guest'
SERVER_ADDRESS='localhost'
RABBIT_PORT=5672
RABBIT_VHOST='/'

def delete_queue(host, port, user, passwd,queue_name):
    API_ENDPOINT = f"http://{host}:1{port}/api/queues/%2f/{queue_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    
    # data to be sent to api
    pdata = {'if-unused':False,'if-empty':False}
    # sending post request and saving response as response object
    r = requests.delete(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        err=r.json()
        if err['error']=='Object Not Found':
            return True
        else:
            return False
    except:
        return True
def decoding_size(x):
    return x*8

class frame_Signals(QWidget):
    change_pixmap_signal = pyqtSignal(np.ndarray)
class metadata_Signals(QWidget):
    change_pixmap_signal = pyqtSignal(np.ndarray)

class Rbmq(QThread):
    def __init__(self,Signal,Channel,exchange_name,queue_name,dispatch):
        super(Rbmq, self).__init__()
        self.signal=Signal
        self.channel = Channel
        self.channel.basic_qos(prefetch_count=1)
        self.exchange=exchange_name
        result=self.channel.queue_declare(queue=queue_name, durable=False, exclusive=False)
        self.channel.queue_bind(exchange=self.exchange,
                        queue=queue_name,routing_key='')
        
        self.channel.basic_consume(queue=queue_name,
                      on_message_callback=
                      lambda ch, method, properties, body:
                          dispatch(
                              ch, method, properties, body,self.signal
                              ),
                          auto_ack=True
                        )
    def run(self):
        self.channel.start_consuming()
        
class RunDesignerGUI():
    def __init__(self):
        processor_handel=dict()
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        
        self.ui = UI_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.widget_action()
        self.control_server_and_signals()
                
        self.MainWindow.show()
        sys.exit(app.exec_())
    
    def widget_action(self):
        self.ui.Active_Button.clicked.connect(self.active_process)
        self.ui.Refresh_Button.clicked.connect(self.refresh)
    
    def active_process(self):
        # self.frame_rbmq_thread.setTerminationEnabled()
        # self.frame_rbmq_thread.terminate()
        # self.frame_rbmq_thread=Rbmq(self.frame_Signal.change_pixmap_signal,
        #                             self.frame_channel,
        #                             INPUT_EXCAHNGE,
        #                             self.dispatch_frame)
        
        pass
    
    def dispatch_metadata(self, channel, method, properties, body,Signal):
        pass
    
    def refresh(self):
        models=self.Redis_client.hget(CAM_NAME,b"alg")
        if models:
            model_dict=json.loads(models)
            for alg in model_dict:
                content=model_dict[alg]
                self.processor_handel[alg]={"ex":content[0],
                                              "ac":content[1],
                                              "lv":content[2],
                                              }
                if content[1]=='T':
                    if content[2]>=USER_ACCESS_LEVEL:
                        self.ui.ModelComboBox.addItem(alg)
        #add none for disable showing process
        _index = self.ui.ModelComboBox.findText("NONE")
        if _index ==-1:
            self.ui.ModelComboBox.addItem("NONE")

    def control_server_and_signals(self):
        self.Redis_client = redis.Redis(host=SERVER_ADDRESS, port=REDIS_PORT,
                                       username=REDIS_USER,
                                       password=REDIS_PASS)        
        self.credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
        self.parameters  = pika.ConnectionParameters(SERVER_ADDRESS,
                                        RABBIT_PORT,
                                        RABBIT_VHOST,
                                        self.credentials)
        self.connection=pika.BlockingConnection(self.parameters)
        #client channels
        self.frame_channel=self.connection.channel()
        self.metadata_channel=self.connection.channel()
        #client signals
            #frame signals
        self.frame_Signal=frame_Signals()
        self.frame_Signal.change_pixmap_signal.connect(self.update_image)
            #metadata signals
        self.metadata_Signal=metadata_Signals()
        self.metadata_Signal.change_pixmap_signal.connect(self.change_process_flage)
        
        self.frame_queue_name=str(time.time())
        #prepare the threads for handeling the messege
        self.frame_rbmq_thread=Rbmq(self.frame_Signal.change_pixmap_signal,
                                    self.frame_channel,
                                    INPUT_EXCAHNGE,
                                    self.frame_queue_name,
                                    self.dispatch_frame)
        
        # # start reading rabbit packet
        self.frame_rbmq_thread.start()
        
    
    def dispatch_frame(self, channel, method, properties, body,signal):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        signal.emit(frames)

    def closeEvent(self, event):
        self.channel.stop_consuming()
        self.connection.close()
        delete_queue(SERVER_ADDRESS,RABBIT_PORT,RABBIT_USER,RABBIT_PASS,self.frame_queue_name)
        event.accept()
        
    
    def change_process_flage(self):
        pass
    
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.image_label.setPixmap(qt_img)
        
        
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.ui.image_label.width(), self.ui.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__ == "__main__":
    RunDesignerGUI()