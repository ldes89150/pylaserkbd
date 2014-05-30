from cv2 import cv


def conectCAM():
    return




if __name__ == '__main__':
    capture = cv.CaptureFromCAM(0)
    cv.NamedWindow("camera",1)
    while True:
        frame = cv.QueryFrame(capture)
        #process image 
        #determine key input
        cv.ShowImage("camera", frame)