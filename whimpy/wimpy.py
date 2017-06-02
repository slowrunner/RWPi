#!/usr/bin/python
#
# wimpy.py   WIMPY ROBOT
#

import rwpilib.PDALib as PDALib
import rwpilib.myPDALib as myPDALib
import rwpilib.myPyLib as myPyLib
from rwpilib.bumpersClass import Bumpers
from rwpilib.usDistanceClass import UltrasonicDistance
import rwpilib.motorsClass as motorsClass
from rwpilib.motorsClass import Motors
import time
import traceback
import rwpilib.tiltpan as tiltpan
import rwpilib.printStatus as printStatus
import rwpilib.encoders as encoders


class Robot():
  # class constants and vars
  OFF=0
  STARTUP=1
  HAPPY=2
  BUMPED=3
  ESCAPING=4
  DONE=5

  lastState=OFF      # create an instance var self.lastState
  currentState=OFF
  bumpDir = Bumpers.NONE
  escapeDir = Motors.NONE

  def newState(self,new):
    self.lastState = self.currentState
    self.currentState = new

  MyDiaInInches=7.0

  def __init__(self):
      print "Robot__init__"
      self.newState(Robot.STARTUP)
      self.printStatus=printStatus.PrintStatus
      self.bumpers=Bumpers()           # give robot instance bumpers
      self.usDistance=UltrasonicDistance()  # give robot instance ultrasonic sensor
      self.motors=Motors(readingsPerSec=20)
      encoders.init()
      encoders.enable_encoder_interrupts()
      print "waiting for threads to start"
      time.sleep(2)

  escapeDirDict={
               Bumpers.NONE      : Motors.NONE,
               Bumpers.REAR      : Motors.NONE, 
               Bumpers.FRONT     : Motors.CW180,
               Bumpers.LEFT      : Motors.CW90,
               Bumpers.RIGHT     : Motors.CCW90,
               Bumpers.LEFTREAR  : Motors.CW45,
               Bumpers.RIGHTREAR : Motors.CCW45,
               Bumpers.ALL       : Motors.NONE }

  def do_escape(self):
          self.newState(Robot.ESCAPING)
          escapeSpin = self.escapeDirDict[self.bumpDir]  
          while (self.currentState == Robot.ESCAPING):
            # response to bumps
            # spin to escapeDir
            if (escapeSpin != Motors.NONE):
               # print "escapeSpin:",escapeSpin
               print "\n* Turning to %s as escape path" % self.motors.dirToStr(escapeSpin)
               self.motors.turn(escapeSpin)
               self.motors.waitForStopped()
            print "Checking if escape path is clear"
            usDist = self.usDistance.inInches(UltrasonicDistance.AVERAGE)
            print "Forward path is clear for: %d inches" % int(usDist)
            if (usDist > self.MyDiaInInches/2):
              print "Moving fwd half my size"
              self.motors.travel(self.MyDiaInInches/2,Motors.SLOW)
              self.motors.waitForStopped()
              self.lastState=self.currentState
              self.currentState=self.DONE
            else:
              escapeSpin = Motors.CCW45
              
  def be_happy(self):
          if (self.currentState != Robot.HAPPY):
              print "\nI'm happy now"
              self.newState(Robot.HAPPY)
              self.printStatus(self)
          # DO NOTHING (BEING HAPPY)
          time.sleep(0.1)
     

  def be_wimpy(self):
    while True:
      if (self.bumpers.status() == Bumpers.NONE):
          self.be_happy()
      else:
          self.newState(Robot.BUMPED)
          self.bumpDir=self.bumpers.status()
          print "\nI've been bumped! (%s)" % self.bumpers.toStr(self.bumpDir)       
          self.do_escape()


               

  
  def cancel(self):
     print "robot.cancel() called"
     self.bumpers.cancel()
     self.motors.cancel()
     self.usDistance.cancel()
     encoders.cancel()

#end Robot() class

# ##### MAIN ######
def main():
  try:
    print "Starting Main"
    tiltpan.setup_servo_pins()
    tiltpan.center_servos()
    
    r=Robot()
    myPyLib.set_cntl_c_handler(r.cancel)  # Set CNTL-C handler 
    r.be_wimpy()
  except SystemExit:
    myPDALib.PiExit()
    print "whimpy: time for threads to quit"
    time.sleep(1)
    print "whimpy.py says: Bye Bye"    
  except:
    print "Exception Raised"
    # r.cancel()
    traceback.print_exc()
    

 
if __name__ == "__main__":
    main()

