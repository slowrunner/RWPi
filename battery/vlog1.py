#!/usr/bin/python
#
# Vlog.py   Vlog
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
import battery

import math
import currentsensor
from datetime import datetime

# ######### SET CNTL-C HANDLER #####
myPyLib.set_cntl_c_handler()

HalfV = 6  # Vbattery through 2:1 v-divider is on pin 6 (0..7) of the MCP3008
VperBit = (4.87/1024)  #4.89 gives same value as multi-meter at 4.68v

print "Logging V Readings and Values"
print "time, reading, volts"
while True:
  time_now=datetime.now()
  reading =  battery.reading(1)
  voltage_now = battery.readingToVolts(reading)
  print "%s, %d, %.2f" % (time_now, reading, voltage_now)
  time.sleep(0.1)

myPDALib.PiExit()

print "Done"

  
  

