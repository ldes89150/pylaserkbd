import cv2

img = cv2.imread("test.jpg")
gray= cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY)
ret,th = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
#th = cv2.adaptiveThreshold(gray,255,cv2.THRESH_BINARY, cv2.THRESH_BINARY,11,2)


'''
refer to 
http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#thresholding
http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html#threshold
'''

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()