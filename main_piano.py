# -*- coding: utf-8 -*-
# This file provide a GUI interference for using pylaserkbd module.

import cv2
import numpy as np
import time
import pylaserkbd
import os

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
    cam = pylaserkbd.CAM(config.camid)
    while(True):
        cam.query()
        charpts, contours = cam.retrieve()
        tones = []
        ps = []
        func = pylaserkbd.make_mapping_function_pianomode(config.corner_position)
        for charpt in charpts:
            if not(func(*charpt)[0] < 0 or func(*charpt)[0] > 300 or func(*charpt)[1] > 180 or func(*charpt)[1] < 0):
                ps.append(func(*charpt))
        for p in ps:
            col = int(14 * p[0] / 300)
            raw = int(2 * p[1] / 180)
            tones.append([col, raw])
        print tones
        cam.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.close()
