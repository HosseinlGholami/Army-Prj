import cv2 as cv
import  time

#TODO: optimize the eye detection independent the image!

def get_object_position(frame,loc):
    # Convert into grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)   
    # Load the cascade

    faces=cv.CascadeClassifier(loc+"face.xml")
    eyes=cv.CascadeClassifier(loc+"eye.xml")

    face=faces.detectMultiScale(gray,1.3,5)
    eye_list=list()
    for x,y,w,h in face:
        gray_face=gray[y:y+h,x:x+w]
        eye_item=eyes.detectMultiScale(gray_face,1.3,5)
        for a,b,c,d in eye_item:
            eye_list.append((x+a,y+b,x+a+c,y+b+d))
    return eye_list


def test_face_detection(loc):
    # Read the input image
    img = cv.imread(loc+'test.jpg')
    eyes=get_object_position(img,loc)
    # Draw rectangle around the eye
    for a,b,c,d in eyes:
        cv.rectangle(img,(a,b),(c,d),(100,100,100),thickness=3)
    cv.imshow('img', img)
    cv.waitKey()
    
# t1=time.time()
# aa=test_face_detection('')
# t2=time.time()

# x=t2-t1
# print(x)
