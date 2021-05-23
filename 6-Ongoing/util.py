from PyQt5.QtCore import QProcess
import pika
import cv2 as cv

#=================================================================
#dummy class for developing , to test and debuge each function :)
#=================================================================
class a():
    def send_log(a,b):
        pass
self=a()
#==================================================================

x=1

def show_camera(self):
    self.send_log('show camera')
    print(x)
def stop_record_cam_data(self):
    self.send_log('stop record cam data')

def start_record_cam_data(self):
    self.send_log('start record cam data')

def stop_send_cam_data(self):
    self.send_log('stop send data to server')

def start_send_cam_data(self):
    self.send_log('start send data to server')

def add_camera(self):
    username='gues1'
    password='guest'
    cam_ip=1
    
    #check the camera
    cap = cv.VideoCapture(cam_ip)
    if not cap.isOpened():
        print("Cannot open camera")
        self.send_log("the ip of cammera is invalid")
    
    #check the athentication
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                        '/',
                                        credentials)
    try:
        connection = pika.BlockingConnection(parameters)
    except :
        print("the connection cant ok")
    
    # curl http api 
    # https://rawcdn.githack.com/rabbitmq/rabbitmq-server/v3.8.16/deps/rabbitmq_management/priv/www/api/index.html
    
    

    self.send_log("camera added")
    
    
add_camera(self)