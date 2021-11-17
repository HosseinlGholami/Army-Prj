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
        self.cam_handel=dict()
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
        #login page
        self.login_ui.login_Button.clicked.connect(self.login)
        #main page
        self.ui.CamNameComboBox.currentTextChanged.connect(self.cam_name_combobox_changed)
        #add_proccessing_layer tab
        self.ui.addc_Button.clicked.connect(self.add_proccesing_layer)
        self.ui.Refresh_Button.clicked.connect(self.reffresh_list)
        
    def add_proccesing_layer(self):
        print("gooje")
        cam_name=self.ui.CamNameComboBox.currentText()
        processor_name=self.ui.processor_lyr_lineEdit.text()
        #TODO: define exchange on rabbit for came_name
        #TODO: add cam_name: alg:{processor_name,lvl_access}
        

    def reffresh_list(self):
        #TODO: remove all content in cam list if no process is active in the list
        print("khiyar")
        
    def cam_name_combobox_changed(self,value):
        self.ui.lvl_ComboBox.clear()
        for level in range(self.cam_handel[value][3],5):
            self.ui.lvl_ComboBox.addItem(str(level))
    
    def login(self):
        self.server_address=self.login_ui.Server_addr_lineEdit.text()
        self.server_port=self.login_ui.Server_port_lineEdit.text()
        self.server_username=self.login_ui.Server_User_lineEdit.text()
        self.server_password=self.login_ui.Server_Pass_lineEdit.text()
        #check authoriation
        try:
            login_status=call_rabbitmq_api_validation(self.server_address,self.server_port,self.server_username,self.server_password)
        except:
            login_status={'error':'offline'}
        if 'tags' in login_status:
            self.LoginWindow.hide()
            self.MainWindow.show()
            self.send_log(f'''you are authorized as {login_status['tags'][0]}''')
            self.update_camera_list()
        else:
            self.send_log_login(f"""authorizatoin fail -->{login_status['error']} """)
    
    def update_camera_list(self):
        for key in self.Redis_client.scan_iter():
            if not("DEF_" in key.decode()) and not("USR_" in key.decode()):
                old_defined_camera=self.Redis_client.hgetall(key)
                self.cam_handel[key.decode()]=[QProcess(),old_defined_camera[b'ex'].decode(),old_defined_camera[b'mn'].decode(), int(old_defined_camera[b'lv'].decode())]
                if old_defined_camera[b'ac']==b'T':
                    self.ui.CamNameComboBox.addItem(key.decode())
                    

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