import picamera
import time
 
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)	# resolution
    camera.rotation =90
    camera.framerate = 30			# frame rate
    print ("start preview direct from GPU")
    camera.start_preview() 	# the start_preview() function 
    while(1):
        a = 1	

