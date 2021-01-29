from time import time 
import cv2 as cv
import pickle
import pika

import orjson

#IP Webcam Mobile application
cap = cv.VideoCapture('rtsp://192.168.1.4:12525/h264_ulaw.sdp')
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
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()   
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break    
        else:
            channel.basic_publish(
            exchange='e.R',
            routing_key='c.1',
            body=frame.tobytes(),
            properties=pika.BasicProperties(delivery_mode = 2,)
            )
        i+=1
        if i>100:
            channel.basic_publish(
            exchange='e.R',
            routing_key='c.1',
            body=bytes(0),
            properties=pika.BasicProperties(delivery_mode = 2,)
            )
            break
    
    cap.release()
    cv.destroyAllWindows()

