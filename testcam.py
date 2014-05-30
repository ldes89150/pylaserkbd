import cv2.cv as cv
import time
import sys

camid= int(sys.argv[1])
print camid
cv.NamedWindow("camera", camid)

capture = cv.CaptureFromCAM(1)

while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("camera", img)
    if cv.WaitKey(10) == 27:
        break
