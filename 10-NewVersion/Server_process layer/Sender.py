from threading import Thread
from multiprocessing import Queue
import cv2 as cv
import pika
import numpy as np
import time
import sys
import os
import  requests
from minio import Minio

ALGORITHM=sys.argv[1]
INPUT_EXCHANGE_NAME = sys.argv[2]
OUTPUT_EXCHANGE_NAME = sys.argv[3]
SERVER_USERNAME=sys.argv[4]
SERVER_PASSWORD=sys.argv[5]
SERVER_IP=sys.argv[6]
SERVER_PORT=int(sys.argv[7])
FRAME_HOP=int(sys.argv[8])
MINIO_USER_FROM_DOCKER_FILE=sys.argv[9]
MINIO_PASS_FROM_DOCKER_FILE=sys.argv[10]
MINIO_SERVER=sys.argv[11]

# ALGORITHM='face'
# INPUT_EXCHANGE_NAME = 'ex_c1'
# OUTPUT_EXCHANGE_NAME = 'ex_c1_pr'
# SERVER_USERNAME='guest'
# SERVER_PASSWORD='guest'
# SERVER_IP='localhost'
# SERVER_PORT=5672

# FRAME_HOP=30
# MINIO_USER_FROM_DOCKER_FILE='admin'
# MINIO_PASS_FROM_DOCKER_FILE='admin1234'
# MINIO_SERVER='localhost:9000'


SERVER_VHOST='/'
ELEMENT_NUMBER_FOR_SAVE=30
cache_path=".\cache"

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
    
class apply_save_procces(Thread):
    def __init__(self,file_dump_queue):
        Thread.__init__(self)
        self.minioClient = Minio(MINIO_SERVER,
                                 access_key=MINIO_USER_FROM_DOCKER_FILE,
                                 secret_key=MINIO_PASS_FROM_DOCKER_FILE,
                                 secure=False)
        self.queue=file_dump_queue
    def run(self):
        buckets = self.minioClient.list_buckets()
        minio_buckets=[bucket.name.split('jangal_')[1] for bucket in buckets]
        if INPUT_EXCHANGE_NAME in minio_buckets:
            bucket_index=minio_buckets.index(INPUT_EXCHANGE_NAME)
            objects = self.minioClient.list_objects(buckets[bucket_index].name, 
                                          recursive=True)
            minio_objects=[obj.object_name for obj in objects]
            if f"{INPUT_EXCHANGE_NAME}.{ALGORITHM}.txt" in minio_objects:
                file = self.minioClient.get_object(buckets[bucket_index].name, f"{INPUT_EXCHANGE_NAME}.{ALGORITHM}.txt")
                with open(cache_path+f"\{INPUT_EXCHANGE_NAME}.{ALGORITHM}.txt", 'wb') as file_data:
                    for d in file.stream(32*1024):
                        file_data.write(d)
        save_counter=0
        while(True):
            object_position=self.queue.get(block=True)
            if save_counter<ELEMENT_NUMBER_FOR_SAVE:
                with open(cache_path+f"\{INPUT_EXCHANGE_NAME}.{ALGORITHM}.txt", "a") as myfile:
                    myfile.write(f"""{time.time()}*{str(object_position)}\r\n""")
                save_counter+=1
            else:
                save_counter=0
                print("write")
                self.minioClient.fput_object(
                    bucket_name='jangal_'+INPUT_EXCHANGE_NAME , object_name=f"{INPUT_EXCHANGE_NAME}.{ALGORITHM}.txt", file_path=cache_path+f"\{INPUT_EXCHANGE_NAME}.{ALGORITHM}.txt")    

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
        file_dump_queue=Queue()
        file_dump_thread=apply_save_procces(file_dump_queue)
        file_dump_thread.start()
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
                file_dump_queue.put(object_position)
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
    result=channel.queue_declare(queue='pr_'+INPUT_EXCHANGE_NAME, durable=False, exclusive=False)
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