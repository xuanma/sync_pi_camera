import RPi.GPIO as GPIO
import time,sys,os, io, time
from picamera import PiCamera
from signal import pause

class PtsOutput(object):
	def __init__(self, camera, video_filename, pts_filename):
		self.camera = camera
		self.video_output = io.open(video_filename, 'wb')
		self.pts_output = io.open(pts_filename, 'w')
		self.start_time = None
		
	def write(self, buf):
		self.video_output.write(buf)
		if self.camera.frame.complete and self.camera.frame.timestamp:
			if self.start_time is None:
				self.start_time = time.time()
			self.pts_output.write(u'%f\n' % (time.time() - self.start_time))
			
	def flush(self):
		self.video_output.flush()
		self.pts_output.flush()
		
	def close(self):
		self.video_output.close()
		self.pts_output.close()	

NUM = '_05'
task_name = 'cage_'
recording_time = 900
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
fps = 30


camera.resolution = (int(resolution_x),int(resolution_y))
camera.framerate = int(fps)
camera.exposure_mode='sports'
camera.shutter_speed=12000
camera.rotation = 90

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
			pts_savename = ''.join((path_for_video, video_base_name, t_str, NUM, '.txt'))
			print('Recording...')
			camera.start_recording(PtsOutput(camera, video_savename, pts_savename), format='h264')
			camera.wait_recording(recording_time)
			camera.stop_recording()
			print('Done') 
			detected_start = 0
			state = 0  
GPIO.cleanup()
