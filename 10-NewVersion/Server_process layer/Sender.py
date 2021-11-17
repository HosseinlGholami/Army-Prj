from threading import Thread
from multiprocessing import Queue
import cv2 as cv
import pika
import numpy as np
import time
import sys
import os
import  requests

ALGORITHM=sys.argv[1]
INPUT_EXCHANGE_NAME = sys.argv[2]
OUTPUT_EXCHANGE_NAME = sys.argv[3]
SERVER_USERNAME=sys.argv[4]
SERVER_PASSWORD=sys.argv[5]
SERVER_IP=sys.argv[6]
SERVER_PORT=int(sys.argv[7])
SERVER_VHOST=sys.argv[8]
FRAME_HOP=int(sys.argv[9])
# RECORD_PATH=sys.argv[10]

# ALGORITHM='face'
# INPUT_EXCHANGE_NAME = 'ex_c1'
# OUTPUT_EXCHANGE_NAME = 'ex_c1_pr'
# SERVER_USERNAME='guest'
# SERVER_PASSWORD='guest'
# SERVER_IP='localhost'
# SERVER_PORT=5672
# SERVER_VHOST='/'
# FRAME_HOP=30
RECORD_PATH=f"""..\Data\jangal_{INPUT_EXCHANGE_NAME}"""

if ALGORITHM =='face':
    from model.face.object_detection import get_object_position 
elif ALGORITHM =='eyes':
    from model.eyes.object_detection  import get_object_position 

def decoding_size(x):
    return x*8
        
def create_exchange(host,port,user,passwd,exchange_name):
        # defining the api-endpoint
    API_ENDPOINT = f"http://{host}:1{port}/api/exchanges/%2f/{exchange_name}"
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

class apply_procces(Thread):
    def __init__(self,reciever_queue):
        Thread.__init__(self)
        self.queue=reciever_queue
        credentials = pika.PlainCredentials(SERVER_USERNAME, SERVER_PASSWORD)
        parameters = pika.ConnectionParameters(SERVER_IP,
                                                SERVER_PORT,
                                                SERVER_VHOST,
                                                credentials)
        self.channel=pika.BlockingConnection(parameters).channel()
    def run(self):
        while(True):
            frame=self.queue.get(block=True)
            object_position=get_object_position(frame,'./model/'+ALGORITHM+'/')
            if object_position:
                # send by rabbitmq        
                self.channel.basic_publish(
                        exchange=OUTPUT_EXCHANGE_NAME,
                        routing_key='',
                        body=np.array(object_position).tobytes(),
                        properties=pika.BasicProperties(delivery_mode = 1)
                        )
                with open(RECORD_PATH+f"\\{ALGORITHM}.txt", "a") as myfile:
                    myfile.write(f"""{time.time()}*{str(object_position)}\r\n""")
            else:
                # send by rabbitmq        
                self.channel.basic_publish(
                        exchange=OUTPUT_EXCHANGE_NAME,
                        routing_key='',
                        body="NULL".encode(),
                        properties=pika.BasicProperties(delivery_mode = 1)
                        )
                
            # for a,b,c,d in object_position:
            #     cv.rectangle(frame, (a, b), (c, d), (255, 0, 0), 2)
            # cv.imshow('frame', frame)
            # if cv.waitKey(1) == ord('q'):
            #     print("done")


def dispatch(channel, method, properties, body,reciever_queue):
    frames=np.frombuffer(body,dtype=np.dtype('uint8'))
    frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
    if frames[0][0][2] % FRAME_HOP ==0:
        reciever_queue.put(frames)
    
def main():
    # Connect to rabbit
    credentials = pika.PlainCredentials(SERVER_USERNAME, SERVER_PASSWORD)
    parameters = pika.ConnectionParameters(SERVER_IP,
                                            SERVER_PORT,
                                            SERVER_VHOST,
                                            credentials)
    channel=pika.BlockingConnection(parameters).channel()
    channel.basic_qos(prefetch_count=5)
    result=channel.queue_declare(queue='pr_'+INPUT_EXCHANGE_NAME, durable=False, exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=INPUT_EXCHANGE_NAME,
                    queue=queue_name,routing_key='')
    create_exchange(SERVER_IP,SERVER_PORT,SERVER_USERNAME,SERVER_PASSWORD,OUTPUT_EXCHANGE_NAME)
    reciever_queue=Queue(3)
    th = apply_procces(reciever_queue)
    th.start()
    channel.basic_consume(queue=queue_name,
                  on_message_callback=
                  lambda ch, method, properties, body:
                      dispatch(
                          ch, method, properties, body,reciever_queue
                          ),
                      auto_ack=True
                    )
    channel.start_consuming()
if __name__ == '__main__':
    main()