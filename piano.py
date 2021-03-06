from Arduino import Arduino
import cv2
import numpy as np
import time
import pylaserkbd
import os

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
board = Arduino('9600', port = "")
HISTORY_TONE = 0
pitch = ['Do', 'Re', 'Me', 'Fa', 'Sol', 'La', 'Si']
while(True):
    cam.query()
    charpts, contours = cam.retrieve()
    func = pylaserkbd.make_mapping_function_pianomode(config.corner_position)
    tones = pylaserkbd.find_tone(func, charpts)
    if len(tones) >= 2:
        tone = 8 - tones[1]
        board.pinMode(tone, 'OUTPUT')
        board.digitalWrite(tone, 'HIGH')
        if HISTORY_TONE != tone:
            board.digitalWrite(HISTORY_TONE, 'LOW')
            board.pinMode(HISTORY_TONE, 'INPUT')
            print pitch[tones[1]]
        HISTORY_TONE = tone
    elif HISTORY_TONE != -1:
        board.digitalWrite(HISTORY_TONE, 'LOW')
        board.pinMode(HISTORY_TONE, 'INPUT')
        print 'Stop'
        HISTORY_TONE = -1
    cam.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.close()
