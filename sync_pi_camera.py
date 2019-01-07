import RPi.GPIO as GPIO
import time,sys,os
from picamera import PiCamera
from signal import pause
from time import sleep

NUM = '_01'
task_name = 'cage_'
camera = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

state = 0
detected_start = 0
detected_stop = 0

    
GPIO.add_event_detect(21, GPIO.RISING)
GPIO.add_event_detect(20, GPIO.RISING)
resolution_x = 1280
resolution_y = 720
fps = 60


camera.resolution = (int(resolution_x),int(resolution_y))
camera.framerate = int(fps)
camera.exposure_mode='sports'
camera.shutter_speed=12000

print('Resolution: ', camera.resolution)
print('Frame Rate: ', camera.framerate)
print('Exposure Mode: ', camera.exposure_mode)
print('Shutter Speed: ', camera.shutter_speed)
print('Waiting for signal')

day = t=list(time.localtime()[0:3])
day_str = [str(i) for i in day]
for i in range(len(day_str)):
	if day[i] < 10:
		day_str[i] = ''.join(('0', day_str[i]))
day_str = ''.join(day_str)
path_for_video = '/home/pi/Videos/'
video_base_name = ''.join((day_str, '_Greyson_'))
video_base_name = ''.join((video_base_name, task_name))

N = 0
while True:
    if GPIO.event_detected(21):
		if GPIO.input(20) == GPIO.HIGH:
			if GPIO.input(21) == GPIO.HIGH:
				N = N+1
				if N == 4:
					detected_start = 1
					N = 0
		else:
			detected_start = 0
			N = 0

    if GPIO.event_detected(20):
		if GPIO.input(21) == GPIO.HIGH:
			if GPIO.input(20) == GPIO.HIGH:
				N = N+1
				if N == 4:
					detected_stop = 1
					N = 0
		else:
			detected_stop = 0
			N = 0
			
    if state == 0:
		if detected_start == 1:
			state = 1
			t=list(time.localtime()[3:7])
			t_str = [str(i) for i in t]
			for i in range(len(t)):
				if t[i] < 10:
					t_str[i] = ''.join(('0', t_str[i]))
			
			t_str = ''.join(t_str)
			video_savename = ''.join((path_for_video, video_base_name, t_str, NUM, '.h264'))
			camera.start_preview()
			camera.start_recording(video_savename)
			
			detected_start = 0
    elif state == 1:
		if detected_stop == 1:
			state = 0
			camera.stop_recording()
			camera.stop_preview()
			detected_stop = 0
			
    print('')  
	   
GPIO.cleanup()
