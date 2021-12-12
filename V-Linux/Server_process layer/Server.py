import sys
import redis
from minio import Minio
import os
import psutil
import json

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt

from ui.loginServerUI import Ui_MainWindow as loginServerUI_MainWindow
from ui.ServerUI import Ui_MainWindow  as ServerUI_MainWindow
from util import call_rabbitmq_api_validation , \
                 update_redis_alg,delete_exchange,delete_queue

RABBIT_PORT=15672
RABBIT_SERVER_LOCAL_HOST='/'

MINIO_FOLDER_HANDEL='jangal_'
RABBIT_EXCHANGE_HANDEL='ex_'

REDIS_IP='localhost'
REDIS_PORT=6379

models_path="./model"

class logSignals(QObject):
    txt = pyqtSignal(str)

class RunDesignerGUI():
    def __init__(self):
        self.cam_handel=dict()
        self.process_handel=dict()
        app = QtWidgets.QApplication(sys.argv)
        app.aboutToQuit.connect(self.closeEvent)
    
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
        self.ui.Refresh_Button.clicked.connect(self.refresh_list)
        #control processesig layer tab
        self.ui.StrSenButton.clicked.connect(self.active_processor_layer)
        self.ui.StpSenButton.clicked.connect(self.deactive_processor_layer)
        self.ui.delSenButton.clicked.connect(self.delete_processor_layer)

    def delete_processor_layer(self):
        processor_name=self.ui.SelectprocessComboBox.currentText()
        self.delete_processor_layer_with_input(processor_name)
        
    def delete_processor_layer_with_input(self,processor_name):
        if not processor_name=="":
            pid=self.process_handel[processor_name]['proc']['pid']
            if pid > 0:
                p = psutil.Process(pid)
                p.terminate()
                self.process_handel[processor_name]['proc']['pid']=-1
                self.process_handel[processor_name]['proc']['mp']=QProcess()
                update_redis_alg(self.Redis_client,
                                 self.process_handel[processor_name]["name"],
                                 self.process_handel[processor_name]['model'],
                                 processor_name,#exchange_name,
                                 "F",
                                 self.process_handel[processor_name]["lv"]
                                 )
                self.send_log('sending metadata to server stoped')
                delete_exchange(self.server_address,self.server_port,
                                self.server_username,self.server_password,
                                processor_name)
                delete_queue(self.server_address,self.server_port,
                                self.server_username,self.server_password,
                                "pr_"+self.process_handel[processor_name]["ex"])
            
            _index = self.ui.SelectprocessComboBox.findText(processor_name)
            self.ui.SelectprocessComboBox.removeItem(_index)
            #free the ram
            del self.process_handel[processor_name]
    
        
    def deactive_processor_layer(self):
        processor_name=self.ui.SelectprocessComboBox.currentText()
        if not processor_name=="":
            pid=self.process_handel[processor_name]['proc']['pid']
            if pid > 0:
                p = psutil.Process(pid)
                p.terminate()
                self.process_handel[processor_name]['proc']['pid']=-1
                self.process_handel[processor_name]['proc']['mp']=QProcess()
                update_redis_alg(self.Redis_client,
                                 self.process_handel[processor_name]["name"],
                                 self.process_handel[processor_name]['model'],
                                 processor_name,#exchange_name,
                                 "F",
                                 self.process_handel[processor_name]["lv"]
                                 )
                self.send_log('sending metadata to server stoped')
                delete_exchange(self.server_address,self.server_port,
                                self.server_username,self.server_password,
                                processor_name)
                delete_queue(self.server_address,self.server_port,
                                self.server_username,self.server_password,
                                "pr_"+self.process_handel[processor_name]["ex"])

    def active_processor_layer(self):
        processor_name=self.ui.SelectprocessComboBox.currentText()
        if not processor_name=="":
            pid=self.process_handel[processor_name]['proc']['pid']
            if pid == -1:
                model=self.ui.AlgComboBox.currentText()
                self.process_handel[processor_name]['model']=model
                frame_hop=self.ui.process_spinBox.value()
                runstr = "python3"
                args = ["Sender.py",
                        self.process_handel[processor_name]['model'],#algorithm
                        self.process_handel[processor_name]['ex'],#input exchange
                        processor_name,
                        self.server_username,
                        self.server_password,
                        self.server_address,
                        self.server_port,
                        str(frame_hop),
                        self.MINIO_USER_FROM_DOCKER_FILE,
                        self.MINIO_PASS_FROM_DOCKER_FILE,
                        self.MINIO_SERVER_ADDR,
                        ]
                process=self.process_handel[processor_name]['proc']['mp']
                process.setProgram(runstr)
                process.setArguments(args)
                ok, pid = process.startDetached()
                if ok:
                    self.process_handel[processor_name]['proc']['pid']=pid                    
                    #prepare data for redis and other side of connection
                    update_redis_alg(self.Redis_client,
                                     self.process_handel[processor_name]["name"],
                                     model,
                                     processor_name,#exchange_name,
                                     "T",
                                     self.process_handel[processor_name]["lv"]
                                     )
                    self.send_log('starting send meta-data to server')
            else:
                self.send_log('its already activated')
        
        
    def add_proccesing_layer(self):
        cam_name=self.ui.CamNameComboBox.currentText()
        if cam_name != "":
            processor_name=self.ui.processor_lyr_lineEdit.text()
            if not processor_name in self.process_handel:
                self.process_handel[processor_name]=self.cam_handel[cam_name]
                self.process_handel[processor_name]["name"]=cam_name
                self.process_handel[processor_name]["proc"]={"mp":QProcess(),"pid":-1}
                self.ui.SelectprocessComboBox.addItem(processor_name)
                self.send_log('''process layer added successfully''')
            else:
                self.send_log('''please change your processor name, name must be unique.''')


    def refresh_list(self):
        active_list_on_server=list()
        for key in self.Redis_client.scan_iter():
            if not("DEF_" in key.decode()) and not("USR_" in key.decode()):
                updated_camera_list=self.Redis_client.hgetall(key)
                active_list_on_server.append(key.decode())
                if not (key.decode() in self.cam_handel):
                    if updated_camera_list[b'ac']==b'T':
                        #agr camera to list nabood va active bood 
                        #biyaresh to list va combo box
                        self.cam_handel[key.decode()]={"ex":updated_camera_list[b'ex'].decode(), "lv" : int(updated_camera_list[b'lv'].decode())}
                        self.ui.CamNameComboBox.addItem(key.decode())
                else:
                    if updated_camera_list[b'ac']==b'F':
                        #agr camera to list bood va deactive shode bood
                        #1-az combobox pakesh kon
                        #2-agr process hayi active dash hazf kon
                        #3-az list pakesh kon
                        processor_layer_list=self.return_processor_layer_list(key.decode())
                        self.remove_item_while_refresh(processor_layer_list,key.decode())
        #remove deleted item
        for camera_name in [x for x in self.cam_handel]:
            if not camera_name in active_list_on_server:
                processor_layer_list=self.return_processor_layer_list(camera_name)
                self.remove_item_while_refresh(processor_layer_list,camera_name)
    
    def return_processor_layer_list(self,cam_name):
        return [processor_name for processor_name in self.process_handel if self.process_handel[processor_name]==cam_name]
    
    def remove_item_while_refresh(self,processor_layer_list,key):
        #1-az combobox pakesh kon
        _index = self.ui.CamNameComboBox.findText(key)
        self.ui.CamNameComboBox.removeItem(_index)
        #2-agr process hayi active dash hazf kon
        for processor_name  in processor_layer_list:
            self.delete_processor_layer_with_input(processor_name)
        #3-az list pakesh kon
        del self.cam_handel[key]
        
    def cam_name_combobox_changed(self,value):
        self.ui.lvl_ComboBox.clear()
        try:
            for level in range(self.cam_handel[value]["lv"],5):
                self.ui.lvl_ComboBox.addItem(str(level))
        except:
            pass
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
            self.connect_to_others_servers()
            self.update_camera_list()
            self.LoginWindow.hide()
            self.MainWindow.show()
            self.send_log(f'''you are authorized as {login_status['tags'][0]}''')
        else:
            self.send_log_login(f"""authorizatoin fail -->{login_status['error']} """)
    
    def connect_to_others_servers(self):
        self.Redis_client = redis.Redis(host=self.server_address, port=REDIS_PORT)
        minio_credentials=self.Redis_client.hgetall("DEF_MINIO")
        self.MINIO_PORT=minio_credentials[b'prt'].decode()
        self.MINIO_SERVER_ADDR=f"{self.server_address}:{self.MINIO_PORT}"
        self.MINIO_USER_FROM_DOCKER_FILE=minio_credentials[b'usr'].decode()
        self.MINIO_PASS_FROM_DOCKER_FILE=minio_credentials[b'psw'].decode()
        self.minioClient = Minio(self.MINIO_SERVER_ADDR,
                                 access_key=self.MINIO_USER_FROM_DOCKER_FILE,
                                 secret_key=self.MINIO_PASS_FROM_DOCKER_FILE,
                                 secure=False)

    def update_camera_list(self):
        for key in self.Redis_client.scan_iter():
            if not("DEF_" in key.decode()) and not("USR_" in key.decode()):
                old_defined_camera=self.Redis_client.hgetall(key)
                self.cam_handel[key.decode()]={"ex":old_defined_camera[b'ex'].decode(),"lv":int(old_defined_camera[b'lv'].decode())}
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
        algs = [f for f in os.listdir(models_path) if not os.path.isfile(os.path.join(models_path, f))]
        for alg in algs:
            self.ui.AlgComboBox.addItem(alg)
     
    def closeEvent(self):
        for processor_name in [x for x in self.process_handel]:
            pid=self.process_handel[processor_name]['proc']['pid']
            if pid > 0:
                p = psutil.Process(pid)
                p.terminate()
            self.Redis_client.hdel(self.process_handel[processor_name]["name"],"alg")
            del self.process_handel[processor_name]
        del self.process_handel
        del self.Redis_client
        del self.minioClient
            

if __name__ == "__main__":
    RunDesignerGUI()    