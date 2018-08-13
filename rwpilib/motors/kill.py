#!/usr/bin/python
#
# kill.py   KILL MOTORS
#
import sys
sys.path.append("/home/pi/RWPi/rwpilib")

import PDALib
import myPDALib

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

# turn off the speed pin - not needed when dir pins are off, but good idea
PDALib.analogWrite(RMotor,0)  #set motor1 to zero speed 
PDALib.analogWrite(LMotor,0)  #set motor2 to zero speed

myPDALib.PiExit()
