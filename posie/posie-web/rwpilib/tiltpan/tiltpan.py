#!/usr/bin/python
#
# tiltpan.py   TILT PAN 
#
# SG90 Micro Servo

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

import PDALib
import myPDALib
import myPyLib
import time


ServoDwellTime = 0.01  #seconds to stay at each position

TILTSERVO = 0
PANSERVO = 1

ServoStep = 10  # must be integer for range func

PanLimitL = 2500
PanCenter = 1500
PanLimitR =  630

TiltLimitUp = 700  #550
TiltCenter = 1375
TiltLimitDn = 1900 #2435


def setup_servo_pins():
  PDALib.pinMode(TILTSERVO,PDALib.SERVO)    # init Tilt servo pin to SERVO mode
  PDALib.pinMode(PANSERVO,PDALib.SERVO )  # init motor2 speed control pin

def center_servos():
  PDALib.servoWrite(TILTSERVO, TiltCenter)
  PDALib.servoWrite(PANSERVO, PanCenter)

def servos_off():
  PDALib.pinMode(TILTSERVO,PDALib.INPUT)    # init Tilt servo off
  PDALib.pinMode(PANSERVO,PDALib.INPUT)     # init motor2 servo off




# ### TEST SERVOS
def main():
  setup_servo_pins()
  center_servos()
  print "Servos Centered"
  time.sleep(1.0)
  try:
    myPyLib.set_cntl_c_handler(servos_off)  # Set CNTL-C handler 



    for panpos in range(PanCenter,PanLimitL+1, ServoStep ):   # move from center to full left
      PDALib.servoWrite(PANSERVO,panpos)                    # set to new position
      print "panpos: %d" % panpos
      time.sleep(ServoDwellTime)

    print "At left limit"
    time.sleep(1)

    for panpos in range(PanLimitL,PanLimitR-1, -ServoStep ):   # move from full left to full right
      PDALib.servoWrite(PANSERVO,panpos)                 # set to new position
      print "panpos: %d" % panpos
      time.sleep(ServoDwellTime)

    print "At right limit"
    time.sleep(1)

    for panpos in range(PanLimitR, PanCenter, ServoStep ):   # move from full right to center
      PDALib.servoWrite(PANSERVO,panpos)                 # set to new position
      print "panpos: %d" % panpos
      time.sleep(ServoDwellTime)

    print "At center"
    time.sleep(1)


    for tiltpos in range(TiltCenter,TiltLimitUp-1, -ServoStep ):   # move from center to full up
      PDALib.servoWrite(TILTSERVO,tiltpos)                      # set to new position
      print "tiltpos: %d" % (tiltpos)
      time.sleep(ServoDwellTime)

    print "At full up"
    time.sleep(1)

    for tiltpos in range(TiltLimitUp,TiltLimitDn+1,ServoStep ):   # move from full up to full down
      PDALib.servoWrite(TILTSERVO, tiltpos)                 # set to new position
      print "tiltpos: %d" % (tiltpos)
      time.sleep(ServoDwellTime)

    print "At full down"
    time.sleep(1)

    for tiltpos in range(TiltLimitDn, TiltCenter, -ServoStep ):   # move from full down back to center
      PDALib.servoWrite(TILTSERVO, tiltpos)                     # set to new position
      print "tiltpos: %d" % (tiltpos)
      time.sleep(ServoDwellTime)

    print "At center"
    time.sleep(1)
    center_servos()
    servos_off()
    print "servos off"
    print "tiltPan Test Main end"

  except SystemExit:
    myPDALib.PiExit()
    print "tiltPan Test Main shutting down"




if __name__ == "__main__":
    main()


