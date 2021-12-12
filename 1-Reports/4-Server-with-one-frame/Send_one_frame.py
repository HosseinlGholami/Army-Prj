import  pika , pickle
import numpy as np

frame = pickle.load( open( "a.p", "rb" ) )

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                        '/',
                                        credentials)
channel=pika.BlockingConnection(parameters).channel()
channel.basic_publish(
            exchange='e.R',
            routing_key='c.1',
            body=frame.tobytes(),
            properties=pika.BasicProperties(delivery_mode = 2,)
            )
