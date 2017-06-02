#!/usr/bin/python
#
# lewisandclark.py
#
# Lewis and Clark Robot
# Purpose: Move and don't get stuck
# Based on "Mobile Robots: Inspiration to Implementation",2nd Ed.
#           Anita M. Flynn, Joseph L. Jones, Bruce A. Seigler
# Note the book's author list as published was "Joseph L. Jones, Bruce A. Seiger, Anita M. Flynn"
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
  EXPLORING=2
  BUMPED=3
  ESCAPING=4
  AVOIDING=5
  DONE=6

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
              print "Returning to state before needed escape"
              if (self.lastState != Robot.ESCAPING):
                self.currentState = self.lastState
              else:
                print "Escape from Escape needed? Done"
                self.currentState = Robot.DONE 
              self.lastState = Robot.ESCAPING
            else:
              escapeSpin = Motors.CCW45

  def do_avoid(self):
          self.newState(Robot.AVOIDING)
          avoidSpin = self.escapeDirDict[self.bumpDir]  
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
              print "Return to state before escape needed"
              self.currentState=self.lastState
              self.lastState=self.AVOIDING
              self.currentState=self.DONE
            else:
              escapeSpin = Motors.CCW45

              
  def do_explore(self):
          if (self.currentState != Robot.EXPLORING):
              print "\nI'm happy now"
              self.newState(Robot.EXPLORING)
              self.printStatus(self)
              self.motors.drive(Motors.SLOW)
          time.sleep(0.1)
     

  def be_lewisandclark(self):
    while True:
      if (self.bumpers.status() != Bumpers.NONE):
          self.newState(Robot.BUMPED)
          self.bumpDir=self.bumpers.status()
          print "\nI've been bumped! (%s)" % self.bumpers.toStr(self.bumpDir)       
          self.do_escape()
      if (


               

  
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
    r.be_lewisandclark()
  except SystemExit:
    myPDALib.PiExit()
    print "lewisandclark: time for threads to quit"
    time.sleep(1)
    print "lewisandclark.py says: Bye Bye"    
  except:
    print "Exception Raised"
    # r.cancel()
    traceback.print_exc()
    

 
if __name__ == "__main__":
    main()

