from time import time 
import cv2 as cv
import pika
import sys
import numpy as np

EXCHANGE_NAME = sys.argv[1]
ROUTING_KEY = sys.argv[2]
CAM_IP = sys.argv[3]

# ROUTING_KEY='c.1'
# CAM_IP=0

if CAM_IP =='0':
    CAM_IP=0

def coding_time(x):
    x = round(x*10000)-128
    if x>255:
        return 255
    elif x<0:
        return 0
    else:
        return x
def coding_size(x):
    return np.uint8((x[0]/8,x[1]/8))

#IP Webcam Mobile application
cap = cv.VideoCapture(CAM_IP)#'rtsp://192.168.1.4:12525/h264_ulaw.sdp')
#Connect to Server
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                        '/',
                                        credentials)
channel=pika.BlockingConnection(parameters).channel()

i=0
if not cap.isOpened():
    print("Cannot open camera")
    exit()
else:
    period=time()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()   
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break    
        else:
            #set the dimention of each frame for converting inside reciever
            frame[0][0][0],frame[0][0][1]=size_of_frame=coding_size(frame.shape).tobytes()
            #set the packet numer of each frame for parsing inside reciever
            frame[0][0][2]=i
            #calculate the time interval between two frame and coding it on
                #the first index of the frame
            Lable=time()-period
            period=time()
            frame[0][1][0]=coding_time(Lable)
                        
            #send frame to rabbit mq to transmit it to client
            channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=frame.tobytes(),
            properties=pika.BasicProperties(delivery_mode = 1,)
            )
            
            #stop sending frame it's just the demo
            #TODO : could be implemented nicer
            i+=1
            if i==255:
                i=0
            
    cap.release()
    cv.destroyAllWindows()

