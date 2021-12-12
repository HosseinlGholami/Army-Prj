from threading import Thread
from multiprocessing import Queue
import cv2 as cv
import pika
import numpy as np
import time
import sys
import os

EXCHANGE_NAME = sys.argv[1]
CAM_IP = sys.argv[2]
SERVER_USERNAME=sys.argv[3]
SERVER_PASSWORD=sys.argv[4]

# EXCHANGE_NAME = 'ex_c1'
# CAM_IP=0#'rtsp://192.168.1.5:12525/h264_ulaw.sdp'#0#
# SERVER_USERNAME='guest'
# SERVER_PASSWORD='guest'

SERVER_IP='localhost'
SERVER_PORT=5672
SERVER_VHOST='/'
RECORD_PATH=f"../Data/jangal_{EXCHANGE_NAME}"
RECORD_FPS=30

if CAM_IP =='0':
    CAM_IP=0

def coding_size(x):
    return np.uint8((x[0]/8,x[1]/8))

class file_recorder(Thread):
    def __init__(self,file_dump_queue):
        Thread.__init__(self)
        self.queue=file_dump_queue
    def run(self):        
        one_min_counter=0
        s_flag=False
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        if not os.path.isdir(RECORD_PATH):
            os.mkdir(RECORD_PATH)
        while(True):
            frame=self.queue.get(block=True)
            if one_min_counter==0:
                if s_flag:
                    out.release()
                else:
                    s_flag=True
                name=str(time.time()).split('.')[0]
                out = cv.VideoWriter(RECORD_PATH+f'/{name}.avi', fourcc, RECORD_FPS ,
                                     (frame[0][0][1]*8, frame[0][0][0]*8 )
                                     )
                one_min_counter=10
                # print(f'{EXCHANGE_NAME}_{name}.avi')
            if frame[0][0][2]==180:
                one_min_counter-=1
            out.write(frame)
            
            # cv.imshow('frame', frame)
            # if cv.waitKey(1) == ord('q'):
            #     break

class RabbitSender(Thread):
    def __init__(self,sender_queue,channel):
        Thread.__init__(self)
        self.queue=sender_queue
        self.channel=channel
    def run(self):
        file_dump_queue=Queue()
        file_dump_thread=file_recorder(file_dump_queue)
        file_dump_thread.start()
        seq_number=1
        while(True):
            frame=self.queue.get(block=True)
            #set the dimention of each frame for converting inside reciever
            frame[0][0][0],frame[0][0][1]=coding_size(frame.shape).tobytes()
            #set the packet numer of each frame for parsing inside reciever
            frame[0][0][2]=seq_number
            file_dump_queue.put(frame)
            #send by rabbitmq        
            self.channel.basic_publish(
                    exchange=EXCHANGE_NAME,
                    routing_key='',
                    body=frame.tobytes(),
                    properties=pika.BasicProperties(delivery_mode = 1)
                    )
            if seq_number ==180: # equal to 6 sec
                seq_number=0
            seq_number+=1
def main():    
    cap = cv.VideoCapture(CAM_IP)
    if not cap.isOpened():
        sys.exit("Cannot open camera")
    #Connect to Server
    credentials = pika.PlainCredentials(SERVER_USERNAME, SERVER_PASSWORD)
    parameters = pika.ConnectionParameters(SERVER_IP,
                                           SERVER_PORT,
                                           SERVER_VHOST,
                                            credentials)
    channel=pika.BlockingConnection(parameters).channel()

    sender_queue=Queue()
    th = RabbitSender(sender_queue,channel)
    th.start()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()   
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        else:
            sender_queue.put(frame)
    time.sleep(1)
    cap.release()
    # th.stop()
    
    # th.join()
if __name__ == '__main__':
    main()