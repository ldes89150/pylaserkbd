# -*- coding: utf-8 -*-
# This file provide a GUI interference for using pylaserkbd module.

import cv2
import numpy as np
import time
import pylaserkbd
import os

if __name__ == '__main__':
    config = pylaserkbd.configuration()
    try:
        '''try to load the configuration from file.'''
        config.load('config_piano.cfg')
    except AssertionError:
        #if there is no configuration file, start
        print "No existing configuration found!"
        config.config_all()
        config.save('config_piano.cfg')
    #use parameters in config to setup
    cam = pylaserkbd.CAM(config.camid, config.thresh, config.dilate_iterations)
    while(True):
        cam.query()
        charpts, contours = cam.retrieve()
        func = pylaserkbd.make_mapping_function_pianomode(config.corner_position)
        tones = pylaserkbd.find_tone(func, charpts)
        #print tones
        cam.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.close()
