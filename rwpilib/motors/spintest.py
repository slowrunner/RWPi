#!/usr/bin/python
#
# spintest.py   SPIN TEST
#
# spin ccw five seconds, pause 5s, spin cw 5s
# With empirical bias number

import PDALib
import myPDALib
import time
import sys
import signal
import currentsensor

# ################# SPIN TEST ###########

# Motor Pins 
# SRV 6		Right Motor (Motor 1) Speed (PWM)
# SRV 7		Left Motor  (Motor 2) Speed (PWM)
RMotor = 6	
LMotor = 7

# DIO 12 (A4)	Motor 1 Dir A (0=coast 1=F/Brake)
# DIO 13 (A5)	Motor 1 Dir B (0=coast 1=R/Brake)

# DIO 14 (A6)	Motor 2 Dir A (0=coast 1=F/Brake)
# DIO 15 (A7)	Motor 2 Dir B (0=coast 1=R/Brake)

M1DirA = 12
M1DirB = 13
M2DirA = 14
M2DirB = 15



MotorRampTime = 0.25 #  1.0   #seconds to reach set speed
DriveTime360 = 2.13     #  1.85      #seconds to drive at set speed
DriveTime180 = DriveTime360 / 2.15
DriveTime90  = DriveTime180 / 2.25
DriveTime45  = DriveTime90 / 2.2


# Empirical settings for minimum drive to turn each wheel
# PWM_frequency dependent, PiDALib default is 490
# PWM_f   RMotorMinF   LMotorMinF
# 10000   215           185
# 490	  83		73  <--
# 100	  34		33
# 33	  22		20

RMotorMinF = 83  # no load (takes more to get right going reliably)
LMotorMinF = 73  # no load 
RMotorMinB = 94  # no load (takes more to get right going reliably)
LMotorMinB = 86  # no load 

# compute motor bias based on startup (amount of right more than left needed)
#MotorBiasF = RMotorMinF-LMotorMinF   # = +10 
#MotorBiasB = RMotorMinB-LMotorMinB   # = +8
MotorBiasCW = RMotorMinB-LMotorMinF   # = +21
MotorBiasCCW = RMotorMinF-LMotorMinB  # = -3

# modify computed motor bias
# MotorBiasCW += 1
# MotorBiasCCW = 0   # positive anti-cw , negative anti-ccw

if MotorBiasCW >0:   # Right takes more so will need to reduce left 
  LMotorBiasCW = MotorBiasCW  
  RMotorBiasCW = 0
  MinMotorsCW  = RMotorMinB
else:               # Left takes more so will need to reduce right
  LMotorBiasCW = 0
  RMotorBiasCW = -MotorBiasCW
  MinMotorsCW = LMotorMinF

if MotorBiasCCW >0:   # Right takes more so will need to reduce left 
  LMotorBiasCCW = MotorBiasCCW  
  RMotorBiasCCW = 0
  MinMotorsCCW  = RMotorMinF
else:               # Left takes more so will need to reduce right
  LMotorBiasCCW = 0
  RMotorBiasCCW = -MotorBiasCCW
  MinMotorsCCW = LMotorMinB


MaxMotors= 255
MinMotors= 0   # variable
RMotorBias = 0 # variable
LMotorBias = 0 # variable

# ################## CONTROL-C HANDLER
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  print '\n** STOPPING MOTORS **' 
  motors_off()
  print 'bye bye'
  myPDALib.PiExit()
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)
# ##################


def setup_motor_pins():
  PDALib.pinMode(RMotor,PDALib.PWM)  # init motor1 speed control pin
  PDALib.pinMode(LMotor,PDALib.PWM)  # init motor2 speed control pin 

  PDALib.pinMode(M1DirA,PDALib.OUTPUT)  #init motor1 dirA/Fwd    enable
  PDALib.pinMode(M1DirB,PDALib.OUTPUT)  #init motor1 dirB/Bkwd  enable
  PDALib.pinMode(M2DirA,PDALib.OUTPUT)  #init motor2 dirA/Fwd    enable
  PDALib.pinMode(M2DirB,PDALib.OUTPUT)  #init motor2 dirB/Bkwd  enable


def motors_off():
  # two ways to stop - set speed to 0 or set direction to off/coast 
  
  # all direction pins to off
  PDALib.digitalWrite(M1DirA,0)  #set to off/coast
  PDALib.digitalWrite(M1DirB,0)  #set to off/coast
  PDALib.digitalWrite(M2DirA,0)  #set to off/coast
  PDALib.digitalWrite(M2DirB,0)  #set to off/coast

  # turn off the speed pin - not needed when dir pins are off, but good idea
  PDALib.analogWrite(RMotor,0)  #set motor1 to zero speed 
  PDALib.analogWrite(LMotor,0)  #set motor2 to zero speed

CCW = 1
CW  = -1

def spin_ccw():
  motors_off()
  PDALib.digitalWrite(M1DirA,1)  #set to forward
  PDALib.digitalWrite(M2DirB,1)  #set to backward
  spin_dir=CCW
  MinMotors=MinMotorsCCW
  LMotorBias=LMotorBiasCCW
  RMotorBias=RMotorBiasCCW

def spin_cw():
  motors_off()
  PDALib.digitalWrite(M1DirB,1)  #set to backward
  PDALib.digitalWrite(M2DirA,1)  #set to forward
  spin_dir=CW
  MinMotors=MinMotorsCW
  LMotorBias=LMotorBiasCW
  RMotorBias=RMotorBiasCW

TILTSERVO = 0
PANSERVO = 1

ServoStep = 10  # must be integer for range func

PanLimitL = 2500
PanCenter = 1535
PanLimitR = 630

TiltLimitUp = 550
TiltCenter = 1375
TiltLimitDn = 2435


def setup_servo_pins():
  PDALib.pinMode(TILTSERVO,PDALib.SERVO)    # init Tilt servo pin to SERVO mode
  PDALib.pinMode(PANSERVO,PDALib.SERVO )  # init motor2 speed control pin

def center_servos():
  PDALib.servoWrite(TILTSERVO, TiltCenter)
  PDALib.servoWrite(PANSERVO, PanCenter)

def servos_off():
  PDALib.pinMode(TILTSERVO,PDALib.INPUT)    # init Tilt servo off
  PDALib.pinMode(PANSERVO,PDALib.INPUT)     # init motor2 servo off


signal.signal(signal.SIGINT, signal_handler)

setup_servo_pins()
center_servos()
time.sleep(1.0)
# servos_off()

setup_motor_pins()
motors_off()


def ramp_speed():
  RampStep = 10  # must be integer for range func
  delayTime=(MotorRampTime/((MaxMotors+1 - MinMotors)/RampStep))
#  print "delayTime: ",delayTime

  for speed in range(MinMotors,MaxMotors+1,RampStep):   # range goes up to but not including
    PDALib.analogWrite(RMotor,speed-RMotorBias)  #set motor1 to desired speed 
    PDALib.analogWrite(LMotor,speed-LMotorBias)  #set motor2 to desired speed
#    print ("speed: %d" % speed )
#    print ("speed: %d current: %.0f" % (speed, currentsensor.current_sense() ))
    time.sleep(delayTime)  

#  print "At max speed"
  for i in range(0,int(DriveTime)):
    print ("current: %.0f" % currentsensor.current_sense())
    time.sleep(1.0)  # spin
  FractionalTime = DriveTime % 1
  if (FractionalTime > 0.01):
    time.sleep(FractionalTime) 

DriveTime=DriveTime360
# get spin for DriveTime
print "Spin360"
spin_ccw()
ramp_speed()
motors_off()
print "Motors Off"
# ---- Just sit for a while ----
time.sleep(3.0)
print ("\ncurrent: %.0f \n" % currentsensor.current_sense())
time.sleep(2.0)
# ---- Now spin clockwise -----
spin_cw()
ramp_speed()
motors_off()
print "Motors Off"
print ("current: %.0f" % currentsensor.current_sense())

time.sleep(5.0)

## 180 and back
print "Spin 180"
DriveTime=DriveTime180
spin_ccw()
ramp_speed()
motors_off()
time.sleep(1.0)
spin_cw()
ramp_speed()
motors_off()

time.sleep(5.0)

spin_cw()
ramp_speed()
motors_off()

time.sleep(1.0)

spin_ccw()
ramp_speed()
motors_off()

time.sleep(5.0)

## 90 and back
print "Spin 90"
DriveTime=DriveTime90
spin_ccw()
ramp_speed()
motors_off()

time.sleep(1.0)

spin_cw()
ramp_speed()
motors_off()

time.sleep(5.0)

spin_cw()
ramp_speed()
motors_off()

time.sleep(1.0)

spin_ccw()
ramp_speed()
motors_off()

time.sleep(5.0)

## spin 45 and back
print "Spin 45"
DriveTime=DriveTime45
spin_ccw()
ramp_speed()
motors_off()

time.sleep(1.0)

spin_cw()
ramp_speed()
motors_off()

time.sleep(5.0)

spin_cw()
ramp_speed()
motors_off()

time.sleep(1.0)

spin_ccw()
ramp_speed()
motors_off()

print "\nDone\n"

myPDALib.PiExit()
