#!/usr/bin/python
#
# currentTest.py   TEST CURRENT SENSOR 
#
import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import myPDALib
import myPyLib
import time
import traceback
import currentsensor


# ### TEST MAIN() ######################


def main():

  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler
  try:
    print "\nCURRENT SENSOR TEST"
    while True:
       mA=currentsensor.current_sense(1,1)
       time.sleep(5)

    
  except SystemExit:
    myPDALib.PiExit()
    print "CURRENT SENSOR TEST: Bye Bye"    

  except:
    print "Exception Raised"
    traceback.print_exc()  



if __name__ == "__main__":
    main()

