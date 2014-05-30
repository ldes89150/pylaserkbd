import cv2
import numpy as np


kernel = np.ones((5, 5), np.uint8)


img = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
dila = cv2.dilate(th, kernel, iterations=2)
contours, hierarchy = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

# retrive characterstic points
charpts = []
for cnt in contours:
    mt = cv2.moments(cnt)
    charpts.append((int(mt['m10'] / mt['m00']), int(mt['m01'] / mt['m00'])))


for charpt in charpts:
    cv2.circle(img, charpt, 2, (0, 0, 255), -1)         



# th = cv2.adaptiveThreshold(gray,255,cv2.THRESH_BINARY, cv2.THRESH_BINARY,11,2)

'''
refer to 
http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#thresholding
http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html#threshold
'''

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
