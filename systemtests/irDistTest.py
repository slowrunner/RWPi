#!/usr/bin/python
#
# irDist.py   IR DISTANCE SENSOR OBJECT
#
# At 12" -   7 readings = 3% uncertainty (0.4), 75 readings = 1% (0.1 inch)
# At 48" - 150 readings = 3% uncertainty (1.4), 75 readings = 6% (3.0 inches)
import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import myPDALib
import myPyLib
import time
import traceback
import irDistance


# ### TEST MAIN() ######################


def main():

  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler
  try:
    print "\nIR DISTANCE TEST"
    while True:
       print "ir sensor distance: %.1f inches" % irDistance.inInches()
       time.sleep(1)

    
  except SystemExit:
    myPDALib.PiExit()
    print "IR DISTANCE TEST: Bye Bye"    

  except:
    print "Exception Raised"
    traceback.print_exc()  



if __name__ == "__main__":
    main()

