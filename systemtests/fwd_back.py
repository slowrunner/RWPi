#!/usr/bin/python
#
# fwd_back2.py   FORWARD AND BACK MOTOR TEST
#
# 10Jun2016 - changed pins for PDALib v0.93
# Drive forward five seconds, pause 5s, drive back 5s
# With empirical bias number

import PDALib
import time
import sys
import signal


# ################# MOTOR TEST ###########

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



MotorRampTime = 1.0  #seconds to reach set speed
DriveTime = 4.0      #seconds to drive at set speed

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

# compute motor bias based on startup
MotorBiasF = RMotorMinF-LMotorMinF 
MotorBiasB = RMotorMinB-LMotorMinB 

# disable computed motor bias and use empirical bias
MotorBiasF = 0
MotorBiasB = -6   # positive anti-cw , negative anti-ccw

if MotorBiasF >0:   # Right takes more so will need to reduce left 
  LMotorBiasF = MotorBiasF  
  RMotorBiasF = 0
  MinMotorsF  = RMotorMinF
else:               # Left takes more so will need to reduce right
  LMotorBiasF = 0
  RMotorBiasF = -MotorBiasF
  MinMotorsF = LMotorMinF

if MotorBiasB >0:   # Right takes more so will need to reduce left 
  LMotorBiasB = MotorBiasB  
  RMotorBiasB = 0
  MinMotorsB  = RMotorMinB
else:               # Left takes more so will need to reduce right
  LMotorBiasB = 0
  RMotorBiasB = -MotorBiasB
  MinMotorsB = LMotorMinB


MaxMotorsF= 255
MaxMotorsB= 255

# ################## CONTROL-C HANDLER
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  print '\n** STOPPING MOTORS **' 
  motors_off()
  print 'bye bye'
  PDALib.LibExit()
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

def motors_fwd():
  motors_off()
  PDALib.digitalWrite(M1DirA,1)  #set to forward
  PDALib.digitalWrite(M2DirA,1)  #set to forward

def motors_bwd():
  motors_off()
  PDALib.digitalWrite(M1DirB,1)  #set to forward
  PDALib.digitalWrite(M2DirB,1)  #set to forward

ACS712PIN = 7
def current_sense():   
    # Sensor puts out 0.185V/A around 2.5v
    #
    #   5000mV          1A        1000A
    #  --ADC---- *   -Sensor-  *  -----  = 26.39358 mA per reading bit
    #   1024           185mV        1A                 around 512
    zero_current = 514.00
    values = []
    for i in range(0,10):
      values.append(PDALib.analogRead(ACS712PIN))
    values.sort()
    middle = values[4:6]
    median = sum(middle) / float(len(middle)) # median 
    average = sum(values) / float(len(values)) # average
    # print("average current %.0f" % ((zero_current - average)*26.39358))
    # print("median current %.0f" % ((zero_current - median)*26.39358))
    pin_value = average  
    current_now = (zero_current - pin_value)*26.39358
    return [round(current_now), int(pin_value)]
  

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


signal.signal(signal.SIGINT, signal_handler)

# setup_servo_pins()
# center_servos()
setup_motor_pins()
motors_off()

# get ready to go forward
motors_fwd()

RampStep = 10  # must be integer for range func
delayTime=(MotorRampTime/((MaxMotorsF+1 - MinMotorsF)/RampStep))
print "delayTime: ",delayTime

for speed in range(MinMotorsF,MaxMotorsF+1,RampStep):   # range goes up to but not including
  PDALib.analogWrite(RMotor,speed-RMotorBiasF)  #set motor1 to desired speed 
  PDALib.analogWrite(LMotor,speed-LMotorBiasF)  #set motor2 to desired speed
  print "speed: ",speed
  print "current:",current_sense()
  time.sleep(delayTime)  

print "At max speed"
for i in range(0,int(DriveTime)):
  print "current:",current_sense()
  time.sleep(1.0)  # drive while asleep at the wheel 
                           # (bad idea but this is a test)
motors_off()
print "Motors Off"


# ---- Just sit for a while ----
time.sleep(3.0)
print "current:",current_sense()
time.sleep(2.0)

# ---- Now drive backward -----

RampStep = 10  # must be integer for range func
MotorRampTIme = 1.0
delayTime=(MotorRampTime/((MaxMotorsB+1 - MinMotorsB)/RampStep))

print "delayTime: ",delayTime

motors_bwd()

for speed in range(MinMotorsB,MaxMotorsB+1,RampStep):   # range goes up to but not including
  PDALib.analogWrite(RMotor,speed-RMotorBiasB)  #set motor1 to desired speed 
  PDALib.analogWrite(LMotor,speed-LMotorBiasB)  #set motor2 to desired speed
  print "speed: ",speed
  time.sleep(delayTime)  

print "At max speed"
time.sleep(int(DriveTime))  # drive while asleep at the wheel for 10 seconds 
                           # (bad idea but this is a test)
motors_off()
