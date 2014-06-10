import maintest
import time
import pylaserkbd
import cv2
cam = pylaserkbd.CAM(0)
corner_position = [(587, 283), (12, 278), (598, 468), (5, 474)]
corner_position_piano = [(510, 240), (118, 227), (618, 443), (66, 433)]
def find_kbd(charpts):
    kbds = []
    func = pylaserkbd.make_mapping_function_kbdmode(corner_position)
    for charpt in charpts:
        if not(func(*charpt)[0] < 0 or func(*charpt)[0] > 500 or func(*charpt)[1] > 300 or func(*charpt)[1] < 0):
            kbds.append(func(*charpt))
    for p in kbds:
        row = (5 * p[1] / 300)
        if row > 1 and row < 2:
            if p[0] < 146 and p[0] >114:
                print 'z'
            elif p[0] < 178 and p[0] >146:  
                print 'x'
            elif p[0] < 210 and p[0] >178:
                print 'c'
            elif p[0] < 242 and p[0] >210:
                print 'v'
            elif p[0] < 274 and p[0] >242:
                print 'b'
            elif p[0] < 306 and p[0] >274:
                print 'n'
            elif p[0] < 338 and p[0] >306:
                print 'm'
        else: print '(%d, %d)' %(int(p[0]), int(p[1]))
def find_tone(charpts):
    tones = []
    ps = []
    func = pylaserkbd.make_mapping_function_pianomode(corner_position_piano)
    for charpt in charpts:
        if not(func(*charpt)[0] < 0 or func(*charpt)[0] > 300 or func(*charpt)[1] > 180 or func(*charpt)[1] < 0):
            ps.append(func(*charpt))
    for p in ps:
        col = int(14 * p[0] / 300)
        raw = int(2 * p[1] / 180)
        tones.append([col, raw])
    print tones
while(True):
    cam.query()
    charpts, contours = cam.retrieve()
    find_kbd(charpts)
    cam.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.close()
