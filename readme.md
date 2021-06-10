# TODO:

---------------------------server app

* make server data durable (client user information  on file with encrypted pika)

* define new user (on server application)

* delete camera function

  ----------------------client app

* when logout in client application you should close the active process!

* create refresh button for being update of client application

-------===High_level====------

* read and exploit "authentication" and "authorisation"  mechanism of RBMQ to control clients from the links blow:
  * https://www.rabbitmq.com/access-control.html



*implement and processing scenario! 

-------------------------------

*test the hardware limitation and distinct the network delay effects --> then optimize it!

# Next version

**create processing layer between sender and receiver

--------

**add camera sender inside docker in to the  add_camera function 

when the esp32-cam and RTSP servers get okayed- right now I cant export the port from inside docker for receiving camera data

---> for version.3

rewrite the sender with recording scenarios 

----------------------------------------------------------

if some problem on fast framing arise :

​		 buffering frames inside the client application