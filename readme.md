# TODO:

cv.VideoCapture(index, apiPreference) 

use apiPreference for dont decode the frame ---> should be deep on it!

---------------------------server app

* coding and decoding on client and server application--> https://www.dacast.com/blog/video-streaming-protocol/

  H264 would be used!


* define new user (on server application)

  ----------------------client app

* when logout in client application you should close the active process!

* create refresh button for being update of client application

-------===High_level====------

* read and exploit "Authentication" and "Authorization"  mechanism of RBMQ to control clients from the links blow:
  * https://www.rabbitmq.com/access-control.html

برنامه دریافت کننده اطلاعات باید بررسی کند در صورتی که اطلاعات به سرور میومد اون اکس چنج رو نمایش بده!

در برنامه سمت سرور یه دونه qprocess بیشتر نمیخایم

---------------

*test the hardware limitation and distinct the network delay effects --> then optimize it!

# Next version

**create processing layer between sender and receiver

-----------

*implement and processing scenario! 

-------------------------------

**add camera sender inside docker in to the  add_camera function 

when the esp32-cam and RTSP servers get okayed- right now I cant export the port from inside docker for receiving camera data

---> for version.3

rewrite the sender with recording scenarios 

----------------------------------------------------------

if some problem on fast framing arise :

​		 buffering frames inside the client application 