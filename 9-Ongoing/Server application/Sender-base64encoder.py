from time import time 
import cv2 as cv
import pika
import sys
import numpy as np
import base64

# EXCHANGE_NAME = sys.argv[1]
# CAM_IP = sys.argv[2]

EXCHANGE_NAME = 'c1'
CAM_IP=0

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
            encoded, frame = cv.imencode('.jpg', frame)            
            frame = base64.b64encode(frame)
            
            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key='',
                body=frame,
                properties=pika.BasicProperties(delivery_mode = 1)
            )

            
    cap.release()
    cv.destroyAllWindows()

