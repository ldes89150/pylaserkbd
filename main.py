#This file provide a GUI interference for using pylaserkbd module.

import cv2
import numpy as np
import time
import pylaserkbd

class configuration():
    def __init__(self):
        self.key_fire_interval=0.5#seconds
        self.camid=0
        #add configuration parameters here
        pass
    def config_CAM_parameters(self):
        pass
    def mapping_calibration(self):
        pass
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
    cam=pylaserkbd.CAM(config.camid)
    while time.sleep(config.key_fire_interval):
        """typing session"""
        pass        