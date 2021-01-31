#https://docs.opencv.org/master/da/d6e/tutorial_py_geometric_transformations.html

import cv2 as cv
import numpy as np

img = cv.imread("Hello.jpg")

#scale
#صرفا اسکیل میکنه چند مدل انترپولیشن داره، ولی فرقش رو نفهمیدم!
def scale(img,coefficient):
    height, width, _ = img.shape
    return cv.resize(img,(int(coefficient*width), int(coefficient*height)),
                    interpolation=cv.INTER_AREA)
res2=scale(img, coefficient=0.5)

#change position
#یه ماتریس انتقال میسازی ضرب میکنی تو تصویر
def change_position_to(img,x,y):
    M = np.float32([
                 [1,0,x],
                 [0,1,y]
                 ])
    height, width, _ = img.shape
    return cv.warpAffine(img,M,(width,height))
res3=change_position_to(img,x=100, y=-300)

#Rotaion
#یه ماتریس دوران داشتیم تو الک مغ، برای دوران اون رو برمیداره ضرب میکنه تو تصویر!
def rotaion(img,angel):
    height, width, _ = img.shape
    M = cv.getRotationMatrix2D(((width-1)/2.0,(height-1)/2.0),angel,1)
    return cv.warpAffine(img,M,(width,height))
res4=rotaion(img, angel=30)


#affine transformation
#این چیز شاخ تری یه ندیده بودم ، یه ماتریس انتقال داریم که سه نقطه که به هم دیگه عمودن رو میدی، بعد 3 نقطه دیگه تو فضا رو میدی بهش که میخای روی اون مپ بشه، یه ماتریس انتقال برات میسازه ضرب میکنی دیگه
def affine_transformation(img,pst1,pst2):
    rows,cols,ch = img.shape
    M = cv.getAffineTransform(pts1,pts2)
    return cv.warpAffine(img,M,(cols,rows))
pts1 = np.float32([[0,0],[1280,0],[0,1280]])
pts2 = np.float32([[100,100],[600,0],[600,1200]])
res5=affine_transformation(img, pts1, pts2)

#Perspective Transformation
#این دیگه عاقبت ماتریس انتقال عه چهار تا نقطه میدی، بهت چهار تا نقطه میده، میتونی فوکوس کنی روش!
#مثلا تو camscanner احتمالا میاد سه نقطه رو تشخیص میده ، برعکس این تبدیل رو روش اعمال میکنه که تصویر صاف شه
#این خوراکه مسخره بازی های پروژه فعلیم هست!!!!!!!!!!!!!!!!!!!!!!!!!
#x,y= as output image
def Perspective_Transformation(img,pts1,x,y):
    pts2 = np.float32([[0,0],[x,0],[0,y],[x,y]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    return cv.warpPerspective(img,M,(x,y))
pts1 = np.float32([[516,286],[788,303],[541,656],[783,651]])
res6=Perspective_Transformation(img, pts1=pts1, x=500,y=500)


cv.imshow("hey", res6)
cv.waitKey(0)
cv.destroyAllWindows()