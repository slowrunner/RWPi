#!/usr/bin/python
#
# center.py   Center servos 
#

import PDALib
import time

ServoDwellTime = 0.01  #seconds to stay at each position

TILTSERVO = 0
PANSERVO = 1

PanLimitL = 2500
PanCenter = 1500
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


setup_servo_pins()
center_servos()
time.sleep(1.0)
#servos_off()  # only costs a few mA to leave on, and no issue with motors if on.
print "Servos Centered"
