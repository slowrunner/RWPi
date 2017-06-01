#
# loopStatus.py  LOOP till LIFE DONE
# 
# The 7v2 unregulated through 2:1 divider must be connected to 
#      ADC6 (pin 6) for this test
#
# This test will loop reading the voltage on ADC6 and current (pin 7)
#      UNTIL voltage drops below 5.3v (6x0.9v - 1.5% error) 10 times,
#      then will issue a shutdown now
#
# Start this test with $ sudo python battery_life.py
#

import PDALib
import myPDALib
import time
import sys
import signal
import currentsensor
import os
import datetime
import sys
import status

def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

nLow = 0
while (battery.hoursOfLifeRemaining()>1.0):
  status()
  # end while

myPDALib.PiExit()
  
  

