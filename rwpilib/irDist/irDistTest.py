#!/usr/bin/python
#
# irDistTest.py   IR DISTANCE SENSOR TEST
#
# (channel 0 of 0..7 is Pololu IR 10-180cm=3v)
#

import PDALib
import myPDALib
import myPyLib
import time
import sys
import signal
import irDistance

# ######### SET CNTL-C HANDLER #####
myPyLib.set_cntl_c_handler()


while True:
  reading  = irDistance.reading()
  print  ("irReading: %0.0f irDist: %0.1f" % (reading, irDistance.readingToInches(reading)))
  time.sleep(0.1)


myPDALib.PiExit()
  
  

