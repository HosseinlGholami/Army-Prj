import cv2 as cv
import numpy as np

def scale(img,coefficient):
    height, width, _ = img.shape
    return cv.resize(img,(int(coefficient*width), int(coefficient*height)),interpolation=cv.INTER_AREA)

def change_position_to(img,x,y):
    M = np.float32([
                 [1,0,x],
                 [0,1,y]
                 ])
    height, width, _ = img.shape
    return cv.warpAffine(img,M,(width,height))

def rotaion(img,angel):
    height, width, _ = img.shape
    M = cv.getRotationMatrix2D(((width-1)/2.0,(height-1)/2.0),angel,1)
    return cv.warpAffine(img,M,(width,height))

def affine_transformation(img,pst1,pst2):
    rows,cols,ch = img.shape
    M = cv.getAffineTransform(pst1,pst2)
    return cv.warpAffine(img,M,(cols,rows))


def Perspective_Transformation(img,pts1,x,y):
    pts2 = np.float32([[0,0],[x,0],[0,y],[x,y]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    return cv.warpPerspective(img,M,(x,y))
