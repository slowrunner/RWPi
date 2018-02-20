#!/usr/bin/python
#
# rwpi.py   RWPi ROBOT
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
import sayStatus
import encoders
import battery
import irDistance
from enum import Enum
import os
import sys
from speak import say


class RWPi():
  # class constants and vars
  OFF=0
  STARTUP=1
  THINKING=2
  WALKING=3
  STOPPING=4
  STOPPED=5
  AVOIDING=6
  BUMPED=7
  ESCAPING=8
  MOVING=9
  EGRET=10
  SCANNER=11
  SHUTDOWN=12
  DONE=13
  
  State = Enum('OFF','STARTUP','THINKING','WALKING','STOPPING','STOPPED','AVOIDING','BUMPED', \
               'ESCAPING','MOVING','SHUTDOWN','DONE','EGRET',"SCANNER")

  lastState=OFF      # create an instance var self.lastState
  currentState=OFF
  bumpDir = Bumpers.NONE
  escapeDir = Motors.NONE
  avoidDir = Motors.NONE

  def newState(self,new):
    self.lastState = self.currentState
    self.currentState = new
    print "New state: %s" % str(self.currentState)
    
  def revertState(self,old):
    self.currentState = self.lastState
    self.lastState = old
    print "New state: %s" % str(self.currentState)

  MyDiaInInches=7.0

  def report(self,rptstr):
    print rptstr
    say(rptstr)

    
  def __init__(self):
      print "RWPi__init__"
      self.newState(RWPi.State.STARTUP)
      self.printStatus=printStatus.PrintStatus
      self.sayStatus=sayStatus.SayStatus
      self.bumpers=Bumpers()           # give robot instance bumpers
      self.usDistance=UltrasonicDistance()  # give robot instance ultrasonic sensor
      self.motors=Motors(readingsPerSec=20)
      encoders.init()
      encoders.enable_encoder_interrupts()
      print "waiting for threads to start"
      time.sleep(2)
      tiltpan.setup_servo_pins()
      tiltpan.center_servos()

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
          self.newState(RWPi.State.ESCAPING)
          escapeSpin = self.escapeDirDict[self.bumpDir]  
          while (self.currentState == RWPi.State.ESCAPING):
            # response to bumps
            # spin to escapeDir
            if (escapeSpin != Motors.NONE):
               # print "escapeSpin:",escapeSpin
               rptstr = "\n* Turning to %s as escape path" % self.motors.dirToStr(escapeSpin)
               self.report(rptstr)
               self.motors.turn(escapeSpin)
               self.motors.waitForStopped()
            rptstr = "Checking if escape path is clear"
            self.report(rptstr)
            tiltpan.center_servos()
            usDist = self.usDistance.inInches(UltrasonicDistance.AVERAGE)
            rptstr = "Forward path is clear for: %d inches" % int(usDist)
            self.report(rptstr)
            if (usDist > self.MyDiaInInches/2):
              rptstr = "Moving fwd half my size"
              self.report(rptstr)
              self.motors.travel(self.MyDiaInInches/2,Motors.SLOW)
              self.motors.waitForStopped()
              self.revertState(RWPi.State.ESCAPING)
            else:
              escapeSpin = Motors.CCW45
          self.revertState(RWPi.State.ESCAPING)
              
  def check_clear(self,bodyLengths=2):
    rptstr = "Checking if path is clear for %d bodyLengths" % bodyLengths
    self.report(rptstr)
    tiltpan.center_servos()
    usDist = self.usDistance.inInches(UltrasonicDistance.AVERAGE)
    clearLengths = int(usDist / self.MyDiaInInches)
    rptstr = "Forward path is clear for: %d lengths" % clearLengths
    self.report(rptstr)
    return (clearLengths >= bodyLengths)
    
              
  def do_avoid(self,bodyLengths=2):
    while (self.check_clear(bodyLengths) != True):
        if (self.currentState != RWPi.State.AVOIDING): 
            self.newState(RWPi.State.AVOIDING)
        # Choose an avoidance spin (hard coded right now)
        avoidSpin = Motors.CW45  
        # spin to avoidDir
        rptstr =  "\n* Turning to %s" % self.motors.dirToStr(avoidSpin)
        self.report(rptstr)
        self.motors.turn(avoidSpin)
        self.motors.waitForStopped()
    if (self.currentState == RWPi.State.AVOIDING):
        self.revertState(RWPi.State.AVOIDING)
          
  def do_thinking(self):
    numThoughts=0
    if (self.currentState != RWPi.THINKING):
        rptstr = "\nI'm THINKING now"
        self.report(rptstr)
        self.newState(RWPi.State.THINKING)
        tiltpan.center_servos()
        self.printStatus(self)
        self.sayStatus(self)
        if (battery.batteryTooLow()):
            rptstr = ("BATTERY %.2f volts BATTERY - SHUTTING DOWN NOW" % battery.volts())
            self.report(rptstr)
            os.system("sudo shutdown -h now")
            sys.exit(0)
        
    while (numThoughts < 300):    # think for about 30 seconds
        numThoughts += 1    
        if (self.bumpers.status() != Bumpers.NONE):
            self.newState(RWPi.State.BUMPED)
            self.bumpDir=self.bumpers.status()
            rptstr =  "\nI've been bumped! (%s)" % self.bumpers.toStr(self.bumpDir)       
            self.report(rptstr)
            self.do_escape()  
            self.revertState(RWPi.State.THINKING)              
        time.sleep(0.1)      
    self.revertState(RWPi.State.THINKING)

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
    self.newState(RWPi.State.EGRET)
    while (self.currentState != RWPi.State.DONE):
        self.do_thinking()
        self.newState(RWPi.State.EGRET)
        if (self.check_clear(4) == True):
            print "egret.py:be_egret: MOVING 3 body lengths"
            self.report("Moving 3 body lengths")
            self.newState(RWPi.State.MOVING)
            self.motors.travel(self.MyDiaInInches*3,Motors.FAST)
            self.motors.waitForStopped()
            self.newState(RWPi.State.STOPPED)
        elif (self.check_clear(2) == True):
            print "egret.py:be_egret: MOVING 1 body length"
            self.report("Moving 1 body length")
            self.newState(RWPi.State.MOVING)
            self.motors.travel(self.MyDiaInInches,Motors.MEDIUM)
            self.motors.waitForStopped()
            self.newState(RWPi.State.STOPPED)
        else:
          self.do_avoid()

  def be_scanner(self):
    scanDirs=13  # 13 gives 15 deg
    scanDeltaAngle = 180 / (scanDirs-1)
    if (self.currentState != RWPi.SCANNER):
          rptstr = "\nI'm Scanning now"
          print rptstr
          self.report(rptstr)
          self.newState(RWPi.State.SCANNER)        
    while (self.currentState != RWPi.State.DONE):
        self.do_thinking()
        for scanAngle in range(180,-1,-scanDeltaAngle):
          tiltpan.pan_servo(scanAngle)
          time.sleep(3)  # to be sure sensor has been polled
          usDist = self.usDistance.inInches()
          irDist = irDistance.inInches()
          print "angle: %d  usDist: %0.1f  irDist: %0.1f inches" % (scanAngle, usDist, irDist)
          time.sleep(2.0)      
    
               

  
  def cancel(self):
     print "RWPi.cancel() called"
     self.report("RWPi.cancel called")
     self.motors.cancel()
     self.newState(RWPi.State.SHUTDOWN)
     self.printStatus(self)
     self.bumpers.cancel()
     self.usDistance.cancel()
     encoders.cancel()
     self.newState(RWPi.State.DONE)
     myPDALib.PiExit()

  def set_cntl_c_handler(self):
     myPyLib.set_cntl_c_handler(self.cancel)  # Set CNTL-C handler 


#end RWPi() class

# ##### MAIN ######
def main():
  try:
    print "Starting rwpi.py Main"
    
    r=RWPi()
    r.set_cntl_c_handler()
    r.be_scanner()
  except SystemExit:
    print "rwpi.py main: time for threads to quit"
    time.sleep(1)
    print "rwpi.py says: Bye Bye"    
  except:
    print "Exception Raised"
    traceback.print_exc()
    

 
if __name__ == "__main__":
    main()

