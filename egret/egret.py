#!/usr/bin/python
#
# egret.py   EGRET ROBOT
#

import PDALib
import myPDALib
import myPyLib
from bumpersClass import Bumpers
from usDistanceClass import UltrasonicDistance
import motorsClass
from motorsClass import Motors
import time
import traceback
import tiltpan
import printStatus
import encoders


class Robot():
  # class constants and vars
  OFF=0
  STARTUP=1
  THINKING=2
  WALKING=3
  STOPPING=4
  AVOIDING=5
  BUMPED=6
  ESCAPING=7
  DONE=8

  lastState=OFF      # create an instance var self.lastState
  currentState=OFF
  bumpDir = Bumpers.NONE
  escapeDir = Motors.NONE
  avoidDir = Motors.NONE

  def newState(self,new):
    self.lastState = self.currentState
    self.currentState = new
    
  def revertState(self,old):
    self.currentState = self.lastState
    self.lastState = old
 
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
              self.revertState(Robot.ESCAPING)
            else:
              escapeSpin = Motors.CCW45
              
  def check_clear(self,bodyLengths=2):
    print "Checking if path is clear"
    usDist = self.usDistance.inInches(UltrasonicDistance.AVERAGE)
    clearLengths = int(usDist / self.MyDiaInInches)
    print "Forward path is clear for: %d lengths" % clearLengths
    return (clearLengths > bodyLengths)
    
              
  def do_avoid(self,bodyLengths=2):
    while ((check_clear(bodyLengths) != True):
        if (self.currentState != Robot.AVOIDING): 
            self.newState(Robot.AVOIDING)
            # Choose an avoidance spin (hard coded right now)
            avoidSpin = Motors.CW45  
            # spin to avoidDir
            if (avoidSpin != Motors.NONE):
                # print "avoidSpin:",avoidSpin
                print "\n* Turning to %s" % self.motors.dirToStr(avoidSpin)
                self.motors.turn(avoidSpin)
                self.motors.waitForStopped()
    if (self.currentState == Robot.AVOIDING):
        self.revertState(Robot.AVOIDING)
          
  def be_THINKING(self):
    if (self.currentState != Robot.THINKING):
        print "\nI'm THINKING now"
        self.newState(Robot.THINKING)
        self.printStatus(self)
        numThoughts=0
    while (numThoughts < 300):    # think for about 30 seconds
        numThoughts += 1    
        if (self.bumpers.status() != Bumpers.NONE):
            self.newState(Robot.BUMPED)
            self.bumpDir=self.bumpers.status()
            print "\nI've been bumped! (%s)" % self.bumpers.toStr(self.bumpDir)       
            self.do_escape()  
            self.revertState(Robot.THINKING)              
        time.sleep(0.1)      
     
'''  egret(): egret inspired behavior
  loop until "tired*":
     (Look straight ahead)
     loop until "tired of standing here":
        "think about something"
     how far is path forward clear*?
     if path not clear, 
         turn to new direction
     else: 
        move "forward some"*
        reset standing here time to 0
         
* tired: remaining battery life estimated to be 20%
* path clear:  ultrasonic distance > 4 body diameters
* forward some:   3 body diameters
 '''
 
  def be_egret(self):
    while (self.currentState != Robot.DONE):
        self.be_THINKING()
        if (check_clear(4) == True):
            self.newState(Robot.MOVING)
            self.motors.travel(self.MyDiaInInches*3,Motors.MEDIUM)
            self.motors.waitForStopped()
            self.newState(Robot.STOPPED)
        elif (check_clear(2) == True):
            self.newState(Robot.MOVING)
            self.motors.travel(self.MyDiaInInches,Motors.SLOW)
            self.motors.waitForStopped()
            self.newState(Robot.STOPPED)
        else:
          self.do_avoid()


               

  
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
    r.be_egret()
  except SystemExit:
    myPDALib.PiExit()
    print "egret main: time for threads to quit"
    time.sleep(1)
    print "egret.py says: Bye Bye"    
  except:
    print "Exception Raised"
    # r.cancel()
    traceback.print_exc()
    

 
if __name__ == "__main__":
    main()

