import sys
from PyQt5 import QtWidgets
from ServerUI import Ui_MainWindow

from PyQt5.QtCore import QProcess
import cv2 as cv
import requests,json

def get_active_exchange(user,passwd,host,port):    
    GET_VHOST = f"http://{host}:{port}/api/definitions"
    r = requests.get(url = GET_VHOST ,auth=(user, passwd),)
    return [ex['name'] for ex in dict(r.json())['exchanges']]
#=================
def call_rabbitmq_api_validation(host, port, user, passwd):
  url = 'http://%s:%s/api/whoami' % (host, port)
  r = requests.get(url, auth=(user,passwd))
  return dict(r.json())
#================
def create_exchange(host,port,user,passwd,exchange_name):
        # defining the api-endpoint
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    # data to be sent to api
    pdata = {"type":"fanout",'durable': False,"auto_delete":True}
    # sending post request and saving response as response object
    r = requests.put(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        r.json()
        return False
    except :
        return True


class RunDesignerGUI():
    def __init__(self):
        self.Data=dict()
        self.process=list()

        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.widget_action()
        self.update_widgets()

        self.MainWindow.show()
        sys.exit(app.exec_())

    def widget_action(self):
        self.ui.actionClose.setStatusTip("Exit the application")
        self.ui.actionClose.triggered.connect(self.close_GUI)
        #add camera
        self.ui.addc_Button.clicked.connect(self.add_camera)
        #send button
        self.ui.StrSenButton.clicked.connect(self.start_send_cam_data)
        self.ui.StpSenButton.clicked.connect(self.stop_send_cam_data)

    #GUI Function
    def show_camera(self):
        #we might have bug on this version since when we close the process somethings leaves here
        username=self.ui.RUsername_lineEdit.text()
        password=self.ui.RPassword_lineEdit.text()
        exchange_name=self.ui.RCamNameComboBox.currentText()
        self.process.append(QProcess())
        self.process[-1].start("python",["Receiver.py",username,password,exchange_name])
        self.send_log('show camera')
    def stop_send_cam_data(self):
        exchange_name=self.ui.CamNameComboBox.currentText()
        process=self.Data[exchange_name][1]
        process.kill()
        self.send_log('stop send data to server')
    
    def start_send_cam_data(self):
        exchange_name=self.ui.CamNameComboBox.currentText()
        CAMERA_IP=self.Data[exchange_name][0]
        process=self.Data[exchange_name][1]
        #ROUTING_KEY='heyhey'
        process.start("python",["Sender.py",exchange_name,CAMERA_IP])
        self.send_log('start send data to server')
    
    
    def add_camera(self):
        username=self.ui.SUsername_lineEdit.text()
        password=self.ui.SPassword_lineEdit.text()
        serverip='localhost'
        serverport=15672
        cam_ip=self.ui.CIP_lineEdit.text()#0#
        exchange_name=self.ui.SE_lineEdit.text()#'ex_salam'#
        self.Data.update({exchange_name:[cam_ip, QProcess()]})
        flag=True
        #check the camera
        if cam_ip=='0':
            cam_ip=0
        cap = cv.VideoCapture(cam_ip)
        if not cap.isOpened():
            self.send_log("the ip of cammera is invalid")
            flag =False
        else:
            self.send_log("camera is valid")
        #check authoriation
        try:
            rabbit_authoriation=call_rabbitmq_api_validation(serverip,serverport,username,password)
        except:
            self.send_log("rabbit is offline")
            rabbit_authoriation={'error':'offline'}
        
        if 'name' in rabbit_authoriation:
            self.send_log("connection to server is ok")
        else:
            flag=False
            self.send_log(f"rabbit_authoriation failed: error --> {rabbit_authoriation['error']}")
        #free the memory
        del cap
        del rabbit_authoriation    
        #save the item
        if flag:
            if create_exchange(serverip,serverport,username,password,exchange_name):
                self.send_log("Exchange added inside server")
                self.send_log("----------------------------------")
                self.send_log("Camera added inside server")
                self.send_log("----------------------------------")
                #should be sent to integrator tools
                self.ui.CamNameComboBox.addItem(exchange_name)
    
        else:
            self.send_log("×××××××××××××××××××××××××××××××××××")
            self.send_log("Camera cant add inside server!")
            self.send_log("×××××××××××××××××××××××××××××××××××")

    def send_log(self,txt):
        pre_txt=self.ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.ui.LogtextBrowser.setText(txt)
        else:
            self.ui.LogtextBrowser.setText(pre_txt+'\n'+txt)
    def close_GUI(self):
        self.MainWindow.close()
    def update_widgets(self):
        self.MainWindow.setWindowTitle("JANGAL")
            

if __name__ == "__main__":
    RunDesignerGUI()    