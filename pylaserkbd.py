# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import time
from pykeyboard import PyKeyboard

k=PyKeyboard()



class CAM():
    def __init__(self, camid, thresh=127, dilate_iterations=3):
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

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def show(self):
        cv2.drawContours(self.img, self.contours, -1, (0, 255, 0), 1)
        for charpt in self.charpts:
            cv2.circle(self.img, charpt, 2, (0, 0, 255), -1)
        # Display the resulting frame
        cv2.imshow('frame', self.img)

class mapping():
    def __init__(self):
        self.M = None

    def __call__(self, px, py):
        v = np.dot(self.M, np.array([px, py, 1]))
        return v[0] / v[2], v[1] / v[2]

def make_mapping_function_kbdmode(corner_position):
    function = mapping()
    pts1 = np.float32([corner_position[0], corner_position[1], corner_position[2], corner_position[3]])
    pts2 = np.float32([[0, 0], [500, 0], [80, 300], [420, 300]])
    function.M = cv2.getPerspectiveTransform(pts1, pts2)
    return function

def make_mapping_function_pianomode(corner_position):
    function = mapping()
    pts1 = np.float32([corner_position[0], corner_position[1], corner_position[2], corner_position[3]])
    pts2 = np.float32([[0, 0], [300, 0], [0, 180], [300, 180]])
    function.M = cv2.getPerspectiveTransform(pts1, pts2)
    return function


def pause():
    print "Press Enter to continue."
    raw_input()
    return

class configuration():
    def __init__(self, camid):
        self.camid = None
        self.thresh = None
        self.dilate_iterations = None
        self.corner_position = None

    def config_CAM_parameters(self):
        check = 'n'
        self.camid = input('Which camera do you need?(Enter [0] for PC cam, [1] for USB cam)')
        while check == 'n':
            thresh = input('Please input thresh light power:')
            dilate_iterations = input('Please input dilate interations:')
            print 'Please touch the laser keyboard.(press q to close the camera)'
            time.sleep(1)
            cam = CAM(self.camid, thresh, dilate_iterations)
            while(True):
                cam.query()
                charpts, contours = cam.retrieve()
                cam.show()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cam.close()
            check = raw_input('Are the parameters okay?(y/n):')
        self.thresh = thresh
        self.dilate_iterations = dilate_iterations

    def mapping_calibration(self):
        corner = ['左上角', '右上角', '左下角', '右下角']
        for i in range(4):
            print 'Please put your finger at', corner[i]
            raw_input('Press enter if you are ready.')
            cam = CAM(self.camid, self.thresh, self.dilate_iterations)
            while(True):
                cam.query()
                charpts, contours = cam.retrieve()
                cam.show()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cam.close()
            print 'Ok, you can leave yuor finger.'
            self.corner_position.append(charpts)
        print self.corner_position
        print 'Calibration done.'
        
    def config_all(self):
        self.config_CAM_parameters()
        self.mapping_calibration()

    def save(self, filepath = None):
        # save configuration parameters to file
        if not filepath:
            filepath = 'config.cfg'
        fout = open(filepath, 'w')
        parameters = ('key_fire_interval',
                      'camid',
                      'thresh',
                      'dilate_iterations',
                      'corner_position')
        for parameter in parameters:
            value = None
            exec("value=self.{0}".format(parameter))
            fout.write(parameter + ' = ' + str(value) + '\n')
        fout.close()

    def load(self, filepath = None):
        # save configuration parameters to file
        try:
            if not filepath:
                filepath = 'config.cfg'
            fin = open(filepath, 'r')
            for s in fin.readlines():
                s = s.strip('\n').split('=')
                exec('self.{0}={1}'.format(s[0], s[1]))
            fin.close()
        except Exception as err:
            print err
            # raise assertion error
            assert False, "File not found!!"

def find_tone(func, charpts):
    tones = [0]
    ps = []    
    for charpt in charpts:
        if not(func(*charpt)[0] < 0 or func(*charpt)[0] > 300 or func(*charpt)[1] > 180 or func(*charpt)[1] < 0):
            ps.append(func(*charpt))
    for p in ps:
        col = int(7 * p[0] / 300)
        raw = int(2 * p[1] / 180)
        tones.append(col)
    return tones


def find_kbd(func,charpts):
    outputs=[]
    kbds=[]
    current=''
    for charpt in charpts:
        if not(func(*charpt)[0] < 0 or func(*charpt)[0] > 500 or func(*charpt)[1] > 300 or func(*charpt)[1] < 0):
            kbds.append(func(*charpt))
    for p in kbds:       
        row = (5 * (p[1]-10) / 300)        
        if row < 1:
            if p[0] < 338  and p[0] > 178:
                current = ' '
        elif row > 1 and row < 2:
            if p[0] < 50 and p[0] > 0:
                current = k.shift_key
            elif p[0] < 146 and p[0] > 114:
                current = 'z'
            elif p[0] < 178 and p[0] > 146:  
                current = 'x'
            elif p[0] < 210 and p[0] > 178:
                current = 'c'
            elif p[0] < 242 and p[0] > 210:
                current = 'v'
            elif p[0] < 274 and p[0] > 242:
                current = 'b'
            elif p[0] < 306 and p[0] > 274:
                current = 'n'
            elif p[0] < 338 and p[0] > 306:
                current = 'm'
            elif p[0] < 370 and p[0] > 338:
                current = ','
            elif p[0] < 402 and p[0] > 370:
                current = '.'
            elif p[0] < 467 and p[0] > 434:
                current = '/'
        elif row > 2 and row < 3:
            if p[0] < 131 and p[0] > 100:
                current = 'a'
            elif p[0] < 162 and p[0] > 131:  
                current = 's'
            elif p[0] < 193 and p[0] > 162:
                current = 'd'
            elif p[0] < 224 and p[0] > 193:
                current = 'f'
            elif p[0] < 255 and p[0] > 224:
                current = 'g'
            elif p[0] < 286 and p[0] > 255:
                current = 'h'
            elif p[0] < 317 and p[0] > 286:
                current = 'j'
            elif p[0] < 348 and p[0] > 317:
                    current = 'k'    
            elif p[0] < 380 and p[0] > 348:
                    current = 'l'
            elif p[0] < 412 and p[0] > 380:
                    current = ';'
            elif p[0] < 470 and p[0] > 412:
                    current = k.enter_key 
        elif row > 3 and row < 4:
            if p[0] < 122 and p[0] > 90:
                current = 'q'
            elif p[0] < 154 and p[0] > 122:  
                current = 'w'
            elif p[0] < 186 and p[0] > 154:
                current = 'e'
            elif p[0] < 218 and p[0] > 186:
                current = 'r'
            elif p[0] < 250 and p[0] > 218:
                current = 't'
            elif p[0] < 282 and p[0] > 250:
                current = 'y'
            elif p[0] < 314 and p[0] > 282:
                current = 'u'
            elif p[0] < 346 and p[0] > 314:
                current = 'i'    
            elif p[0] < 378 and p[0] > 346:
                current = 'o'
            elif p[0] < 410 and p[0] > 378:
                current = 'p'
            elif p[0] < 450 and p[0] > 410:
                current = k.backspace_key
        elif row > 4 and row < 5:
            if p[0] < 108 and p[0] > 80:
                current = '1'
            elif p[0] < 136 and p[0] > 108:  
                current = '2'
            elif p[0] < 165 and p[0] > 136:
                current = '3'
            elif p[0] < 193 and p[0] > 165:
                current = '4'
            elif p[0] < 221 and p[0] > 193:
                current = '5'
            elif p[0] < 250 and p[0] > 221:
                current = '6'
            elif p[0] < 278 and p[0] > 250:
                current = '7'
            elif p[0] < 306 and p[0] > 278:
                current = '8'    
            elif p[0] < 335 and p[0] > 306:
                current = '9'
            elif p[0] < 363 and p[0] > 335:
                current = '0'
            elif p[0] < 391 and p[0] > 363:
                current = '-'
            elif p[0] < 420 and p[0] > 391:
                current = '='
        else:
            pass  
    if current != '':
        outputs.append(current)        
    return outputs

class kbd_event_handler():
    def __init__(self):
        self.state=[]
    def __call__(self,keys):
        for key in self.state:
            if key not in keys:
                k.release_key(key)
        for key in keys:
            if key not in self.state:
                k.press_key(key)
        self.state=keys

class kbd_event_handler_single(kbd_event_handler):
    def __call__(self,keys):
        for key in keys:
            if key not in self.state:
                k.tap_key(key)
        self.state=keys
    
