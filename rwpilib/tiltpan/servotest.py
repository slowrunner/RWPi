#!/usr/bin/python
#
# servotest.py   SG90 SERVO TEST
#
# 10Jun2016 - file header added
# SG90 Micro Servo

# It fit for most brands of radio equipment including Hitec, Futaba, GWS, JR, Sanwa

#Specification :

#* Weight : 9 g

#* Size : 22 x 11.5 x 27 mm

#* Operating Speed (4.8V no load): 0.12sec/60 degrees 
#* Stall Torque (4.8V): 17.5oz/in (1.2 kg/cm)

#* Temperature Range: -30 to +60 Degree C
#* Dead Band Width: 7usec
#Operating Voltage:3.0-7.2 Volts

#Features :
#- Coreless Motor
#- All Nylon Gear
#- Connector Wire Length 150MM

import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import PDALib
import myPDALib
import myPyLib
import time
import currentsensor


ServoDwellTime = 0.01  #seconds to stay at each position

TILTSERVO = 0
PANSERVO = 1

ServoStep = 10  # must be integer for range func

PanLimitL = 2400
PanCenter = 1450
PanLimitR =  600

TiltLimitUp = 500
TiltCenter = 1400
TiltLimitDn = 1900


def setup_servo_pins():
  PDALib.pinMode(Tilt,PDALib.SERVO)    # init Tilt servo pin to SERVO mode
  PDALib.pinMode(Pan,PDALib.SERVO )  # init motor2 speed control pin

def center_servos():
  PDALib.servoWrite(TILTSERVO, TiltCenter)
  PDALib.servoWrite(PANSERVO, PanCenter)

def servos_off():
  PDALib.pinMode(TILTSERVO,PDALib.INPUT)    # init Tilt servo off
  PDALib.pinMode(PANSERVO,PDALib.INPUT)     # init motor2 servo off




# ### TEST SERVOS

myPyLib.set_cntl_c_handler(servos_off)  # Set CNTL-C handler 


center_servos()
time.sleep(1.0)
#servos_off()
print "Servos Centered and off"
time.sleep(1.0)
current_now = currentsensor.current_sense(10)
print "nominal current: %.0f" %  current_now
time.sleep(5.0)

for panpos in range(PanCenter,PanLimitL+1, ServoStep ):   # move from center to full left
    PDALib.servoWrite(PANSERVO,panpos)                    # set to new position
    current_now = currentsensor.current_sense(4)
    print "pan: %d current: %.0f" % (panpos, current_now)
    time.sleep(ServoDwellTime)

print "At left limit"
time.sleep(1)
print "current: %.0f mA" % currentsensor.current_sense(10)
time.sleep(1)

for panpos in range(PanLimitL,PanLimitR-1, -ServoStep ):   # move from full left to full right
    PDALib.servoWrite(PANSERVO,panpos)                 # set to new position
    current_now = currentsensor.current_sense(4)
    print "pan: %d current: %.0f" % (panpos, current_now)
    time.sleep(ServoDwellTime)

print "At right limit"
time.sleep(1)
print "current: %.0f mA" % currentsensor.current_sense(10)
time.sleep(1)

for panpos in range(PanLimitR, PanCenter, ServoStep ):   # move from full right to center
    PDALib.servoWrite(PANSERVO,panpos)                 # set to new position
    current_now = currentsensor.current_sense(4)
    print "pan: %d current: %.0f" % (panpos, current_now)
    time.sleep(ServoDwellTime)

print "At center"
time.sleep(1)
print "current: %.0f mA" % currentsensor.current_sense(10)
time.sleep(1)


for tiltpos in range(TiltCenter,TiltLimitUp-1, -ServoStep ):   # move from center to full up
    PDALib.servoWrite(TILTSERVO,tiltpos)                      # set to new position
    current_now = currentsensor.current_sense(4)
    print "tiltpos: %d current: %.0f" % (tiltpos, current_now)
    time.sleep(ServoDwellTime)

print "At full up"
time.sleep(1)
print "current: %.0f mA" % currentsensor.current_sense(10)
time.sleep(1)

for tiltpos in range(TiltLimitUp,TiltLimitDn+1,ServoStep ):   # move from full up to full down
    PDALib.servoWrite(TILTSERVO, tiltpos)                 # set to new position
    current_now = currentsensor.current_sense(4)
    print "tiltpos: %d current: %.0f" % (tiltpos, current_now)
    time.sleep(ServoDwellTime)

print "At full down"
time.sleep(1)
print "current: %.0f mA" % currentsensor.current_sense(10)
time.sleep(1)

for tiltpos in range(TiltLimitDn, TiltCenter, -ServoStep ):   # move from full down back to center
    PDALib.servoWrite(TILTSERVO, tiltpos)                     # set to new position
    current_now = currentsensor.current_sense(4)
    print "tiltpos: %d current: %.0f" % (tiltpos, current_now)
    time.sleep(ServoDwellTime)

print "At center"
time.sleep(1)
print "current: %.0f mA" % currentsensor.current_sense(10)
time.sleep(1)

center_servos()
time.sleep(10.0)
#servos_off()
current_now = currentsensor.current_sense(4)
print "current: %.0f" % (current_now)
print "servotest.py Done - Bye Bye"

