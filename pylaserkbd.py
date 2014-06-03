import cv2
import numpy as np
import scipy as sp

class CAM():
    def __init__(self, camid):
        self.camid = camid
        self.cap = cv2.VideoCapture(self.camid)
        self.img = None
        self.ret = None
        self.contour = None    
        
        # image processing parameters
        self.thresh = 127
        self.dilate_iterations = 2
        self.kernel = np.ones((5, 5), np.uint8)
    
    def query_from_file(self, img_path):
        '''test from stored file'''
        self.img = cv2.imread(img_path)
            
    def query(self):
        '''query an image from camera'''
        self.ret, self.img = self.cap.read()
    
    def __process(self): 
        grey = cv2.cvtColor(self.img, cv2.cv.CV_BGR2GRAY)
        ret, th = cv2.threshold(grey, self.thresh, 255, cv2.THRESH_BINARY)
        dila = cv2.dilate(th, self.kernel, iterations=self.dilate_iterations)
        return dila
    
    def retrieve(self):
        '''process the image and return a list contours and a list including tuples of characteristic point
        ex: [(p1x,p1y),(p2x,p2y),...(pnx,pny)],[contours]'''
        processed_img = self.__process()
        contours, hierarchy = cv2.findContours(processed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        charpts = []
        for cnt in contours:
            mt = cv2.moments(cnt)
            charpts.append((int(mt['m10'] / mt['m00']), int(mt['m01'] / mt['m00'])))
        return charpts, contours

    def show(self, charpts, contours):
        cv2.drawContours(self.img, contours, -1, (0, 255, 0), 1)
        for charpt in charpts:
            cv2.circle(self.img, charpt, 2, (0, 0, 255), -1)
        # Display the resulting frame
        cv2.imshow('frame',self.img)

class mapping():
    def __init__(self):
        '''store the mapping parameters (ex: transformation matrix)'''
        pass
    def __call__(self, px, py):
        pass

def make_mapping_function():
    '''setup and return a mapping function object, for example, 
    if we give this function enough pairs of coordinates between
     images and desktop surface.'''
    pass

