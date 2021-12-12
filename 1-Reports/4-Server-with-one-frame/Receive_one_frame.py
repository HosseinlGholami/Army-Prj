import  pika
import numpy as np
import cv2 as cv
import pickle

frame = pickle.load( open( "a.p", "rb" ) )


def Packet_Handeler_callback(ch, method, properties, body):
    X=np.frombuffer(body,dtype=np.dtype('uint8'))
    frame=X.reshape(1080, 1920, 3)
    cv.imshow('frame',  frame  )    
    cv.waitKey()
    cv.destroyAllWindows()
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


