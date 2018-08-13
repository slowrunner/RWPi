#!/usr/bin/python
#
# motorsTest.py   MOTORS CLASS TEST
#
# METHODS:

#   motors(readingPerSec)                    # create instance and motor control thread
#   cancel()                                 # stop motors, close motor control thread
#   drive(driveSpeed)                        # ramp speed to go fwd(+) or back(-) at 0-100%
#   travel(distance.inInches, driveSpeed=MEDIUM) # go fwd(+) or back(-) a distance
#   spin(spinSpeed)                          # ramp spin speed to go ccw(+) or cw(-) at 0-100%
#   turn(Motors.DIRECTION)                   # Turn ccw(+) cw(-) to angle from 0
#   stop()                                   # come to graceful stop
#   modeToStr(mode=motorsMode)               # string version of motorsMode or passed mode constant
#   mode()                                   # returns Motors.STOPPED,DRIVE,TRAVEL,SPIN,TURN,STOP
#   halt()                                   # immediate stop
#   currentSpeed()                           # numerical speed percent +/-  0-100 of minToMove to max speed
#   speedToStr(speed=_currentSpeed)          # returns string name or str() of param or currentSpeed
#   calibrate()                              # find minFwdPwr, minBwdPwr, 
#                                            # minCCWDPwr, minCWPwr, 
#                                            # biasFwd, biasBwd
#   waitForStopped(timeout=60)               # call to wait for motion to end with timeout

# VARIABLES
#   readingsPerSec

# CONSTANTS
#
# Motors.NONE,CW360,CCW360,CW180,CCW180,CW135,CCW135,CW90,CCW90,CW45,CCW45  (TURNDIRS)
# dirToStr()     # returns string for Motor.TURNDIRS
#

import sys
# uncomment when testing from rwpilib/motors or RWPi/systemtests
sys.path.append("/home/pi/RWPi/rwpilib")

import PDALib
import myPDALib
import myPyLib
from myPyLib import sign, clamp
import time
import threading
import traceback
import datetime
import encoders
import motorsClass as mc


# ##### Motors CLASS TEST METHOD ######
# the first time through the main() while loop, the sensors may not have been read yet
#     so Motors.status() and each Motors may have a value of 8/UNKNOWN 

def main():
  # note: lowercase Motors is object, uppercase Motors is class (everywhere in code)

  motors=mc.Motors(readingsPerSec=10)  #create instance and control Motors thread


  myPyLib.set_cntl_c_handler(motors.cancel)  # Set CNTL-C handler 
  try:
    print "\n"

# ######## TEST calibrate()
#    motors.calibrate()

# ######## TEST spin()
    print "TEST SPIN"
    motors.spin(mc.Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    print "spin(SLOW)"
    motors.spin(mc.Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)


    print "spin(-FAST)"
    motors.spin(-mc.Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    print "spin(-SLOW)"
    motors.spin(-mc.Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)

# ###### TEST drive()
    print "TEST DRIVE"
    print "drive(SLOW)"
    motors.drive(mc.Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    print "drive(-SLOW)"
    motors.drive(-mc.Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)


    print "drive(MEDIUM)"
    motors.drive(mc.Motors.MEDIUM)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    print "drive(-MEDIUM)"
    motors.drive(-mc.Motors.MEDIUM)
    time.sleep(5)
    motors.stop()
    time.sleep(3)

    print "drive(FAST)"
    motors.drive(mc.Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    print "drive(-FAST)"
    motors.drive(-mc.Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)

# ####### TEST travel()
    print "TEST TRAVEL FWD 6.0 inches:", datetime.datetime.now()
    motors.travel(6.0, mc.Motors.MEDIUM)
    time.sleep(5.0)

    print "TEST TRAVEL BWD(-) 6.0 inches:", datetime.datetime.now()
    motors.travel(-6.0, mc.Motors.MEDIUM)
    time.sleep(5.0)

# ####### TEST turn()
    print "TEST TURNS"
    trn1=mc.Motors.CCW90
    trn2=mc.Motors.CW180
    trn3=mc.Motors.CCW90
    print "turn(CCW90)"
    motors.turn(trn1)
    time.sleep(5)
    print "turn(CW180)"
    motors.turn(trn2)
    time.sleep(5)
    print "turn(CCW90)"
    motors.turn(trn3)
    time.sleep(5)


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


