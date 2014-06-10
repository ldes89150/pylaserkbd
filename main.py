# -*- coding: utf-8 -*-
# This file provide a GUI interference for using pylaserkbd module.

import cv2
import numpy as np
import time
import pylaserkbd
import os

def type_char(character):
    #no implementaion now
    print character
    pass

if __name__ == '__main__':
    config = pylaserkbd.configuration(1)
    try:
        '''try to load the configuration from file.'''
        config.load()
    except AssertionError:
        #if there is no configuration file, start
        print "No existing configuration found!"
        config.config_all()
        config.save()
    #use parameters in config to setup
    cam = pylaserkbd.CAM(config.camid, config.thresh, config.dilate_iterations)
    func = pylaserkbd.make_mapping_function_kbdmode(config.corner_position)
    
    #Please finish this part, Tony
    ''' 
    while time.sleep(config.key_fire_interval):
        piano_tone = cam.make_mapping_function(config.corner_position)
        print piano_tone
    '''
