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
from util import  call_rabbitmq_api_validation, create_exchange,delete_exchange

RABBIT_PORT=15672
RABBIT_SERVER_IP='localhost'
RABBIT_SERVER_LOCAL_HOST='/'

MINIO_FOLDER_HANDEL='jangal_'
RABBIT_EXCHANGE_HANDEL='ex_'
MINIO_PORT='9000'
MINIO_SERVER_ADDR=f'localhost:{MINIO_PORT}'
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
        #loginui
        self.login_ui.login_Button.clicked.connect(self.login)
        #mainui
        #add_cam tab
        self.ui.addc_Button.clicked.connect(self.add_camera)
        #control_cam tab
        self.ui.StrSenButton.clicked.connect(self.active_camera)
        self.ui.delete_cam_Button.clicked.connect(self.delete_camera)
        self.ui.StpSenButton.clicked.connect(self.deactive_camera)
        self.ui.delete_store_cam_Button.clicked.connect(self.clear_storage)
        #add_usr tab
        self.ui.add_user_Button.clicked.connect(self.add_usr)
        #reomve user
        self.ui.rmv_user_Button.clicked.connect(self.remove_usr)
        
    def remove_usr(self):
        username=self.ui.usr_Username_lineEdit.text()
        if not (username==""):
            self.Redis_client.hdel('USR_REDIS_ACL', username)
            self.Redis_client.acl_deluser(username)
            index_ = self.ui.usr_ComboBox.findText(username)
            self.ui.usr_ComboBox.removeItem(index_)
            self.send_log('user removed successfully')
            
    def add_usr(self):
        username=self.ui.usr_Username_lineEdit.text()
        password=self.ui.usr_Password_lineEdit.text()
        access_level=self.ui.lvl_usr_ComboBox.currentText()
        self.Redis_client.hset('USR_REDIS_ACL', username , access_level)
        self.Redis_client.acl_setuser(username, enabled=True, nopass=False, passwords="+"+password,
                                   commands=["+HGETALL","+ACL","+SCAN"],categories=['+@hash'],
                                   keys=["*"])
        self.ui.usr_ComboBox.addItem(username)
        self.send_log('user added successfully')
            
    def active_camera(self):
        cam_name=self.ui.CamNameComboBox.currentText()
        if cam_name!="":
            process=self.cam_handel[cam_name]["proc"]            
            if process.state()!=2:
                cam_ip =self.cam_handel[cam_name]["ip"]
                runstr = "python3"
                args = ["Sender.py",RABBIT_EXCHANGE_HANDEL+cam_name,cam_ip,self.username,self.password]
                process.start(runstr,args)
                self.Redis_client.hset(cam_name, "ac", "T")
                self.send_log('starting send data to server')
                self.ui.CamNameComboBox_2.addItem(cam_name)
            else:
                self.send_log('its already activated')
            
    def deactive_camera(self):
        cam_name=self.ui.CamNameComboBox.currentText()
        if cam_name:
            Process=self.cam_handel[cam_name]["proc"]
            if Process.state()==2:
                Process.kill()
                self.cam_handel[cam_name]["proc"]=QProcess()
                self.Redis_client.hset(cam_name, "ac", "F")
                self.send_log('sending data to server stoped')

    def delete_camera(self):
        cam_name=self.ui.CamNameComboBox.currentText()
        if cam_name:
            Process=self.cam_handel[cam_name]["proc"]
            if Process.state()==2:
                Process.kill()
            self.Redis_client.delete(cam_name)
            del self.cam_handel[cam_name]

            _index = self.ui.CamNameComboBox.findText(cam_name)
            self.ui.CamNameComboBox.removeItem(_index)
            self.send_log('camera has removed from server but the stored data sill avail')
                
    def clear_storage(self):
        cam_name=self.ui.CamNameComboBox_2.currentText()
        try:
            pid=self.cam_handel[cam_name][3]
            if pid!=-1:
                self.send_log('please deactivate camera to remove data')
                return
            if cam_name:
                buckets = self.minioClient .list_buckets()
                index=[ i for i,bname in enumerate(buckets) if bname.name==(MINIO_FOLDER_HANDEL+RABBIT_EXCHANGE_HANDEL+cam_name)][0]
                objects = self.minioClient .list_objects(buckets[index].name,recursive=True)
                for obj in objects:
                    self.minioClient .remove_object(obj.bucket_name, obj.object_name)
                self.minioClient .remove_bucket(buckets[index].name)
                index_ = self.ui.CamNameComboBox_2.findText(cam_name)
                self.ui.CamNameComboBox_2.removeItem(index_)
                self.send_log('camera data deleted successfully')
            else:
                self.send_log('please activate camera first to records somethigns')

        except:
            if cam_name:
                buckets = self.minioClient .list_buckets()
                index=[ i for i,bname in enumerate(buckets) if bname.name==(MINIO_FOLDER_HANDEL+RABBIT_EXCHANGE_HANDEL+cam_name)][0]
                objects = self.minioClient .list_objects(buckets[index].name,recursive=True)
                for obj in objects:
                    self.minioClient .remove_object(obj.bucket_name, obj.object_name)
                self.minioClient .remove_bucket(buckets[index].name)
                index_ = self.ui.CamNameComboBox_2.findText(cam_name)
                self.ui.CamNameComboBox_2.removeItem(index_)
                self.send_log('camera data deleted successfully')
            else:
                self.send_log('please activate camera first to records somethigns')

    def add_camera(self):
        cam_name=self.ui.SE_lineEdit.text()
        if not( cam_name in self.cam_handel):
            self.cam_handel.update({cam_name:''})
            self.send_log('''camera name is valid''')
        else:
            self.send_log('''please change your camera name, camera name must be unique.''')
            return
        cam_ip=self.ui.CIP_lineEdit.text()
        if cam_ip=='0':
            cam_ip=0
        cap = cv.VideoCapture(cam_ip)
        if cam_ip==0:
            cam_ip='0'
        if not cap.isOpened():
            self.send_log("the ip of cammera is invalid")
            return
        else:
            self.send_log("camera is valid")
        #free the memory
        del cap
        #get level of access
        camera_access_level=self.ui.CamNameComboBox_3.currentText()
        if create_exchange(RABBIT_SERVER_IP,RABBIT_PORT,self.username,self.password,"ex_"+cam_name):
            pid=-1
            #save every things on data
            self.cam_handel[cam_name]={
                    "proc":QProcess(),
                    "ip":cam_ip,
                    "level":camera_access_level
                }
            self.ui.CamNameComboBox.addItem(cam_name)
            self.send_log("camera added inside server successfully")
            self.send_log("--------------------------------------")
            self.Redis_client.hset(cam_name, "ex", "ex_"+cam_name)
            self.Redis_client.hset(cam_name, "lv", camera_access_level)
            self.Redis_client.hset(cam_name, "mn", "jangal_"+cam_name)
            self.Redis_client.hset(cam_name, "ip", cam_ip)
            self.Redis_client.hset(cam_name, "ac", "F")
        else:
            self.send_log("camera is valid")

    
    def login(self):
        self.username=self.login_ui.Username_lineEdit.text()
        self.password=self.login_ui.Password_lineEdit.text()
        #check authoriation
        try:
            login_status=call_rabbitmq_api_validation(RABBIT_SERVER_IP,RABBIT_PORT,self.username,self.password)
        except:
            login_status={'error':'offline'}
        if 'tags' in login_status:
            self.LoginWindow.hide()
            self.MainWindow.show()
            self.send_log(f'''you are authorized as {login_status['tags'][0]}''')
            self.update_storage_for_deleting()
            self.update_camera_list()
            self.fill_rabbit_minio_pass_inside_redis()
        else:
            self.send_log_login(f"""authorizatoin fail -->{login_status['error']} """)
    def fill_rabbit_minio_pass_inside_redis(self):
        self.Redis_client.hset("DEF_RABBIT", "usr", self.username)
        self.Redis_client.hset("DEF_RABBIT", "psw", self.password)
        self.Redis_client.hset("DEF_RABBIT", "prt", RABBIT_PORT)
        

        self.Redis_client.hset("DEF_MINIO", "usr", MINIO_USER_FROM_DOCKER_FILE)
        self.Redis_client.hset("DEF_MINIO", "psw", MINIO_PASS_FROM_DOCKER_FILE)
        self.Redis_client.hset("DEF_MINIO", "prt", MINIO_PORT)

    def update_storage_for_deleting(self):
        buckets = self.minioClient.list_buckets()
        for bucket in buckets:
            cam_name=bucket.name.split(MINIO_FOLDER_HANDEL+RABBIT_EXCHANGE_HANDEL)[1]
            self.ui.CamNameComboBox_2.addItem(cam_name)
    
    def update_camera_list(self):
        for key in self.Redis_client.scan_iter():
            if not("DEF_" in key.decode()) and not("USR_" in key.decode()):
                old_defined_camera=self.Redis_client.hgetall(key)
                self.cam_handel[key.decode()]={
                    "proc":QProcess(),
                    "ip":old_defined_camera[b'ip'].decode(),
                    "level":old_defined_camera[b'lv'].decode()
                }
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
        for cam_name in self.cam_handel:
            process=self.cam_handel[cam_name]["proc"]
            if process.state()==2:
                process.kill()
                try:
                    self.Redis_client.hset(cam_name, "ac", "F")
                except:
                    pass
        del self.cam_handel
        del self.Redis_client
        del self.minioClient


if __name__ == "__main__":
    RunDesignerGUI()    