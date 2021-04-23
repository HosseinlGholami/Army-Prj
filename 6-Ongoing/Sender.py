from time import time 
import cv2 as cv
import pika
import sys

ROUTING_KEY = sys.argv[1]
CAM_IP = sys.argv[2]

if CAM_IP =='0':
    CAM_IP=0

print(CAM_IP)
print(type(CAM_IP))

def coding (x):
    x = round(x*10000)-128
    if x>255:
        return 255
    elif x<0:
        return 0
    else:
        return x

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
            
            Lable=time()-period
            period=time()
            frame[0][0][0]=coding(Lable)
            
            channel.basic_publish(
            exchange='e.R',
            routing_key=ROUTING_KEY,
            body=frame.tobytes(),
            properties=pika.BasicProperties(delivery_mode = 2,)
            )
        i+=1
        if i>100000:
            channel.basic_publish(
            exchange='e.R',
            routing_key=ROUTING_KEY,
            body=bytes(0),
            properties=pika.BasicProperties(delivery_mode = 2,)
            )
            break
    
    cap.release()
    cv.destroyAllWindows()

