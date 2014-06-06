import cv2
import pylaserkbd
cam = pylaserkbd.CAM(1)
while(True):
    cam.query()
    charpts, contours = cam.retrieve()
    cam.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
