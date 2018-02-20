#!/usr/bin/python

import PDALib
import myPDALib
import myPyLib
import math
import time
import traceback

ACS712PIN = 7  # Current sensor is on pin 7 (0..7) of the MCP3008

# zero_current = 514.00  # MCP3008 10 bit reading at open circuit, no load
# mVperBit=26.39358  # MCP3008  10bit reading

#zero_current = 2047.50   # MCP3008 10 bit reading at open circuit, no load
#mVperBit=6.520806        # MCP3208  12bit reading

# REFERENCE READING - IDLE
refReading=2019.0
refCurrent=280.0    # mA

# REFERENCE 2 - two fibanacci and currentsensor
refReading2=1965.0
refCurrent2=560.0

mAperDelta= (refCurrent2 - refCurrent) / (refReading - refReading2)

print ("mAperDelta: %.2f" % mAperDelta)

# current = (refReading - reading) * mAperDelta + refCurrent

# current_sense(10) readings:
#
# 

# ###### CURRENT_SENSE(readings=75)
#
# reads current sensor directly

def current_sense(readings=75,debug=0):   



    if (readings > 1):
      values = []
      for i in range(0,readings):
        values.append(myPDALib.analogRead12bit(ACS712PIN))
      values.sort()
      pin_value = sum(values) / float(len(values)) # average
    else:
      # current from a single analog reading
      pin_value =  myPDALib.analogRead12bit(ACS712PIN)
    
    current_now = (refReading - pin_value) * mAperDelta + refCurrent
    if (debug != 0): 
        print ("reading: %d  current: %.0f mA" % (pin_value, current_now))
    return current_now

def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  while True:
    try:
      current_sense(100,1) 
      time.sleep(1)
    except SystemExit:
      myPDALib.PiExit()
      print "currentsensor: Bye Bye"   
      break 
    except:
      print "Exception Raised"
      traceback.print_exc()  
      break
  
if __name__ == "__main__":
    main()


  

