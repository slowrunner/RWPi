#!/usr/bin/python
#
# analogtest.py   Pure ADC CHANNELS TEST
#
# (channel 0 of 0..7 is Pololu IR 10-180cm=3v)
# (channel 6 of 0..7 is 7v2 unreg (9v max) 2:1 divider
# (channel 7 of 0..7 is the ACS712-05 current sensor output voltage)
#

import PDALib
import myPDALib
import time
import sys
import signal

# ################ Control-C Handling #########
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# ###############




while True:
  print "\n"
  for pin in range(0,7+1):
      print ( "pin %d reading: %d voltage: %.2f" % (pin, PDALib.analogRead(pin), myPDALib.readVoltage(pin) ) )
  time.sleep(1.0)


myPDALib.PiExit()
  
  

