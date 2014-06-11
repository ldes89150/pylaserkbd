# -*- coding: UTF-8 -*-
# This file provide a GUI interference for using pylaserkbd module.

import cv2
import numpy as np
import time
import pylaserkbd
import os

if __name__ == '__main__':
    config = pylaserkbd.configuration(2)
    try:
        '''try to load the configuration from file.'''
        config.load()
    except AssertionError:
        #if there is no configuration file, start
        print "No existing configuration found!"
        config.config_all()
        config.save()
    #use parameters in config to setup
<<<<<<< HEAD
    cam = pylaserkbd.CAM(config.camid)
    func=pylaserkbd.make_mapping_function_kbdmode(config.corner_position)
    
    #Please finish this part, Tony
    cam = pylaserkbd.CAM(0)
    global output
    global current_his
    output = []
    current_his = [0]
    def find_kbd(charpts, output, current_his):
        kbds = []
        current = ''
        for charpt in charpts:
            if not(func(*charpt)[0] < 0 or func(*charpt)[0] > 500 or func(*charpt)[1] > 300 or func(*charpt)[1] < 0):
                kbds.append(func(*charpt))
        for p in kbds:       
            row = (5 * p[1] / 300)         
            if row > 1 and row < 2:
                if p[0] < 146 and p[0] > 114:
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
                    del output[len(output) - 1]
                    print output
            else:
                    print '(%d, %d)' % (int(p[0]), int(p[1]))    
        if current != '' and current != current_his[0] :
            current_his[0] = current
            output.append(current)        
            print len(output)    
            print output
    while(True):
        cam.query()
        charpts, contours = cam.retrieve()
        find_kbd(charpts, output, current_his)
        cam.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.close()
    ''' 
    while time.sleep(config.key_fire_interval):
        piano_tone = cam.make_mapping_function(config.corner_position)
        print piano_tone
    '''

=======
    cam = pylaserkbd.CAM(config.camid, config.thresh, config.dilate_iterations)
    func = pylaserkbd.make_mapping_function_kbdmode(config.corner_position)
    handler = pylaserkbd.kbd_event_handler_single()
    while True:
        cam.query()
        charpts, contours = cam.retrieve()
        cam.show()
        keys=pylaserkbd.find_kbd(func,charpts)
        handler(keys)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.close()
            break
>>>>>>> 95cb9abbb39438a5c722f98df77572f1fdc9f811
