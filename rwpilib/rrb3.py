#!/usr/bin/python
#
# rrb3.py   RaspiRobotBoard Interface for RWPi ROBOT
#

#    forward(self, seconds=0, speed=1.0):
#    stop(self):
#    reverse(self, seconds=0, speed=1.0):
#    left(self, seconds=0, speed=0.5):
#    right(self, seconds=0, speed=0.5):

#    get_distance(self):

#    cleanup(self):

#    set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
#    set_driver_pins(self, left_pwm, left_dir, right_pwm, right_dir):

#    To use:  import rrb3 as rrb
#             rr=rrb.RRB3()
#             rr.forward(2,1.0)  # fwd for 2s at full speed
#             print("distance: %.1f cm" % rr.get_distance()) 


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


class RRB3():
  # rrb3 stuff
  MOTOR_DELAY = 0.2

  left_pwm = 0        # 0.0-1.0
  right_pwm = 0       # 0.0-1.0

  old_left_dir = -1   # 0=fwd, 1=bwd
  old_right_dir = -1  # 0=fwd, 1=bwd

  # #### RWPi Vars AND CONSTANTS

  LEFT = 0     # LEFT MOTOR
  RIGHT = 1    # RIGHT MOTOR

  # Motor Pins 
  # SRV 6		Motor 1 Speed (PWM)
  # SRV 7		Motor 2 Speed (PWM)

  RMotor = 6
  LMotor = 7

  MotorPin = [7,6]  # MotorPin[0] Left, MotorPin[1] Right

  # DIO 12 (A4)	Motor 1 Dir A (0=coast 1=F/Brake)
  # DIO 13 (A5)	Motor 1 Dir B (0=coast 1=R/Brake)

  # DIO 14 (A6)	Motor 2 Dir A (0=coast 1=F/Brake)
  # DIO 15 (A7)	Motor 2 Dir B (0=coast 1=R/Brake)

  M1DirA = 12
  M1DirB = 13
  M2DirA = 14
  M2DirB = 15
  MotorDirA = [14,12]  # 0 left 1 right
  MotorDirB = [15,13]  # 0 left 1 right

  MinPwr2Move = 100
  MaxPwr = 255






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
      print "RRB3__init__"
      self.newState(RRB3.State.STARTUP)
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
          self.newState(RRB3.State.ESCAPING)
          escapeSpin = self.escapeDirDict[self.bumpDir]  
          while (self.currentState == RRB3.State.ESCAPING):
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
              self.revertState(RRB3.State.ESCAPING)
            else:
              escapeSpin = Motors.CCW45
          self.revertState(RRB3.State.ESCAPING)
              
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
        if (self.currentState != RRB3.State.AVOIDING): 
            self.newState(RRB3.State.AVOIDING)
        # Choose an avoidance spin (hard coded right now)
        avoidSpin = Motors.CW45  
        # spin to avoidDir
        rptstr =  "\n* Turning to %s" % self.motors.dirToStr(avoidSpin)
        self.report(rptstr)
        self.motors.turn(avoidSpin)
        self.motors.waitForStopped()
    if (self.currentState == RRB3.State.AVOIDING):
        self.revertState(RRB3.State.AVOIDING)
          
  def do_thinking(self):
    numThoughts=0
    if (self.currentState != RRB3.THINKING):
        rptstr = "\nI'm THINKING now"
        self.report(rptstr)
        self.newState(RRB3.State.THINKING)
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
            self.newState(RRB3.State.BUMPED)
            self.bumpDir=self.bumpers.status()
            rptstr =  "\nI've been bumped! (%s)" % self.bumpers.toStr(self.bumpDir)       
            self.report(rptstr)
            self.do_escape()  
            self.revertState(RRB3.State.THINKING)              
        time.sleep(0.1)      
    self.revertState(RRB3.State.THINKING)

  def cancel(self):
     print "RRB3.cancel() called"
     self.report("RRB3.cancel called")
     self.motors.cancel()
     self.newState(RRB3.State.SHUTDOWN)
     self.printStatus(self)
     self.bumpers.cancel()
     self.usDistance.cancel()
     encoders.cancel()
     self.newState(RRB3.State.DONE)
     myPDALib.PiExit()

  def set_cntl_c_handler(self):
     myPyLib.set_cntl_c_handler(self.cancel)  # Set CNTL-C handler 


#    forward(self, seconds=0, speed=1.0):
  def forward(self, seconds=0, speed=1.0):
      self.motors.drive(int(speed*100))   # translate 0-1 to 0-100
      if seconds >0:
          time.sleep(seconds)
          self.stop()

#    stop(self):
  def stop(self):
      self.motors.stop()

#    reverse(self, seconds=0, speed=1.0):
  def reverse(self, seconds=0, speed=1.0):
      #self.set_motors(speed, 1, speed, 1)
      self.motors.drive(-int(speed*100))  # translate 0-1 to 0..-100
      if seconds >0:
          time.sleep(seconds)
          self.stop()




#    left(self, seconds=0, speed=0.5):
  def left(self, seconds=0, speed=0.5):
      self.motors.spin(int(speed*100))           # translate 0-1 to 0-100
      if seconds >0:
          time.sleep(seconds)
          self.stop()



#    right(self, seconds=0, speed=0.5):
  def right(self, seconds=0, speed=0.5):
      self.motors.spin(-int(speed*100))         # translate 0-1 into  0 to -100
      if seconds >0:
          time.sleep(seconds)
          self.stop()


#    get_distance(self):
  def get_distance(self):
      return self.usDistance.read()    #perform one reading and return distance in Cm

#    cleanup(self):
  def cleanup(self):
      self.cancel()

#    set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
  def set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
        if self.old_left_dir != left_dir or self.old_right_dir != right_dir:
            self.motors.stop()    # stop motors between sudden changes of direction
            time.sleep(self.MOTOR_DELAY)
        self.set_driver_pins(left_pwm, left_dir, right_pwm, right_dir)
        self.old_left_dir = left_dir
        self.old_right_dir = right_dir

#    set_driver_pins(self, left_pwm, left_dir, right_pwm, right_dir):
  def set_driver_pins(self, left_pwm, left_dir, right_pwm, right_dir):  # 0.0 to 1.0, fwd=0 rev=1, 0.0-1.0, fwd=0 rev=1
        #self.left_pwm.ChangeDutyCycle(left_pwm * 100 * self.pwm_scale)
        if(left_pwm > 0):
          PDALib.analogWrite(self.MotorPin[self.LEFT], int( left_pwm * (self.MaxPwr - self.MinPwr2Move) + self.MinPwr2Move ) ) #set motor pwr level
        else:
          PDALib.analogWrite(self.MotorPin[self.LEFT], 0 ) #set motor pwr level

        #GPIO.output(self.LEFT_1_PIN, left_dir)
        #GPIO.output(self.LEFT_2_PIN, not left_dir)
        PDALib.digitalWrite(self.MotorDirA[self.LEFT],not left_dir)      # write 1=fwd 0=coast
        PDALib.digitalWrite(self.MotorDirB[self.LEFT],left_dir)          # write 1=bwd 0=coast

        #self.right_pwm.ChangeDutyCycle(right_pwm * 100 * self.pwm_scale)
        if(right_pwm > 0):
          PDALib.analogWrite(self.MotorPin[self.RIGHT], int( right_pwm * (self.MaxPwr - self.MinPwr2Move) + self.MinPwr2Move ) ) #set motor pwr level
        else:          
          PDALib.analogWrite(self.MotorPin[self.RIGHT], 0 )    #set motor pwr level to 0 
        #GPIO.output(self.RIGHT_1_PIN, right_dir)
        #GPIO.output(self.RIGHT_2_PIN, not right_dir)
        PDALib.digitalWrite(self.MotorDirA[self.RIGHT],not right_dir)      # write 1=fwd 0=coast
        PDALib.digitalWrite(self.MotorDirB[self.RIGHT],right_dir)          # write 1=bwd 0=coast



#end RRB3() class

# ##### MAIN ######
def main():
  try:
    print "Starting rr3.py Main"
    
    r=RRB3()
    r.set_cntl_c_handler()
    r.stop()
    r.forward(1,1)
    r.left(1,0.75)
    r.reverse(1,1)
    r.right(1,0.75)
    r.reverse(2)
    r.left(1)
    r.forward(2)
    r.right(0.5)
    r.left(0.5)
    r.right(0.5)
    print("distance: %.1f cm" % r.get_distance()) 
    r.do_thinking()
    r.cleanup()
    sys.exit(0)
  except SystemExit:
    print "rrb3.py main: time for threads to quit"
    time.sleep(1)
    print "rrb3.py says: Bye Bye"    
  except:
    print "Exception Raised"
    traceback.print_exc()
    

 
if __name__ == "__main__":
    main()

