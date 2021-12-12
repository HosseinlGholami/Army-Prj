import cv2 as cv

from Geometric_Transformations import scale
img = scale(cv.imread("Hello.jpg"),coefficient=0.5)


cv.rectangle(img, (20, 20), (300, 300), (255, 255, 0), thickness=2, lineType=cv.LINE_8)
cv.line(img, (20, 140), (380, 200), (0, 255, 0), thickness=4, lineType=cv.LINE_AA)
cv.putText(img, "this is Hossein :)))))))))))))))))))", (90, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
cv.circle(img, (200, 200), 150, (0, 0, 0), thickness=5, lineType=cv.LINE_AA)
# cv.ellipse(img, (190, 200), (100, 50), 45, 0, 360, (255, 0, 0), thickness=2, lineType=cv.LINE_AA)

cv.namedWindow('hey',cv.WINDOW_AUTOSIZE)
cv.imshow("hey", img)

k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("hey.jpg", img)
    cv.destroyAllWindows()
else:
     cv.destroyAllWindows()
