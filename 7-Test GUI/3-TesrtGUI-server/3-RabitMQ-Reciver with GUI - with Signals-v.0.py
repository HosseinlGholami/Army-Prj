import concurrent.futures
import logging
import queue
import threading
import time
import cv2 as cv
import  pika
import numpy as np
import sys

#QUEUE= sys.argv[1]
QUEUE='Cam1'

def decoding_time(x):
    return (128+x)/10000
def decoding_size(x):
    return x*8

def Packet_Handeler_callback(ch, method, properties, body,queue):
    frames=np.frombuffer(body,dtype=np.dtype('uint8'))
    frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
    #param that cloud use in the futures
    #frames[0][0][2]#packet number
    
    queue.put(frames)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def Viewer(queue, event):
    """Pretend we're saving a number in the database."""
    while not event.is_set() or not queue.empty():
        message = queue.get()
        cv.imshow("window",message)
        #delay time between frame
        #time.sleep(decoding_time(message[0][1][0]) )
        cv.waitKey(1)
        #logging.info(
        #    "queue size:%d", queue.qsize()
        #)
    #cv.destroyWindow('window')
    #logging.info("Consumer received event. Exiting")



#Connect to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                        '/',
                                        credentials)
channel=pika.BlockingConnection(parameters).channel()
channel.basic_qos(prefetch_count=30)
channel.basic_consume(queue=QUEUE,
                      on_message_callback=
                      lambda ch, method, properties, body:
                          Packet_Handeler_callback(
                              ch, method, properties, body,pipeline
                              ),
                     #consumer_tag='1'
                        )
#prepare Loging format for debuging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")
#Queue for Buffring the frame
pipeline = queue.Queue(maxsize=500)
#Create event for stoping threads
event = threading.Event()
#Lunch trad
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(Viewer  , pipeline, event)
    #set counsumer on the specific queue
    # try:
    #channel start consuming
    print(' [*] Waiting for messages')
    channel.start_consuming()
    # except:
    #     channel.stop_consuming()
    #     #stop the thread
    #     print('Stop Thread')
    #     event.set()