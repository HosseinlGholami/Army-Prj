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
def create_new_exchange(host, port, user, passwd,exchange_name):
    url = 'http://%s:%s/api/whoami' % (host, port)
    


#GUI Function
def show_camera(self):
    self.send_log('show camera')
def stop_record_cam_data(self):
    self.send_log('stop record cam data')

def start_record_cam_data(self):
    self.send_log('start record cam data')

def stop_send_cam_data(self):
    self.send_log('stop send data to server')

def start_send_cam_data(self):
    self.send_log('start send data to server')

def add_camera(self):
    username='guest'
    password='gue1st'
    serverip='localhost'
    serverport=15672
    cam_ip=0
    flag=True
    #check the camera
    cap = cv.VideoCapture(cam_ip)
    if not cap.isOpened():
        self.send_log("the ip of cammera is invalid")
        flag =False
    else:
        self.send_log("camera is valid")
    #check authoriation
    rabbit_authoriation=call_rabbitmq_api_validation(serverip,serverport,username,password)
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
        self.send_log("Camera added inside server")
        
    else:
        self.send_log("Camera cant add inside server!")
# add_camera(self)