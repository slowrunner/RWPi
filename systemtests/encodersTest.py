#!/usr/bin/python
#
# encoderDriveTest.py   
#
#
import sys
sys.path.insert(0, '/home/pi/RWPi/rwpilib')

import PDALib
import myPDALib
import myPyLib
import time
import traceback
import motorsClass as motors
import encoders
import datetime as datetime


# Motor Class Methods:

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
#   waitForStopped(timeout=60)               # call to wait for motion to end with timeout


# Encoder Methods

#   init()                                   # hardware set
#   enable_encoder_interrupts()              # setup encoder interrupt
#   leftCount()                              # left count since last reset
#   rightCount()                             # right count since last reset
#   bias()                                   # absolute difference between left and right
#   reset()                                  # reset encoder counts to 0
#   disable_encoder_interrupts()             # disable encoder interrupt
#   printStatus()                            # print left, right, bias, and interrupt state

#   CLICKS_PIVOT_360=42   (from pogo lib_rwp)
#   CLICKS_SPIN_360=43    (from pogo lib_rwp)




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
  m = motors.Motors(30)

  try:
    print "\nENCODER DRIVE TEST"
    """
    m.setInitialCounts()
    print "Travel Forward 12 at Medium Speed"
    m.travel(12,m.MEDIUM)
    if (m.mode() == m.STOPPED): time.sleep(0.100)
    while (m.mode() != m.STOPPED): time.sleep(0.01)
    print "\n********************* DONE TRAVEL\n"
    encoders.printStatus()
    print "Distance Traveled: %.1f inches" % m.distanceTraveled()

    encoders.reset()
    time.sleep(15)

    m.setInitialCounts()
    print "Travel Backward 12 at Medium Speed"
    m.travel(-12,m.MEDIUM)
    if (m.mode() == m.STOPPED): time.sleep(0.100)
    while (m.mode() != m.STOPPED): time.sleep(0.01)
    print "\n********************* DONE TRAVEL"
    encoders.printStatus()
    print "Distance Traveled: %.1f inches" % m.distanceTraveled()

    time.sleep(15)
    """

    print "Turn CCW360"
    encoders.reset()
    trn1=m.CCW360
    m.turn(trn1)
    time.sleep(0.1)
    while (m.mode() != m.STOPPED): time.sleep(0.1)
    print "\n**** STOPPED "
    encoders.printStatus()

    time.sleep(15)

    print "Turn CW360"
    encoders.reset()
    trn1=m.CW360
    m.turn(trn1)
    time.sleep(0.1)
    while (m.mode() != m.STOPPED): time.sleep(0.1)
    print "\n**** STOPPED "
    encoders.printStatus()


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


