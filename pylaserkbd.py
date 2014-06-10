import cv2
import numpy as np
import scipy as sp

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
    
    def mapping(self, corner_position):
        kb_high = corner_position[2][1] - corner_position[0][1]
        kb_length = corner_position[1][0] - corner_position[0][0]
        pts1 = np.float32([corner_position[0], corner_position[1], corner_position[2], corner_position[3]])
        pts2 = np.float32([[0, 0], [kb_length, 0], [0, kb_high], [kb_length, kb_high]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        self.img = cv2.warpPerspective(self.img, M, (kb_length, kb_high))
        return kb_length

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
        self.key_fire_interval = 0.5  # seconds
        self.camid = camid
        self.thresh = 127
        self.dilate_iterations = 2
        self.corner_position = [(1, 0), (2, 0.0)]

    def config_CAM_parameters(self):
        check = 'n'
        while check == 'n':
            thresh = input('Please input thresh light power:')
            dilate_iterations = input('Please input dilate interations:')
            print 'Please touch the laser keyboard.(press q to close the camera)'
            time.sleep(1)
            cam = pylaserkbd.CAM(self.camid, thresh, dilate_iterations)
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
            cam = pylaserkbd.CAM(self.camid, self.thresh, self.dilate_iterations)
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

    def save(self):
        # save configuration parameters to file
        fout = open('config.cfg', 'w')
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

    def load(self):
        # save configuration parameters to file
        try:
            fin = open('config.cfg', 'r')
            for s in fin.readlines():
                s = s.strip('\n').split('=')
                exec('self.{0}={1}'.format(s[0], s[1]))
            fin.close()
        except Exception as err:
            print err
            # raise assertion error
            assert False, "config.cfg not found!!"
