#!/usr/bin/python
#
# currentlog.py   currentlog
#
# 1st run: no cap     ave=346mA range=528mA range of peak 96mA
#
# 2nd run: 6.8uF cap  ave=286ma range=527mA range of peak 97mA (not well formed)
#
# 3rd run: .01uF cap  ave=336ma range=528mA range of peak 100mA
#
# 
import PDALib
import myPDALib
import myPyLib
import time

import math
import currentsensor
from datetime import datetime

# ######### SET CNTL-C HANDLER #####
myPyLib.set_cntl_c_handler()

ACS712PIN = 7  # Current sensor is on pin 7 (0..7) of the MCP3008
zero_current = 514.00  # reading at open circuit, no load

print "Logging Current Readings and Values"
print "time, reading, current"
while True:
  time_now=datetime.now()
  pin_value =  PDALib.analogRead(ACS712PIN)
  current_now = (zero_current - pin_value)*26.39358
  print "%s, %d, %.0f" % (time_now, pin_value, current_now)
  time.sleep(0.1)

myPDALib.PiExit()

print "Done"

  
  

