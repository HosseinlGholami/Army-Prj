import cv2 as cv
import time

def get_object_position(frame,loc):
    # Convert into grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)   
    # Load the cascade
    face_cascade = cv.CascadeClassifier(loc+'haarcascade_frontalface_default.xml')
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)    
    face_list=list()
    for x,y,w,h in faces:
        face_list.append((x,y,x+w,y+h))
    return face_list

def test_face_detection(loc):
    # Read the input image
    img = cv.imread(loc+'test.jpg')
    faces=get_object_position(img,loc)
    
    # Draw rectangle around the faces
    for a,b,c,d in faces:
        cv.rectangle(img, (a, b), (c, d), (100, 100, 100), 3)
    cv.imshow('img', img)
    cv.waitKey()

# t1=time.time()
# test_face_detection("")
# t2=time.time()

# x=t2-t1
# print(x)