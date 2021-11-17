import  requests
from PyQt5.QtCore import QProcess
import cv2 as cv
import pickle
#=================================================================
#dummy class for developing , to test and debuge each function :)
#=================================================================
class a():
    def send_log(a,b):
        pass
self=a()
#==================================================================
#rabbit related function:
def get_active_exchange(user,passwd,host,port):    
    GET_VHOST = f"http://{host}:{port}/api/definitions"
    r = requests.get(url = GET_VHOST ,auth=(user, passwd),)
    return [ex['name'] for ex in dict(r.json())['exchanges']]
#=================
def call_rabbitmq_api_validation(host, port, user, passwd):
  url = f"http://{host}:1{port}/api/whoami"
  r = requests.get(url, auth=(user,passwd))
  return dict(r.json())
#================
def create_exchange(host,port,user,passwd,exchange_name):
        # defining the api-endpoint
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    # data to be sent to api
    pdata = {"type":"fanout",'durable': False,"auto_delete":False}
    # sending post request and saving response as response object
    r = requests.put(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        r.json()
        return False
    except :
        return True

def check_binded_exchange(host, port, user, passwd,exchange_name):
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}/bindings/source"
    # your source code here
    # sending post request and saving response as response object
    r = requests.get(url = API_ENDPOINT ,auth=(user, passwd),)
    return [person['destination'] for person in r.json()]
    

def delete_exchange(host, port, user, passwd,exchange_name):
    active_person=check_binded_exchange(host, port, user, passwd,exchange_name)
    if len(active_person)==0:
        API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}"
        # your source code here
        headers = {'content-type': 'application/json'}
        # data to be sent to api
        pdata = {'type':'fanout','if-unused':True}
        # sending post request and saving response as response object
        r = requests.delete(url = API_ENDPOINT ,auth=(user, passwd),
                          json = pdata,
                          headers=headers)
        try:
            r.json()
            return False
        except:
            return True
    else:
        return active_person
        
#=============================================================================
#---------------------------------GUI Function--------------------------------
#=============================================================================
def stop_send_cam_data(self):
    exchange_name=self.ui.CamNameComboBox.currentText()
    if exchange_name:
        process=self.Data[exchange_name][1]
        process.kill()
        self.send_log('stop send data to server')

def start_send_cam_data(self):
    exchange_name=self.ui.CamNameComboBox.currentText()
    if exchange_name:
        CAMERA_IP=self.Data[exchange_name][0]
        process=self.Data[exchange_name][1]
        process.start("python",["Sender.py",exchange_name,CAMERA_IP])
        self.send_log('start send data to server')

def delete_camera(self):
    username=self.ui.SUsername_lineEdit.text()
    password=self.ui.SPassword_lineEdit.text()
    exchange_name=self.ui.CamNameComboBox.currentText()
    if exchange_name:
        resp=delete_exchange('localhost',15672,username,password,exchange_name)
        if resp==True:
            self.send_log('exchange has deleted')
            self.ui.CamNameComboBox.removeItem(self.ui.CamNameComboBox.currentIndex())
            del self.DmData[exchange_name]
            del self.Data[exchange_name]
            with open('server.dinf', 'wb') as handle:
                pickle.dump(self.DmData, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        elif resp==False:
            self.send_log('This exchange does not exist')
        else:
            self.send_log('This exchange person are bind to this exchange:')
            for person in resp:
                self.send_log(resp)
                    
def add_camera(self):
    username=self.ui.SUsername_lineEdit.text()
    password=self.ui.SPassword_lineEdit.text()
    serverip='localhost'
    serverport=15672
    cam_ip=self.ui.CIP_lineEdit.text()
    exchange_name=self.ui.SE_lineEdit.text()
    cap = cv.VideoCapture(cam_ip)
    if not cap.isOpened():
        self.send_log("the ip of cammera is invalid")
        flag =False
    else:
        self.send_log("camera is valid")
    #free the memory
    del cap
    
    if not exchange_name in self.Data:
        #create an exchange
        create_exchange(serverip,serverport,username,password,exchange_name)        
        #save every things on data 
        self.Data.update({exchange_name:[cam_ip, QProcess()]})
        #save every things on dummy data for make data persistance
        self.DmData.update({exchange_name:[str(cam_ip),"0"]})
        with open('server.dinf', 'wb') as handle:
            pickle.dump(self.DmData, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.ui.CamNameComboBox.addItem(exchange_name)
        self.send_log("Camera added inside server")
        self.send_log("----------------------------------")
    else:
        self.send_log("This exchange already exist!")
    
def login(self):
    username=self.ui.SUsername_lineEdit.text()
    password=self.ui.SPassword_lineEdit.text()
    serverip='localhost'
    serverport=15672

    #check authoriation
    try:
        rabbit_authorization=call_rabbitmq_api_validation(serverip,serverport,username,password)
    except:
        self.send_log("rabbit is offline")
        rabbit_authorization={'error':'offline'}
    
    if 'name' in rabbit_authorization:
        #the authori
        self.restore_last_config(username,password)
        self.ui.tabWidget.setTabVisible(0,False)
        for i in range(1,4):
            self.ui.tabWidget.setTabVisible(i,True)
        self.send_log("connection to server is ok")
    else:
        self.send_log(f"rabbit_authorization failed: error --> {rabbit_authorization['error']}")
    del rabbit_authorization

def restore_last_config(self,username,password):
    with open('server.dinf', 'rb') as handle:
        readfile_list = pickle.load(handle)
    for exchange_name in readfile_list:
        self.Data.update({exchange_name:
                          [readfile_list[exchange_name][0],QProcess()]
                          })
        self.DmData.update({exchange_name:
              [readfile_list[exchange_name][0],0]
              })
        self.ui.CamNameComboBox.addItem(exchange_name)
        create_exchange('localhost',15672,username,password,exchange_name)