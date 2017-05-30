#!/usr/bin/python
#
# irDistRead.py   Gather readings from IR sensor to build table
#
# (channel 0 of 0..7 is Pololu IR 10-180cm=3v)
#

import myPDALib
import myPyLib
import time
import irDistance

myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 


while True:
  print "\n"
  print ( "IR Sensor reading: %d" %  irDistance.reading()  )
  time.sleep(1.0)


myPDALib.PiExit()
  
  

