import time
import cv2 as cv
import pickle


every_frame = pickle.load( open( "frames", "rb" ) )

sampel_under_mean_time =[(x[1],i) for i,x in enumerate(every_frame) if x[1]<0.03 ]

for X in every_frame:
    cv.imshow("mamad",X[0])
    time.sleep(X[1])
    cv.waitKey(1)
cv.destroyWindow('mamad')