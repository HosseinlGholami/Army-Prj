import  pika
import numpy as np
import cv2 as cv
from queue import Queue
import threading

Desiger_FPS=30.0
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, Desiger_FPS , (1920,1080))

class Worker(threading.Thread):
    def __init__(self, q, *args, **kwargs):
        self.q = q
        super().__init__(*args, **kwargs)
    def run(self):
        while True:
            data=self.q.get()
            if data !='a':
                out.write(data)
            else:
                print('save kardam')
                out.release()
            # do whatever work you have to do on work
            self.q.task_done()

q = Queue()
Worker(q).start()


def Packet_Handeler_callback(ch, method, properties, body):
    if body:
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(1080, 1920, 3)
        q.put_nowait(frames)
    else:
        q.put_nowait('a')
    ch.basic_ack(delivery_tag = method.delivery_tag)
    


credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                        '/',
                                        credentials)
channel=pika.BlockingConnection(parameters).channel()

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='Cam1',
              on_message_callback=Packet_Handeler_callback,
              consumer_tag='1')
print(' [*] Waiting for messages')
channel.start_consuming()


