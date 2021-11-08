import sys
import cv2 as cv
import redis
from minio import Minio
import psutil

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt

from ui.loginServerUI import Ui_MainWindow as loginServerUI_MainWindow
from ui.ServerUI import Ui_MainWindow  as ServerUI_MainWindow
from util import  call_rabbitmq_api_validation, create_exchange

RABBIT_PORT=15672
RABBIT_SERVER_IP='localhost'
RABBIT_SERVER_LOCAL_HOST='/'

MINIO_FOLDER_HANDEL='jangal_'
RABBIT_EXCHANGE_HANDEL='ex_'
MINIO_SERVER_ADDR='localhost:9000'
MINIO_USER_FROM_DOCKER_FILE='admin'
MINIO_PASS_FROM_DOCKER_FILE='admin1234'

REDIS_IP='localhost'
REDIS_PORT=6379

class logSignals(QObject):
    txt = pyqtSignal(str)

class RunDesignerGUI():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        app.aboutToQuit.connect(self.closeEvent)
        self.Redis_client = redis.Redis(host=REDIS_IP, port=REDIS_PORT)
        self.minioClient = Minio(MINIO_SERVER_ADDR, access_key=MINIO_USER_FROM_DOCKER_FILE, secret_key=MINIO_PASS_FROM_DOCKER_FILE, secure=False)

        self.LoginWindow = QtWidgets.QMainWindow()
        self.MainWindow = QtWidgets.QMainWindow()
        #login server UI
        self.login_ui = loginServerUI_MainWindow()
        self.login_ui.setupUi(self.LoginWindow)
        #Server main UI
        self.ui =ServerUI_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.widget_action()
        self.update_widgets()
        
        self.MainWindow.hide()
        self.LoginWindow.show()
        sys.exit(app.exec_())
        
    def widget_action(self):
        #signals
        self.log_signal=logSignals()
        self.log_signal.txt.connect(self.send_log)
    
    
    


                
    def send_log_login(self,txt):
        pre_txt=self.login_ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.login_ui.LogtextBrowser.setText(txt)
        else:
            self.login_ui.LogtextBrowser.setText(pre_txt+'\n'+txt)
    
    def send_log(self,txt):
        pre_txt=self.ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.ui.LogtextBrowser.setText(txt)
        else:
            self.ui.LogtextBrowser.setText(pre_txt+'\n'+txt)
        
    def update_widgets(self):
        self.LoginWindow.setWindowTitle("JANGAL")
        self.LoginWindow.setWindowTitle("JANGAL")
        
     
    def closeEvent(self):
        del self.Redis_client
        del self.minioClient

            

if __name__ == "__main__":
    RunDesignerGUI()    