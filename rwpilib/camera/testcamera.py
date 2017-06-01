from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5) # allow camera to set auto exposure
camera.capture('capture.jpg')
camera.stop_preview()

