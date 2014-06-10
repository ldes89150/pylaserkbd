# -*- coding: utf-8 -*-
# This file provide a GUI interference for using pylaserkbd module.

import cv2
import numpy as np
import time
import pylaserkbd
import os
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
        self.corner_position = [(1,0),(2,0.0)]

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

    def save(self):
        # save configuration parameters to file
        fout=open('config.cfg','w')
        parameters=('key_fire_interval',
                    'camid',
                    'thresh',
                    'dilate_iterations',
                    'corner_position')
        for parameter in parameters:
            value=None
            exec("value=self.{0}".format(parameter))
            fout.write(parameter+' = '+str(value)+'\n')
        fout.close()


    def load(self):
        # save configuration parameters to file
        try:
            fin=open('config.cfg','r')
            for s in fin.readlines():
                s=s.strip('\n').split('=')
                exec('self.{0}={1}'.format(s[0],s[1]))
            fin.close()
        except Exception as err:
            print err
            # raise assertion error
            assert False,"config.cfg not found!!"

if __name__ == '__main__':
    config = configuration(1)
    config.save()
    try:
        '''try to load the configuration from file.'''
        config.load()
    except AssertionError:
        '''if there is no configuration file, start'''
	print "No existing configuration found!"
	config.config_CAM_parameters()
        config.mapping_calibration()
        config.save()
    cam = pylaserkbd.CAM(config.camid)
    while time.sleep(config.key_fire_interval):
        piano_tone = cam.make_mapping_function(config.corner_position)
        print piano_tone

