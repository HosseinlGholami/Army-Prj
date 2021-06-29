from time import time 
import cv2 as cv
import pika
import sys
###
# python sender.py PACKET_NUM CAMERA_ADDRES SERVER_USER SERVER_PASS
###
if len(sys.argv)==1:
    PACKET_NUM=10
    CAMERA_ADDRESS=0#'rtsp://192.168.1.4:12525/h264_ulaw.sdp')
    SERVER_USER='guest'
    SERVER_PASS='guest'
elif len(sys.argv)==2:
    PACKET_NUM=sys.argv[1]
    CAMERA_ADDRESS=sys.argv[2]
    SERVER_USER='guest'
    SERVER_PASS='guest'
elif len(sys.argv)==3:
    PACKET_NUM=sys.argv[1]
    CAMERA_ADDRESS=sys.argv[2]
    SERVER_USER=sys.argv[3]
    SERVER_PASS='guest'
elif len(sys.argv)==4:
    PACKET_NUM=sys.argv[1]
    CAMERA_ADDRESS=sys.argv[2]
    SERVER_USER=sys.argv[3]
    SERVER_PASS=sys.argv[4]
else:
    PACKET_NUM=0
    CAMERA_ADDRESS=0
    SERVER_USER='guest'
    SERVER_PASS='guest'
    
def coding (x):
    x = round(x*10000)-128
    if x>255:
        return 255
    elif x<0:
        return 0
    else:
        return x

#IP Webcam Mobile application
cap = cv.VideoCapture(CAMERA_ADDRESS)
#Connect to Server
credentials = pika.PlainCredentials(SERVER_USER,SERVER_PASS)
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
            routing_key='c.1',
            body=frame.tobytes(),
            properties=pika.BasicProperties(delivery_mode = 2,)
            )
        i+=1
        if PACKET_NUM!=-1:
            if i>PACKET_NUM:
                channel.basic_publish(
                exchange='e.R',
                routing_key='c.1',
                body=bytes(0),
                properties=pika.BasicProperties(delivery_mode = 2,)
                )
                break
    
    cap.release()
    cv.destroyAllWindows()