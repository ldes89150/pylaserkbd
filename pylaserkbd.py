import cv2
import numpy as np
import scipy as sp

class CAM():
    def __init__(self, camid, thresh = 127, dilate_iterations = 2):
        self.camid = camid
        self.cap = cv2.VideoCapture(self.camid)
        self.img = None
        self.ret = None
        self.contours = None
        self.charpts = None
        
        # image processing parameters
        self.thresh = thresh
        self.dilate_iterations = dilate_iterations
        self.kernel = np.ones((5, 5), np.uint8)
    
    def query_from_file(self, img_path):
        '''test from stored file'''
        self.img = cv2.imread(img_path)
            
    def query(self):
        '''query an image from camera'''
        self.ret, self.img = self.cap.read()
    
    def __process(self): 
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, th = cv2.threshold(gray, self.thresh, 255, cv2.THRESH_BINARY)
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
        self.contours = contours
        self.charpts = charpts
        return charpts, contours
    def release(self):
        self.cap.release()
    def show(self):
        cv2.drawContours(self.img, self.contours, -1, (0, 255, 0), 1)
        for charpt in self.charpts:
            cv2.circle(self.img, charpt, 2, (0, 0, 255), -1)
        # Display the resulting frame
        cv2.imshow('frame',self.img)
        

class mapping():
    def __init__(self, corner_position):
        self.origin = corner_position[2]
        self.x_length = corner_position[3][0] - corner_position[2][0]
        self.y_length = corner_position[0][1] - corner_position[2][1]
        self.position = None
        pass
    def __call__(self, position):
        delta_x = position[0] - self.origin[0]
        delta_y = position[1] - self.origin[1]
        if self.x_length > delta_x and self.y_length > delta_y and delta_x > 0 and delta_y > 0:
            self.position = np.array([delta_x / self.x_length * 14., delta_y / self.y_length * 2. ])
        return self.position

def make_mapping_function(position):
    '''setup and return a mapping function object'''
    pass
