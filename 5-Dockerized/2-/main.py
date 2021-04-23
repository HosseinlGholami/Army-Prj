import docker
import time
from Server import Run_Broker,create_Sender_Image,Run_sender

PORT={ 5672:5672 ,
   15672:15672 }
client = docker.from_env()
network=client.networks.create("inter_network", driver="bridge")
Queue_container = Run_Broker(client,path='./rbmq/',ports=PORT)
time.sleep(5)
image=create_Sender_Image(client,path='./Sender/',IMAGE_name='sender:v.0')
Sender_container=Run_sender(client,image,'CONTAINER_NAME',network)
