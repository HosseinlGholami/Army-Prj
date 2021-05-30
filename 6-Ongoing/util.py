from PyQt5.QtCore import QProcess
import pika
import cv2 as cv
import requests,json

#=================================================================
#dummy class for developing , to test and debuge each function :)
#=================================================================
class a():
    def send_log(a,b):
        pass
self=a()
#==================================================================
# https://rawcdn.githack.com/rabbitmq/rabbitmq-server/v3.8.16/deps/rabbitmq_management/priv/www/api/index.html
    
def call_rabbitmq_api_validation(host, port, user, passwd):
  url = 'http://%s:%s/api/whoami' % (host, port)
  r = requests.get(url, auth=(user,passwd))
  return dict(r.json())
def create_exchange(host,port,user,passwd,exchange_name):
        # defining the api-endpoint
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    # data to be sent to api
    pdata = {"type":"direct"}
    # sending post request and saving response as response object
    r = requests.put(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        r.json()
        return False
    except :
        return True


#GUI Function
def show_camera(self):
    self.send_log('show camera')
def stop_record_cam_data(self):
    self.send_log('stop record cam data')

def start_record_cam_data(self):
    self.send_log('start record cam data')

def stop_send_cam_data(self):
    exchange_name=self.ui.CamNameComboBox.currentText()
    process=self.Data[exchange_name][1]
    process.kill()
    self.send_log('stop send data to server')

def start_send_cam_data(self):
    exchange_name=self.ui.CamNameComboBox.currentText()
    CAMERA_IP=self.Data[exchange_name][0]
    process=self.Data[exchange_name][1]
    ROUTING_KEY='heyhey'
    process.start("python",["Sender.py",exchange_name,ROUTING_KEY,CAMERA_IP])
    self.send_log('start send data to server')


def add_camera(self):
    username=self.ui.SUsername_lineEdit.text()#'guest'#
    password=self.ui.SPassword_lineEdit.text()#'gues1t'#
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
            self.ui.RCamNameComboBox.addItem(exchange_name)
    else:
        self.send_log("×××××××××××××××××××××××××××××××××××")
        self.send_log("Camera cant add inside server!")
        self.send_log("×××××××××××××××××××××××××××××××××××")
