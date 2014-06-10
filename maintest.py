import copy
import time
import pylaserkbd
import cv2
cam = pylaserkbd.CAM(0)
corner_position = [(600, 300), (20, 310), (604, 464), (5, 474)]
corner_position_piano = [(510, 240), (118, 227), (618, 443), (66, 433)]
global output
global current_his
output = []
current_his = [0]
def find_kbd(charpts, output, current_his):
    kbds = []
    current = ''
    func = pylaserkbd.make_mapping_function_kbdmode(corner_position)
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
    find_kbd(charpts, output, current_his)
    cam.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.close()
