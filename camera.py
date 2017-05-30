#!/usr/bin/python

from picamera import PiCamera
from time import sleep
from datetime import datetime

camera = PiCamera()
camera.resolution = (2592, 1944)

camera.start_preview()
sleep(5) # allow camera to set auto exposure
fname = "images/capture_"+datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
fn = camera.capture(fname)
camera.stop_preview()

