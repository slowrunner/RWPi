#!/usr/bin/python
#
# motortest.py   MOTOR TEST
#
# 10Jun2016 - changed pins for PDALib v0.93

import PDALib
import time
import sys
import signal

# ################# MOTOR TEST ###########

# Motor Pins 
# SRV 6		Motor 1 Speed (PWM)
# SRV 7		Motor 2 Speed (PWM)
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

# ################## CONTROL-C HANDLER
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  print '\n** STOPPING MOTORS **' 
  PDALib.analogWrite(RMotor,0)  #set motor1 to zero speed 
  PDALib.analogWrite(LMotor,0)  #set motor2 to zero speed
  print 'bye bye'
  PDALib.LibExit()
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)
# ##################





PDALib.pinMode(RMotor,PDALib.PWM)  # init motor1 speed control pin
PDALib.pinMode(LMotor,PDALib.PWM)  # init motor2 speed control pin 

PDALib.pinMode(M1DirA,PDALib.OUTPUT)  #init motor1 dirA/Fwd    enable
PDALib.pinMode(M1DirB,PDALib.OUTPUT)  #init motor1 dirB/Bkwd  enable
PDALib.pinMode(M2DirA,PDALib.OUTPUT)  #init motor2 dirA/Fwd    enable
PDALib.pinMode(M2DirB,PDALib.OUTPUT)  #init motor2 dirB/Bkwd  enable

# init all direction pins to off
PDALib.digitalWrite(M1DirA,0)  #set to off/coast
PDALib.digitalWrite(M1DirB,0)  #set to off/coast
PDALib.digitalWrite(M2DirA,0)  #set to off/coast
PDALib.digitalWrite(M2DirB,0)  #set to off/coast

# get ready to go forward
PDALib.digitalWrite(M1DirA,1)  #set to forward
PDALib.digitalWrite(M2DirA,1)  #set to forward

# setting speed will start us going  (zero to fast in one command for this test)
PDALib.analogWrite(RMotor,200)  #set motor1 speed 
PDALib.analogWrite(LMotor,200)  #set motor2 speed

time.sleep(4.0)  # drive while asleep at the wheel (seconds) 
                           # (bad idea but this is a test)

# two ways to stop - set speed to 0 or set direction to off/coast 
PDALib.digitalWrite(M1DirA,0)  #set to off/coast to stop
PDALib.digitalWrite(M2DirA,0)  #set to off/coast to stop

# turn off the speed pin - not needed when dir pins are off, but good idea
PDALib.analogWrite(RMotor,0)  #set motor1 to zero speed 
PDALib.analogWrite(LMotor,0)  #set motor2 to zero speed
