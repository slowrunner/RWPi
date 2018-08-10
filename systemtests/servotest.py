#!/usr/bin/python
#
# encoders.py   ENCODERS TEST
#
# 10Jun2016 - file header added

import PDALib
import time
import sys
import signal



ServoDwellTime = 0.2  #seconds to stay at each position

TILTSERVO = 0
PANSERVO = 1

ServoStep = 10  # must be integer for range func

PanLimitL = 2000 # 2500
PanCenter = 1480 # 1535
PanLimitR = 1000 # 630

TiltLimitUp = 600 #550
TiltCenter = 1320 # 1375
TiltLimitDn = 1750 # 2435


def setup_servo_pins():
  PDALib.pinMode(Tilt,PDALib.SERVO)    # init Tilt servo pin to SERVO mode
  PDALib.pinMode(Pan,PDALib.SERVO )  # init motor2 speed control pin

def center_servos():
  PDALib.servoWrite(TILTSERVO, TiltCenter)
  PDALib.servoWrite(PANSERVO, PanCenter)


# ################## CONTROL-C HANDLER
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  print "Servos to Center For Exit"
  center_servos()
  PDALib.LibExit()
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)
# ##################

center_servos()
print "Servos Centered"

for panpos in range(PanCenter,PanLimitL+1, ServoStep ):   # move from center to full left
    PDALib.servoWrite(PANSERVO,panpos)                    # set to new position
    print "pan: ",panpos,"current:",PDALib.analogRead(7)*5.0/1023*0.185*1000.0
    time.sleep(ServoDwellTime)

print "At left limit"
time.sleep(2)

for panpos in range(PanLimitL,PanLimitR-1, -ServoStep ):   # move from full left to full right
    PDALib.servoWrite(PANSERVO,panpos)                 # set to new position
    print "pan: ",panpos,"current:",PDALib.analogRead(7)*5.0/1023*0.185*1000.0
    time.sleep(ServoDwellTime)

print "At right limit"
time.sleep(2)

for panpos in range(PanLimitR, PanCenter, ServoStep ):   # move from full right to center
    PDALib.servoWrite(PANSERVO,panpos)                 # set to new position
    print "pan: ",panpos,"current:",PDALib.analogRead(7)*5.0/1023*0.185*1000.0
    time.sleep(ServoDwellTime)

print "At center"
time.sleep(2)


for tiltpos in range(TiltCenter,TiltLimitUp-1, -ServoStep ):   # move from center to full up
    PDALib.servoWrite(TILTSERVO,tiltpos)                      # set to new position
    print "tilt: ",tiltpos,"current:",PDALib.analogRead(7)*5.0/1023*0.185*1000.0
    time.sleep(ServoDwellTime)

print "At full up"
time.sleep(2)

for tiltpos in range(TiltLimitUp,TiltLimitDn+1,ServoStep ):   # move from full up to full down
    PDALib.servoWrite(TILTSERVO, tiltpos)                 # set to new position
    print "tilt: ",tiltpos,"current:",PDALib.analogRead(7)*5.0/1023*0.185*1000.0
    time.sleep(ServoDwellTime)

print "At full down"
time.sleep(2)

for tiltpos in range(TiltLimitDn, TiltCenter, -ServoStep ):   # move from full down back to center
    PDALib.servoWrite(TILTSERVO, tiltpos)                     # set to new position
    print "tilt: ",tiltpos,"current:",PDALib.analogRead(7)*5.0/1023*0.185*1000.0
    time.sleep(ServoDwellTime)

print "At center"
time.sleep(2)

center_servos()
