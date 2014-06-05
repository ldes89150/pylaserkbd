# -*- coding: utf-8 -*-
#This file provide a GUI interference for using pylaserkbd module.

import cv2
import numpy as np
import time
import pylaserkbd
import os

class configuration():
    def __init__(self, camid):
        self.key_fire_interval = 0.5#seconds
        self.camid = camid
        self.cam = None
        self.thresh = 127
        self.dilate_iterations = 2
        self.corner_position = np.zeros((4, 2))
    def config_CAM_parameters(self):
        check = 'n'
        while check == 'n':
            thresh = input('Please input thresh light power:')
            dilate_iterations = input('Please input dilate interations:')
            print 'Please touch the laser keyboard.(press q to close the camera)'
            time.sleep(1)
            self.cam = pylaserkbd.CAM(self.camid, thresh, dilate_iterations)
            for i in range(100):
                self.cam.query()
                charpts, contours = self.cam.retrieve()
                self.cam.show()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            self.cam.release()
            cv2.destroyAllWindows()
            check = raw_input('Are the parameters okay?(y/n):')
        self.thresh = thresh
        self.dilate_iterations = dilate_iterations
    def mapping_calibration(self):
        corner = ['左上角', '右上角', '左下角', '右下角']
        for n in range(4):
            print 'Please put your finger at', corner[n]
            os.system("pause")#press any key to continue
			#time.sleep(2)
            img = pylaserkbd.CAM(self.camid, self.thresh, self.dilate_iterations)
            img.query()
            charpts, contours = img.retrieve()
            print 'Ok, you can leave yuor finger.'
            #self.corner_position[n] = charpts
            img.release()
            #time.sleep(2)
        print 'Calibration done.'
    def save(self):
        #save configuration paraeters to file
        pass
    def load(self):
        try:
            '''try to load configuration'''
        except:
            pass
            #raise assertion error 
if __name__  == '__main__':
    config= configuration()
    try:
        config.load()
        '''try to load the configuration from file.'''
    except:
        '''if there is no configuration file, start'''
        config.config_CAM_parameters()
        config.mapping_calibration()
        config.save()
    cam = pylaserkbd.CAM(config.camid)
    while time.sleep(config.key_fire_interval):
        """typing session"""
        pass        