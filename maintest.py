import main
import time
import pylaserkbd
import cv2
cam = pylaserkbd.CAM(0)
corner_position = [[86, 399], [577, 421], [66, 472], [604, 470]]
while(True):
    cam.query()
    func = pylaserkbd.make_mapping_function(corner_position)
    charpts, contours = cam.retrieve()
    for charpt in charpts:
        print func(*charpt)
    '''piano_tone = []
    for charpt in charpts:
        piano_tone.append(int(14 * charpt[0] / kb_length))
    print piano_tone'''
    cam.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.close()