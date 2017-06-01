#!/usr/bin/python
#
# center2.py   Center servos and measure current 
#

import PDALib
import time
import currentsensor


ServoDwellTime = 0.01  #seconds to stay at each position

TILTSERVO = 0
PANSERVO = 1

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

print ("\ncurrent: %.0f \n" % currentsensor.current_sense3())
print "setup_servo_pins()"
setup_servo_pins()
time.sleep(0.2)
print ("\ncurrent: %.0f \n" % currentsensor.current_sense3())
print "center_servos()"
center_servos()
time.sleep(1.0)
n=0
values=0
for i in range(1,100):
  n+=1
  values += currentsensor.current_sense()
ave_current = values / n
print "servos at rest"
print ("ave current: %.0f" % ave_current)
print ("\ncurrent: %.0f \n" % currentsensor.current_sense3())
print "servos_off()"
servos_off()
print "Servos Centered and off"
time.sleep(0.2)
print ("\ncurrent: %.0f \n" % currentsensor.current_sense3())
n=0
values=0
for i in range(1,100):
  n += 1
  values += currentsensor.current_sense()
ave_current=values / n
print ("ave current: %.0f" % ave_current)
print ("\ncurrent: %.0f \n" % currentsensor.current_sense3())
print "Done"

