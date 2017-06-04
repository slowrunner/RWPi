#!/usr/bin/python
#
# motorsDist.py   MOTORS CLASS DISTANCE TEST
#
# Methods:

#   motors(readingPerSec)                    # create instance and motor control thread
#   cancel()                                 # stop motors, close motor control thread
#   drive(driveSpeed)                        # ramp speed to go fwd(+) or back(-) at 0-100%
#   travel(distance.inInches, driveSpeed)    # go fwd(+) or back(-) a distance
#   spin(spinSpeed)                          # ramp spin speed to go ccw(+) or cw(-) at 0-100%
#   turn(Motors.DIRECTION)                   # Turn ccw(+) cw(-) to angle from 0
#   stop()                                   # come to graceful stop
#   halt()                                   # immediate stop
#   calibrate()                              # find minFwdPwr, minBwdPwr, 
#                                            # minCCWDPwr, minCWPwr, 
#                                            # biasFwd, biasBwd

from motorsClass import *
import sys
sys.path.insert(0,'..')

import PDALib
import myPDALib
import myPyLib
import time
import traceback
import datetime
import encoders

motors = None  # global handle to MotorClass

def motorsDistCancel():
  global motors
  motors.cancel()
  encoders.cancel()

# ##### Motors CLASS DISTANCE TEST METHOD ######

def main():
  global motors

  encoders.init()
  encoders.enable_encoder_interrupts()

  motors=Motors(readingsPerSec=10)  #create instance and control Motors thread
  print "motors.debugLevel: %d" % motors.debugLevel
  motors.debugLevel = 1
  encoders.debugLevel = 1

  myPyLib.set_cntl_c_handler(motorsDistCancel)  # Set CNTL-C handler 
  try:
    print "\n"

   
# ####### TEST travel()
    print "TEST TRAVEL FWD 12.0 inches MEDIUM:", datetime.datetime.now()
    motors.travel(12.0, Motors.MEDIUM)
    time.sleep(5.0)

    print "TEST TRAVEL BWD(-) 6.0 inches MEDIUM:", datetime.datetime.now()
    motors.travel(-12.0, Motors.MEDIUM)
    time.sleep(5.0)

    print "TEST TRAVEL FWD 6.0 inches SLOW:", datetime.datetime.now()
    motors.travel(6.0, Motors.SLOW)
    time.sleep(5.0)

    print "TEST TRAVEL BWD(-) 6.0 inches SLOW:", datetime.datetime.now()
    motors.travel(-6.0, Motors.SLOW)
    time.sleep(5.0)

    print "TEST TRAVEL FWD 18.0 inches FAST:", datetime.datetime.now()
    motors.travel(18.0, Motors.FAST)
    time.sleep(5.0)

    print "TEST TRAVEL BWD(-) 18.0 inches FAST:", datetime.datetime.now()
    motors.travel(-18.0, Motors.FAST)
    time.sleep(5.0)


   
# ###### EXIT TEST GRACEFULLY cancel()
    motors.cancel()
    
    
  except SystemExit:
    myPDALib.PiExit()
    print "MotorsClass TEST: Bye Bye"    
  except:
    print "Exception Raised"
    motors.cancel()
    traceback.print_exc()  



if __name__ == "__main__":
    main()


