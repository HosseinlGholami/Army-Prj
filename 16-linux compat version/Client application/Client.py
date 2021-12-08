import sys
import redis
from minio import Minio
import os
import psutil
from PyQt5.QtCore import QProcess
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt

from ui.loginUI import Ui_MainWindow as loginUI_MainWindow
from ui.ClientUI import Ui_MainWindow  as UI_MainWindow

# from util import call_rabbitmq_api_validation , \
#                  update_redis_alg,delete_exchange,delete_queue

REDIS_PORT=6379

# MINIO_PORT
MINIO_FOLDER_HANDEL="jangal_ex_"

class Playback_process(QObject):
    def __init__(self,minio_server_address,minio_user,minio_pass):
        self.playback_app_process=QProcess()
        self.MINIO_SERVER_ADDR=minio_server_address
        self.MINIO_USER=minio_user
        self.MINIO_PASS=minio_pass
    def run_playback_process(self,cam_name):
        if not cam_name=="":
            if self.playback_app_process.state()!=2:
                runstr = "python3"
                args = ["playback.py",
                        cam_name,
                        self.MINIO_SERVER_ADDR,
                        self.MINIO_USER,
                        self.MINIO_PASS,
                        ]
                self.playback_app_process.start(runstr,args)
                self.Flage=True
                return True
            else:
                return False
        
class RunDesignerGUI():
    def __init__(self):
        self.cam_handel=dict()
        app = QtWidgets.QApplication(sys.argv)
        app.aboutToQuit.connect(self.closeEvent)
    
        self.LoginWindow = QtWidgets.QMainWindow()
        self.MainWindow = QtWidgets.QMainWindow()
        #login server UI
        self.login_ui = loginUI_MainWindow()
        self.login_ui.setupUi(self.LoginWindow)
        #Server main UI
        self.ui =UI_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.widget_action()
        self.update_widgets()
        
        self.MainWindow.hide()
        self.LoginWindow.show()
        sys.exit(app.exec_())
        
    def widget_action(self):
        #login page
        self.login_ui.login_Button.clicked.connect(self.login)
        #main page
        self.ui.Refresh_Button.clicked.connect(self.refresh)
        self.ui.showcam_Button.clicked.connect(self.show_cam)
        self.ui.playback_Button.clicked.connect(self.Run_playpack_app)
    
    def Run_playpack_app(self):
        cam_name=self.ui.playbackCamNameComboBox.currentText()
        if not cam_name=="":
            if self.playback_process.run_playback_process(cam_name):
                self.send_log('playback window runs')
            else:
                self.send_log("A playback window is already open, close that first")
    
    
        
    def show_cam(self):
        cam_name=self.ui.CamNameComboBox.currentText()
        if self.cam_handel[cam_name]['proc'].state()!=2:
            runstr = "python3"
            args = ["Receiver.py",
                    cam_name,
                    self.server_address,
                    self.server_username,
                    self.server_password,
                    str(REDIS_PORT),
                    str(self.USER_ACESS_LEVEL),
                    self.RABBIT_PORT,
                    self.RABBIT_USER,
                    self.RABBIT_PASS,
                    ]
            print(args)
            self.cam_handel[cam_name]['proc'].start(runstr,args)
            self.send_log('show camera :'+cam_name)
        else:
            self.send_log("this cam window is already open, close that first")

    def refresh(self):
        active_list_on_server=[]
        for key in self.Redis_client.scan_iter():
            if not("DEF_" in key.decode()) and not("USR_" in key.decode()):
                updated_camera_list=self.Redis_client.hgetall(key)
                #TODO:check this condition
                if int(updated_camera_list[b'lv'].decode())>=self.USER_ACESS_LEVEL:
                    active_list_on_server.append(key.decode())
                    if not (key.decode() in self.cam_handel):
                        if updated_camera_list[b'ac']==b'T':
                            #agr camera to list nabood va active bood 
                            #biyaresh to list va combo box
                            self.cam_handel[key.decode()]={"ex":updated_camera_list[b'ex'].decode(),"proc":QProcess()}    
                            self.ui.CamNameComboBox.addItem(key.decode())
                    else:
                        if updated_camera_list[b'ac']==b'F':
                            #agr camera to list bood va deactive shode bood
                            #1-az combobox pakesh kon
                            #2-agr process hayi active dash hazf kon
                            #3-az list pakesh kon
                            self.remove_item_while_refresh(key.decode())
        #remove deleted item
        for camera_name in [x for x in self.cam_handel]:
            if not camera_name in active_list_on_server:
                self.remove_item_while_refresh(camera_name)
        
        #lets handel the play back item
        self.update_storage_for_play_back()
        
    def update_storage_for_play_back(self):
        buckets = self.minioClient.list_buckets()
        for bucket in buckets:
            cam_name=bucket.name.split(MINIO_FOLDER_HANDEL)[1]
            index_ = self.ui.playbackCamNameComboBox.findText(cam_name)
            if index_ ==-1:
                self.ui.playbackCamNameComboBox.addItem(cam_name)
                        
    def remove_item_while_refresh(self,key):
        #1-az combobox pakesh kon
        _index = self.ui.CamNameComboBox.findText(key)
        self.ui.CamNameComboBox.removeItem(_index)
        #2-agr process active dash hazf kon
        try:
            self.cam_handel[key]['proc'].kill()
        except Exception as e:
            print(e)
        #3-az list pakesh kon
        del self.cam_handel[key]
    
    def login(self):
        self.server_address=self.login_ui.Server_addr_lineEdit.text()
        self.server_username=self.login_ui.Server_User_lineEdit.text()
        self.server_password=self.login_ui.Server_Pass_lineEdit.text()
        self.Redis_client = redis.Redis(host=self.server_address, port=REDIS_PORT,
                                       username=self.server_username,
                                       password=self.server_password)
        #check authoriation
        try:    
            login_status=self.Redis_client.acl_whoami()
        except:
            login_status=False
        if login_status:
            self.connect_to_others_servers()
            self.update_camera_list()
            self.LoginWindow.hide()
            self.MainWindow.show()
            self.send_log(f'''you are authorized as {login_status}''')
        else:
            self.send_log_login("authorizatoin fail")
    
    def connect_to_others_servers(self):
        minio_credentials=self.Redis_client.hgetall("DEF_MINIO")
        self.MINIO_PORT=minio_credentials[b'prt'].decode()
        self.MINIO_SERVER_ADDR=f"{self.server_address}:{self.MINIO_PORT}"
        self.MINIO_USER=minio_credentials[b'usr'].decode()
        self.MINIO_PASS=minio_credentials[b'psw'].decode()

        self.playback_process=Playback_process(self.MINIO_SERVER_ADDR,
                                               self.MINIO_USER,
                                               self.MINIO_PASS)
        self.minioClient = Minio(self.MINIO_SERVER_ADDR,
                                 access_key=self.MINIO_USER,
                                 secret_key=self.MINIO_PASS,
                                 secure=False)
        rabbit_credentials=self.Redis_client.hgetall("DEF_RABBIT")
        self.RABBIT_USER=rabbit_credentials[b'usr'].decode()
        self.RABBIT_PASS=rabbit_credentials[b'psw'].decode()
        self.RABBIT_PORT=rabbit_credentials[b'prt'].decode()[1:]
        client_redis_lvls=self.Redis_client.hgetall("USR_REDIS_ACL")
        self.USER_ACESS_LEVEL=int(client_redis_lvls[self.server_username.encode()])
        
    def update_camera_list(self):
        self.ui.user_label.setText(self.server_username)
        self.ui.lvl_label.setText(str(self.USER_ACESS_LEVEL))
        self.refresh()
    
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
        #TODO:
            #remove every things
        pass

            

if __name__ == "__main__":
    RunDesignerGUI()    