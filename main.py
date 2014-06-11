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
    cam = pylaserkbd.CAM(config.camid, config.thresh, config.dilate_iterations)
    func = pylaserkbd.make_mapping_function_kbdmode(config.corner_position)
    handler = pylaserkbd.kbd_event_handler()
    while True:
        cam.query()
        charpts, contours = cam.retrieve()
        keys=pylaserkbd.find_kbd(func,charpts)
        print keys
        handler(keys)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.close()
            break
