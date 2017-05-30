#!/usr/bin/python
#
# encoderDriveTest.py   
#
#
import PDALib
import myPDALib
import myPyLib
import time
import traceback
import motorsClass as motors
import encoders
import datetime as datetime
import sys





# ### TEST MAIN() ######################

m = None  # handle to MotorClass

def ctrl_c_callback():
    global m
    m.cancel()
    encoders.cancel()


def main():
  global m

  myPyLib.set_cntl_c_handler(ctrl_c_callback)  # Set CNTL-C handler 
  encoders.init()
  encoders.enable_encoder_interrupts()
  m = motors.Motors()

  try:
    print "\nENCODER DRIVE TEST"

    m.setInitialCounts()
    print "Travel Forward 24 at Medium Speed"
    m.travel(24,m.MEDIUM)   
    if (m.mode() == m.STOPPED): time.sleep(0.100)
    while (m.mode() != m.STOPPED): time.sleep(0.01)
    print "\n********************* DONE TRAVEL\n"
    encoders.printStatus()
    print "Distance Traveled: %.1f inches" % m.distanceTraveled()
    
    encoders.reset()
    time.sleep(15)

    m.setInitialCounts()
    print "Travel Backward 24 at Medium Speed"
    m.travel(-24,m.MEDIUM)   
    if (m.mode() == m.STOPPED): time.sleep(0.100)
    while (m.mode() != m.STOPPED): time.sleep(0.01)
    print "\n********************* DONE TRAVEL"
    encoders.printStatus()   
    print "Distance Traveled: %.1f inches" % m.distanceTraveled()

    m.cancel()
    encoders.cancel()

    myPDALib.PiExit()  
    sys.exit(0)
    
  except SystemExit:
    myPDALib.PiExit()
    print "ENCODER DRIVE TEST: Bye Bye"    

  except:
    print "Exception Raised"
    traceback.print_exc()  



if __name__ == "__main__":
    main()


