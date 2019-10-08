#!/usr/bin/python
#
#  currentsensor.py    API for reading current from the ACS712 sensor
#
#  Aug2018 tests show readings are generally within 60mA of the actual current
#  e.g.  idle (w pigpio daemon running)  .31-33 Amps shows 337-379mA
#        loaded w three systemtests/loadcpu_fib.py .68-.70 Amps shows 664-741mA
#
import sys
sys.path.insert(0, '/home/pi/RWPi/rwpilib')
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
refReading=2026.0 # 2019.0
refCurrent=220.0  # 280.0    # mA

# REFERENCE READING - zero
# refReading=2129.0 # 2019.0
# refCurrent=0.0  # 0.0    # mA

# REFERENCE 2 - two fibanacci and currentsensor
refReading2=1980.0 #1965.0
# refReading2=1982.0 # with zero pt 1
refCurrent2=490.0 #560.0

mAperDelta= (refCurrent2 - refCurrent) / (refReading - refReading2)

print("mAperDelta: %.2f" % mAperDelta)

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
        time.sleep(0.005)
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
      current_sense(200,1)
      time.sleep(1)
    except SystemExit:
      myPDALib.PiExit()
      print("currentsensor: Bye Bye")
      break
    except:
      print("Exception Raised")
      traceback.print_exc()
      break

if __name__ == "__main__":
    main()


  

