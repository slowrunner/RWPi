#!/usr/bin/python
#
# ULTRASONIC DISTANCE SENSOR TEST
#
# Alan McDonley 23 June 2016

import PDALib
import myPDALib
import time
import sys
import signal
import usDistance


# ################## CONTROL-C HANDLER
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  usDistance.clearEcho()
  myPDALib.PiExit()  
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)
# ##################


usDistance.init()
while 1:
      # print(readDistance2(18,22)/58)
      print( "Dist: %.2f inches" %  usDistance.inInches() )
      time.sleep(0.1)



