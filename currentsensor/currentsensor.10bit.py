#!/usr/bin/python

import PDALib
import myPDALib
import myPyLib
import math
import time
import traceback

ACS712PIN = 7  # Current sensor is on pin 7 (0..7) of the MCP3008

# current_sense(10) readings:
#
# currenttest.py time.sleep(10): 0.27A multimeter, 270-279mA current_sense(10)
# Running HCSR04.py:  0.27-0.30 multimeter 270-300mA current_sense(4)  
# Running 1 servo: current_sense(4) 350-600mA with spikes 1100-1700ma
# Motors: 


def current_sense(readings=75):   
    # Sensor puts out 0.185V/A around 2.5v
    #
    #   5000mV          1A        1000A
    #  --ADC---- *   -Sensor-  *  -----  = 26.39358 mA per reading bit
    #   1024           185mV        1A                 around 512

    zero_current = 514.00  # reading at open circuit, no load
    
    # perhaps should use same mVperBit as analogtest: 4.87v/1024=25.70735
    #
    # ACS712-05 spec 1.5% reading error
    #
    # The ADC says 1.5% gain error and +/- 1 bit reading error
    # at 500ma that is 7.5mA +/-26.4mA + 7.5ma sensor error 
    # for a total error of +/-50ma
    # or readings of +20 to -18 around the zero reading.


    if (readings > 1):
      values = []
      for i in range(0,readings):
        values.append(PDALib.analogRead(ACS712PIN))
      values.sort()
      average = sum(values) / float(len(values)) # average
      current_now = (zero_current - average)*26.39358
    else:
      # current from a single analog reading
      pin_value =  PDALib.analogRead(ACS712PIN)
      current_now = (zero_current - pin_value)*26.39358
#     print("current %.0f" % current_now )
    return current_now

def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  while True:
    try:
      print("current %.0f mA" % current_sense() )
      time.sleep(0.3)
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


  

