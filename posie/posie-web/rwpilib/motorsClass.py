#!/usr/bin/python
#
# motorsClass.py   MOTORS CLASS
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
#  ### INTERNAL METHODS

#   __init__(readingsPerSec=10)          # initialize instance of class
#   setup_motor_pins()                   # set up Pi Droid Alpha and GPIO
#
#   ### THREAD METHODS
#
#   pollMotors(tSleep=0.1)               # motor control thread
#
#   rampTgtCurStep(target,current,rampStep)  # calculate next speed on ramp to target
#   speed2Pwr(s,driveSpeed,spinSpeed)    # convert speed (+/- 0-100%) to 
#   setMotorsPwr(lPwr,rPwr)              # Apply power to motors Pwr: +/- (0-255)
#                                            #         power between (+/- 255 and minimum to move)
#   control()          # dispatch to control methods based on motorsMode
#   controlDrive()     # monitor drive mode
#   controlSpin()      # monitor spin mode
#   controlTravel()    # monitor drive until distance reached
#   controlTurn()      # monitor spin until angle reached
#   controlStop()      # monitor drive or spin while stopping
#   controlStopped()   # routine called while motors are not running
#
#   motors_off()
#
#   motors_fwd()
#   motors_bwd()
#   motors_ccw()
#   motors_cw()

# INTERNAL VARS
#
#   motorsMode
#   self.debugLevel  0=off 1=basic 99=all

import sys
# uncomment when testing below rwpilib\ 
#sys.path.insert(0,'..')

import PDALib
import myPDALib
import myPyLib
from myPyLib import sign, clamp
import time
import threading
import traceback
import datetime
import encoders


class Motors():

  # CLASS VARS (Avail to all instances)
  # Access as Motors.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the Motors class   
  tSleep=0.1            # time for read_sensor thread to sleep 
  debugLevel=0          # set self.debugLevel (or motors.debugLevel) =99 for all, =1 for some

  # Empirical settings for minimum drive to turn each wheel
  # PWM_frequency dependent, PiDALib default is 490
  # PWM_f   RMotorMinF   LMotorMinF
  # 10000   215           185
  # 490	     83		    73  <--
  # 100	     34		    33
  # 33	     22		    20

  # RMotorMinF = 83  # no load (takes more to get right going reliably)
  # LMotorMinF = 73  # no load 
  # RMotorMinB = 94  # no load (takes more to get right going reliably)
  # LMotorMinB = 86  # no load 
  # Motor Pins 

  # SRV 6		Motor 1 Speed (PWM)
  # SRV 7		Motor 2 Speed (PWM)
  RMotor = 6
  LMotor = 7

  # DIO 12 (A4)	        Motor 1 Dir A (0=coast 1=F/Brake)
  # DIO 13 (A5)	        Motor 1 Dir B (0=coast 1=R/Brake)

  # DIO 14 (A6)  	Motor 2 Dir A (0=coast 1=F/Brake)
  # DIO 15 (A7) 	Motor 2 Dir B (0=coast 1=R/Brake)

  M1DirA = 12
  M1DirB = 13
  M2DirA = 14
  M2DirB = 15

  
  minFwdPwr = 145 # 83      # minimum to start moving forward
  minBwdPwr = 145 # 120 # 94      # minimum to start moving backward
  
  driveSpeed   = 0       # target 0 to +/-100% of speed range
  _currentSpeed = 0       # current speed at the moment, ramps up or down
  rampStep     = 13      # amount to change speed each time through control loop 

  minCCWPwr = 120 # 86      # minimum drive to spin CCW
  minCWPwr  = 120 # 94      # minimum drive to spin CW

  biasFwd  = 21      # amount of right more than left needed to go Fwd straight
  biasBwd  = 0       # amount of right more than left needed to go Bwd straight

  maxPwr = 255

  driveDistance  = 0    # distance in inches fwd(+) or bwd(-)
  currentDistance= 0    # how far travelled since told to travel

  initialLeftCount = 0  # place to store the counter value when starting motion
  initialRightCount = 0
  initialMeanCount = 0

  targetTime= 0         # time to stop travel (till encoders)

  spinSpeed   = 0       # speed to spin ccw(+) cw(-)
  turnDir     = 0

  #Modes
  STOPPED = 0 
  DRIVE   = 1
  TRAVEL  = 2
  SPIN    = 3
  TURN    = 4 
  STOP    = 5

  Modes2Str = { STOPPED  : 'STOPPED',
                 STOP     : 'STOP',
                 DRIVE    : 'DRIVE',
                 TRAVEL   : 'TRAVEL',
                 SPIN     : 'SPIN',
                 TURN     : 'TURN' }

  motorsMode     = STOPPED
  
  def mode(self):
      return self.motorsMode
 
  def modeToStr(mode = motorsMode):
      return Modes2Str[mode]
      
  lastMotorsMode = STOPPED

  #Speeds
  NONE    = 0
  SLOW    = 1
  WALK    = 5    
  MEDIUM  = 50
  FAST    = 100

  SpeedsToStr = {NONE    : 'NONE',
                 SLOW    : 'SLOW',
                 WALK    : 'WALK',
                 MEDIUM  : 'MEDIUM',
                 FAST    : 'FAST',
                 -SLOW   : '-SLOW',
                 -WALK   : '-WALK',
                 -MEDIUM : '-MEDIUM',
                 -FAST   : '-FAST' }

  def currentSpeed():
      return _currentSpeed

  def speedToStr(nSpeed=_currentSpeed):
       if (nSpeed in SpeedsToStr):
           speedStr=SpeedsToStr[nSpeed]
       else:
           speedStr=str(nSpeed)
  
  InchesPerSec = {      # travel distance per second (for 24")
                  SLOW   : 1.5,
                  WALK   : 2.0,    
                  MEDIUM : 3.1,
                  FAST   : 6.7,
                  -SLOW  : 1.5,
                  -WALK  : 2.0,
                  -MEDIUM: 3.1,
                  -FAST  : 6.7 }


  MotorRampTime = 0.25    # NOT IMPLEMENTED

  CCW360 = 3.15           # seconds to turn at Motors.MEDIUM
  CCW180 = 1.58
  CCW135 = 1.15
  CCW90  = 0.84
  CCW45  = 0.5
  CW360  = -CCW360
  CW180  = -CCW180
  CW135  = -CCW135
  CW90   = -CCW90 * 0.93
  CW45   = -CCW45 * 0.9
  NOTURN = 0

  DirsToStr = {
    CCW45  : 'CCW45',
    CCW90  : 'CCW90',
    CCW135 : 'CCW135',
    CCW180 : 'CCW180',
    CCW360 : 'CCW360',
    CW45   : 'CW45',
    CW90   : 'CW90',
    CW135  : 'CW135',
    CW180  : 'CW180',
    CW360  : 'CW360', 
    NOTURN : 'NO TURN'}

  def dirToStr(self, mDir):
       if (mDir in self.DirsToStr):
          strDir=self.DirsToStr[mDir]
       else:
          strDir='?'
       return strDir
    
  
  
  # end of class vars definition

  # ### encoder methods

  def setInitialCounts(self):
    initialLeftCount=encoders.leftCount()
    initialRightCount=encoders.rightCount()
    initialMeanCount=(initialLeftCount+initialRightCount)/2.0 

  def distanceTraveled(self):
    currentLeftCount = encoders.leftCount()
    currentRightCount = encoders.rightCount()
    currentMeanCount = ( currentLeftCount + currentRightCount) / 2.0
    countsTraveled = (currentMeanCount - self.initialMeanCount)
    distance=countsTraveled * encoders.InchesPerCount
    if (self.debugLevel > 1): 
       print "motorsClass:distanceTraveled: called"
       print "encoder status:"
       encoders.printStatus()
       print "distance traveled:", distance

    return distance
    

  def __init__(self,readingsPerSec=10):
    self.setup_motor_pins()
    # SINGLETON TEST 
    if (Motors.pollThreadHandle!=None): 
        print "Second Motors Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "Motors: worker thread readingsPerSec:",readingsPerSec
    Motors.tSleep=1.0/readingsPerSec    #compute desired sleep
    Motors.readingsPerSec=readingsPerSec
    Motors.pollThreadHandle = threading.Thread( target=self.pollMotors, 
                                               args=(Motors.tSleep,))
    Motors.pollThreadHandle.start()
    if (self.debugLevel >0):  print "Motors worker thread told to start",datetime.datetime.now()
    time.sleep(0.01)  # give time for motor control thread to start
  #end init()

  # Motors THREAD WORKER METHOD TO CONTROL MOTORS
  def pollMotors(self,tSleep=0.1):     
    print ("Motors: pollMotors thread started with %f at %s" % (tSleep,datetime.datetime.now()))
    t = threading.currentThread()   # get handle to self (pollingMotors thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.control()
      time.sleep(tSleep)
    if (self.debugLevel >0):  print("do_run went false. Stopping pollMotors thread at %s" % datetime.datetime.now())

  # RAMP FROM CURRENT TO TARGET IN STEP (TARGET BETWEEN -100 to +100)
  #
  # usage:  nextCurrent = rampTargetCurrentStep(target, current, rampStep)
  #
  def rampTgtCurStep(self, target, current, rampStep):
      if (self.debugLevel >1):   print "\n", datetime.datetime.now()
      if (self.debugLevel >1):   print "tgt: %d cur: %d  ramp: %d" % (target, current, rampStep)
      nextCurrent = current
      if (nextCurrent != target):
        if (target >= 0):
          if (current < target):
            nextCurrent += rampStep
            nextCurrent = clamp(nextCurrent,-100,target)
          elif (current > target):
            nextCurrent -= rampStep
            nextCurrent = clamp(nextCurrent,target,100)

        elif (target<0):
          if (current > target):
            nextCurrent -= rampStep
            nextCurrent = clamp(nextCurrent,target,100)
          elif (current < target):
            nextCurrent += rampStep
            nextCurrent = clamp(nextCurrent,-100,target)
      if (self.debugLevel >1):   print "nextCurrent: %d" % nextCurrent
      return nextCurrent

  # ##### SPEED2PWR 
  # convert left,right speeds +/-(0 to 100) to power +/-(minDrive to 255)
  #   (with positive bias of right more than left) 
  #   returns (lpwr,rpwr)
  #
  def speed2Pwr(s,driveSpeed,spinSpeed):
     # ### DRIVE
     if (driveSpeed>0):   # FORWARD
       pwrA= int( (s.maxPwr-s.minFwdPwr)*(driveSpeed/100.0) + s.minFwdPwr)
       pwrB= (pwrA-abs(s.biasFwd))
       if (s.biasFwd>0):     
           rPwr=pwrA   # right more than left
           lPwr=pwrB
       else:
           rPwr=pwrB   # right less than left
           lPwr=pwrA
     if (driveSpeed<0):  # BACKWARD
       pwrA= int( (s.maxPwr-s.minBwdPwr) * abs(driveSpeed/100.0) + s.minBwdPwr)
       pwrB= (pwrA-abs(s.biasBwd))
       if (s.biasBwd>0): 
           rPwr=-pwrA   # right more than left
           lPwr=-pwrB  
       else:
           rPwr=-pwrB   # right less than left
           lPwr=-pwrA

     # ### SPIN
     if (spinSpeed>0 ):    #  CCW
       rPwr= int( (s.maxPwr-s.minCCWPwr)*(spinSpeed/100.0) + s.minCCWPwr)
       lPwr= -rPwr
     elif (spinSpeed<0 ):  # CW
       lPwr= int( (s.maxPwr-s.minCWPwr) * abs(spinSpeed/100.0) + s.minCWPwr)
       rPwr= -lPwr
     elif (spinSpeed ==0 and driveSpeed==0):
       lPwr=0
       rPwr=0
     return (lPwr,rPwr)


  def controlDrive(self):
      if (self.debugLevel >1):   print "handling motorsMode DRIVE"
      self._currentSpeed = self.rampTgtCurStep(self.driveSpeed, 
                                         self._currentSpeed, 
                                         self.rampStep)
      lPwr,rPwr = self.speed2Pwr(self._currentSpeed,0)
      self.setMotorsPwr(lPwr,rPwr)  # pwrs=(lPwr,rPwr)


  # ### CONTROL TRAVEL
  # Travel at set speed until 30% of distance, then WALK
  def controlTravel(self):
      if (self.debugLevel >1):   print "handling motorsMode TRAVEL"
      self._currentSpeed = self.rampTgtCurStep(self.driveSpeed, 
                                         self._currentSpeed, 
                                         self.rampStep)
      lPwr,rPwr = self.speed2Pwr(self._currentSpeed,0)  
      self.setMotorsPwr(lPwr,rPwr)  # pwrs=(lPwr,rPwr)

      if (self.debugLevel >1):   print "controlTravel:",datetime.datetime.now()
      if (self.targetTime == 0):
         # tvl_time is based on driveDistance which may be negative - use sign(driveDistance) to fix
         tvl_time = sign(self.driveDistance)* self.driveDistance/self.InchesPerSec[self.driveSpeed]
         if (self.debugLevel >1):   print "controlTravel: tvl_time: %.1f" % tvl_time
         tgt_secs = int(tvl_time)
         tgt_millisec = int((tvl_time-tgt_secs)*1000)
         tgt_delta=datetime.timedelta(seconds=tgt_secs+5, milliseconds=tgt_millisec)
         self.targetTime = datetime.datetime.now()+tgt_delta
      if (datetime.datetime.now() > self.targetTime):
         if (self.debugLevel >0):   print ("controlTravel: hit time limit at %s" % datetime.datetime.now() )
         self.targetTime = 0
         self.stop()
      self.currentDistance = self.distanceTraveled()
      if (self.currentDistance > abs(self.driveDistance)):
         if (self.debugLevel >0):   print ("controlTravel: hit distance limit at %s" % datetime.datetime.now() )
         self.targetTime = 0
         self.stop()
      else:
         if (self.debugLevel >0): 
             print "controlTravel: dist: %.1f" % self.currentDistance
         if (abs(self.driveSpeed) > Motors.WALK):
             if (self.currentDistance > abs(0.3 * self.driveDistance)):
               self.driveSpeed = sign(self.driveDistance) * Motors.WALK
               if (self.debugLevel > 0): print "motorsClass:controlTravel:30% there - slow to WALK"       

      return


  def controlSpin(self):
      if (self.debugLevel >1):   print "handling motorsMode SPIN"
      self._currentSpeed = self.rampTgtCurStep(self.spinSpeed,
                                         self._currentSpeed, 
                                         self.rampStep)
      lPwr,rPwr = self.speed2Pwr(0,self._currentSpeed)  # (drive,spin)
      self.setMotorsPwr(lPwr,rPwr)  # pwrs=(lPwr,rPwr)
      return
    
  def controlTurn(self):
      if (self.debugLevel >1):   print "handling motorsMode TURN"

      if (self.debugLevel >1):   print "controlTurn:",datetime.datetime.now()
      if (self.targetTime == 0):
         trn_time = sign(self.turnDir)*self.turnDir
         tgt_secs = int(trn_time)
         tgt_millisec = int( (trn_time - clamp(tgt_secs,0,60) )*1000)
         tgt_delta=datetime.timedelta(seconds=tgt_secs, milliseconds=tgt_millisec)
         self.targetTime = datetime.datetime.now()+tgt_delta
         if (self.debugLevel >1):   print ("tgt_secs: %d tgt_millisec: %d tgt_time: %s" % (tgt_secs, tgt_millisec, self.targetTime))
      if (datetime.datetime.now() > self.targetTime):
         if (self.debugLevel >1):   print ("controlTurn: hit requested limit at %s" % datetime.datetime.now() )
         self.targetTime = 0
#         self.stop()
         self.spinSpeed     = Motors.NONE
         self.driveSpeed    = Motors.NONE
         self.driveDistance = 0
         self.motorsMode    = Motors.STOP
     
      self._currentSpeed = self.rampTgtCurStep(self.spinSpeed, 
                                         self._currentSpeed, 
                                         self.rampStep)
      lPwr,rPwr = self.speed2Pwr(0,self._currentSpeed)  # (drive,spin)
      self.setMotorsPwr(lPwr,rPwr)  

      return
    
  def controlStop(self):
      if (self.debugLevel >1):   print "handling motorsMode STOP"
      if (self.debugLevel >1):   print "controlStop:",datetime.datetime.now()
      self._currentSpeed = self.rampTgtCurStep(0, 
                                         self._currentSpeed, 
                                         self.rampStep)
      
      if self.lastMotorsMode in (Motors.DRIVE, Motors.TRAVEL):
          lPwr,rPwr = self.speed2Pwr(self._currentSpeed,0)  # (drive,spin)
      elif self.lastMotorsMode in (Motors.SPIN, Motors.TURN):
          lPwr,rPwr = self.speed2Pwr(0,self._currentSpeed)  # (drive,spin)
      else:           # Handle stopping from all other modes
          lPwr = 0
          rPwr = 0
      self.setMotorsPwr(lPwr,rPwr)  # pwrs=(lPwr,rPwr)

      if (self._currentSpeed == 0): self.motorsMode=Motors.STOPPED
      return

  def controlStopped(self):
      #if (self.debugLevel >1):   print "handling motorsMode STOPPED"
      #if (self.debugLevel >1):   print "controlStopped:",datetime.datetime.now()
      pass
      return
  

  def control(self):  #CONTROL THE MOTORS 
       if (self.debugLevel >1):   print ("motorsMode: %s " % (self.Modes2Str[self.motorsMode]))
       if (self.debugLevel >1):   print ("driveSpeed: %s:%d spinSpeed: %s:%d currentSpeed: %d" % (self.SpeedsToStr[self.driveSpeed], self.driveSpeed, self.SpeedsToStr[self.spinSpeed], self.spinSpeed,self._currentSpeed ) )
       if (self.debugLevel >1):   print ("driveDist : %.1f currentDist: %.1f" % (self.driveDistance,self.currentDistance) )
       if (self.debugLevel >1):   print ("turnDir   : %d " % self.turnDir)

       if (self.motorsMode == Motors.DRIVE):    self.controlDrive()
       elif (self.motorsMode == Motors.TRAVEL): self.controlTravel()
       elif (self.motorsMode == Motors.SPIN):   self.controlSpin()
       elif (self.motorsMode == Motors.TURN):   self.controlTurn()
       elif (self.motorsMode == Motors.STOP):   self.controlStop()
       elif (self.motorsMode == Motors.STOPPED):self.controlStopped()
       else:
           if (self.debugLevel >1):   print "handling motorsMode else"
         
       return   

  def setup_motor_pins(self):
    PDALib.pinMode(Motors.RMotor,PDALib.PWM)  # init motor1 speed control pin
    PDALib.pinMode(Motors.LMotor,PDALib.PWM)  # init motor2 speed control pin 

    PDALib.pinMode(Motors.M1DirA,PDALib.OUTPUT)  #init motor1 dirA/Fwd    enable
    PDALib.pinMode(Motors.M1DirB,PDALib.OUTPUT)  #init motor1 dirB/Bkwd  enable
    PDALib.pinMode(Motors.M2DirA,PDALib.OUTPUT)  #init motor2 dirA/Fwd    enable
    PDALib.pinMode(Motors.M2DirB,PDALib.OUTPUT)  #init motor2 dirB/Bkwd  enable

  def motors_off(self):
    # two ways to stop - set speed to 0 or set direction to off/coast 
    self.spinSpeed =Motors.NONE
    self.driveSpeed =Motors.NONE

    # turn off the speed pins
    PDALib.analogWrite(Motors.RMotor,0)  #set motor1 to zero speed 
    PDALib.analogWrite(Motors.LMotor,0)  #set motor2 to zero speed

  
    # all direction pins to off
    PDALib.digitalWrite(Motors.M1DirA,0)  #set to off/coast
    PDALib.digitalWrite(Motors.M1DirB,0)  #set to off/coast
    PDALib.digitalWrite(Motors.M2DirA,0)  #set to off/coast
    PDALib.digitalWrite(Motors.M2DirB,0)  #set to off/coast


    self.motorsMode = Motors.STOPPED

  def motors_fwd(self):
    motors_off()
    PDALib.digitalWrite(Motors.M1DirA,1)  #rt set to forward
    PDALib.digitalWrite(Motors.M2DirA,1)  #lft set to forward

  def motors_bwd(self):
    motors_off()
    PDALib.digitalWrite(Motors.M1DirB,1)  #rt set to backward
    PDALib.digitalWrite(Motors.M2DirB,1)  #lft set to backward

  def motors_ccw(self):
    motors_off()
    PDALib.digitalWrite(Motors.M1DirA,1)  #R set to forward
    PDALib.digitalWrite(Motors.M2DirB,1)  #L set to backward

  def motors_cw(self):
    motors_off()
    PDALib.digitalWrite(Motors.M1DirB,1)  #R set to backward
    PDALib.digitalWrite(Motors.M2DirA,1)  #L set to forward

  #   drive(Motors.SPEED) # ramp speed to go fwd(+) or back(-) at 0-100%
  def drive(self,speed):
      self.motorsMode  = Motors.DRIVE
      self.spinSpeed   = self.NONE
      self.driveDistance = 0
      self.driveSpeed    = speed
      return

  #   travel(distance.inInches, Motors.SPEED)  # go fwd (+) or back (-) a distance
  def travel(self,distance, speed=MEDIUM):
      self.motorsMode = Motors.TRAVEL
      self.spinSpeed =self.NONE
      self.driveDistance = distance
      encoders.reset()
      self.setInitialCounts()
      self.driveSpeed = speed * sign(distance)
      if (self.debugLevel >0):  print ("starting travel %.1f at %d" % (distance, speed))
      return

  #   spin(Motors.SPEED)  # ramp spin speed to go ccw(+) or cw(-) at 0-100%
  def spin(self, speed):
      self.motorsMode = Motors.SPIN
      self.driveSpeed = Motors.NONE
      self.driveDistance  = 0
      self.spinSpeed = speed
      return

  #   turn(Motors.DIRECTION) # Turn to direction in degrees
  def turn(self, direction):
      self.motorsMode     = Motors.TURN
      self.driveSpeed     = Motors.NONE
      self.driveDistance  = 0
      self.turnDir        = direction
      self.spinSpeed      = Motors.MEDIUM * sign(direction)
      return

  #   stop()  # come to graceful stop
  def stop(self):  # don't change mode, just bring speed to 0
      self.spinSpeed     = Motors.NONE
      self.driveSpeed    = Motors.NONE
      self.driveDistance = 0
      self.lastMotorsMode = self.motorsMode
      self.motorsMode    = Motors.STOP
      return

  #   halt()  # immediate stop
  def halt(self):
      self.motors_off()
      self.spinSpeed     = Motors.NONE
      self.driveSpeed    = Motors.NONE
      self.driveDistance = 0
      self.motorsMode    = Motors.STOPPED
      return

  #   calibrate()        # find minFwdDrive, minBwdDrive, minCCWDrive, minCWDrive, biasFwd, biasBwd
  def calibrate(self):
      if (self.debugLevel >0):  print "Calibrate() Started"
      time.sleep(1)
      if (self.debugLevel >0):  print "Calibrate minFwdDrive, minBwdDrive"
      time.sleep(1)
      if (self.debugLevel >0):  print "Calibrate minCCWDrive, minCWDrive"
      time.sleep(1)
      if (self.debugLevel >0):  print "Calibrate biasFwd, biasBwd"
      time.sleep(1)

      if (self.debugLevel >0):  print "\n"
      if (self.debugLevel >0):  print "*******************"
      if (self.debugLevel >0):  print "Calibration Results"
      if (self.debugLevel >0):  print ("minFwdDrive: %d  minBwdDrive: %d" % (self.minFwdDrive, self.minBwdDrive))
      if (self.debugLevel >0):  print ("minCCWDrive: %d  minCWDrive:  %d" % (self.minCCWDrive, self.minCWDrive))
      if (self.debugLevel >0):  print ("biasFwd: %d  biasBwd: %d" % (self.biasFwd, self.biasBwd))
      if (self.debugLevel >0):  print "Done"
      return


  def cancel(self):
     print "Motors.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for Motors.control Thread to quit"
     self.pollThreadHandle.join()
     self.halt()

  def waitForStopped(self, timeout=60):
     if (self.debugLevel >0):  print ("waitForStopped or %.1f" % timeout)
     tWaitForModeChange = 2*Motors.tSleep
     time.sleep(tWaitForModeChange)
     timeout_delta=datetime.timedelta(seconds=int(timeout))
     timeoutTime = datetime.datetime.now()+timeout_delta

     while ((datetime.datetime.now() < timeoutTime) and (self.motorsMode != Motors.STOPPED)):
         time.sleep(tWaitForModeChange)


# ##### LOW LEVEL MOTOR METHODS
#   setMotorsPwr(lPwr,rPwr)           # Pwr:+/- 0-255 
  def setMotorsPwr(self,lPwr,rPwr):

    if (lPwr>0):
      PDALib.digitalWrite(Motors.M2DirA,1)  #lft set to forward
      PDALib.digitalWrite(Motors.M2DirB,0)  #set to off/coast

    elif (lPwr<0):
      PDALib.digitalWrite(Motors.M2DirA,0)  #set to off/coast
      PDALib.digitalWrite(Motors.M2DirB,1)  #lft set to backward

    else:
      PDALib.digitalWrite(Motors.M2DirA,0)  #set to off/coast
      PDALib.digitalWrite(Motors.M2DirB,0)  #set to off/coast

    if (rPwr>0):
      PDALib.digitalWrite(Motors.M1DirA,1)  #rt set to forward
      PDALib.digitalWrite(Motors.M1DirB,0)  #set to off/coast

    elif (rPwr<0):
      PDALib.digitalWrite(Motors.M1DirA,0)  #set to off/coast
      PDALib.digitalWrite(Motors.M1DirB,1)  #rt set to backward

    else:
      PDALib.digitalWrite(Motors.M1DirA,0)  #set to off/coast
      PDALib.digitalWrite(Motors.M1DirB,0)  #set to off/coast

    # Now power the motors
    if (self.debugLevel >1):   print ("setMotorsPwr(lPwr:%d,rPwr:%d) %s" % (lPwr,rPwr,datetime.datetime.now()))
    PDALib.analogWrite(Motors.LMotor,abs(lPwr))  #set lft motor2
    PDALib.analogWrite(Motors.RMotor,abs(rPwr))  #set rt motor1 

# end setMotorsPwr()

# ##### Motors CLASS TEST METHOD ######
# the first time through the main() while loop, the sensors may not have been read yet
#     so Motors.status() and each Motors may have a value of 8/UNKNOWN 

def main():
  # note: lowercase Motors is object, uppercase Motors is class (everywhere in code)

  motors=Motors(readingsPerSec=10)  #create instance and control Motors thread


  myPyLib.set_cntl_c_handler(motors.cancel)  # Set CNTL-C handler 
  try:
    print "\n"

# ##### TEST rampTgtCurStep()

#    motors.rampTgtCurStep(0, 0, 30)

#    motors.rampTgtCurStep(100, -100, 30)
#    motors.rampTgtCurStep(100, -50, 30)
#    motors.rampTgtCurStep(100, 0, 30)
#    motors.rampTgtCurStep(100, 50, 30)
#    motors.rampTgtCurStep(100, 80, 30)

#    motors.rampTgtCurStep(-100, 100, 30)
#    motors.rampTgtCurStep(-100, 10, 30)
#    motors.rampTgtCurStep(-100, 0, 30)
#    motors.rampTgtCurStep(-100, -50, 30)
#    motors.rampTgtCurStep(-100, -80, 30)

#    motors.rampTgtCurStep(0, -100, 30)
#    motors.rampTgtCurStep(0, -10, 30)
#    motors.rampTgtCurStep(0, +10, 30)

#    motors.rampTgtCurStep(50, -100, 30)
#    motors.rampTgtCurStep(50, 40, 30)
#    motors.rampTgtCurStep(50, 60, 30)

#    motors.rampTgtCurStep(-50, 100, 30)
#    motors.rampTgtCurStep(-50, -40, 30)
#    motors.rampTgtCurStep(-50, -60, 30)

    

# ######## TEST calibrate()
#    motors.calibrate()

# ######## TEST spin()
    print "TEST SPIN"
    motors.spin(Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    print "spin(SLOW)"
    motors.spin(Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)


    print "spin(-FAST)"
    motors.spin(-Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    motors.spin(-Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)

# ###### TEST drive()
    print "TEST DRIVE"
    motors.drive(Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    motors.drive(-Motors.SLOW)
    time.sleep(5)
    motors.stop()
    time.sleep(3)


    
    motors.drive(Motors.MEDIUM)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    motors.drive(-Motors.MEDIUM)
    time.sleep(5)
    motors.stop()
    time.sleep(3)

 
    motors.drive(Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
    motors.drive(-Motors.FAST)
    time.sleep(5)
    motors.stop()
    time.sleep(3)
   
# ####### TEST travel()
    print "TEST TRAVEL FWD 6.0 inches:", datetime.datetime.now()
    motors.travel(6.0, Motors.MEDIUM)
    time.sleep(5.0)

    print "TEST TRAVEL BWD(-) 6.0 inches:", datetime.datetime.now()
    motors.travel(-6.0, Motors.MEDIUM)
    time.sleep(5.0)

# ####### TEST turn()
    print "TEST TURNS"
    trn1=Motors.CCW90
    trn2=Motors.CW180
    trn3=Motors.CCW90
    motors.turn(trn1)
    time.sleep(5)
    motors.turn(trn2)
    time.sleep(5)
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


