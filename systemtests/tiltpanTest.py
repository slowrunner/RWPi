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

# ### Servo control:

# setup_servo_pins(): Enables the servo
# center_servos():  enables and sets center pan forward, center tilt level
# servos_on():  Enables the tilt, pan servos
# servos_off(): Disables the tilt, pan servos (by setting to input)
# init_servos():  enables and centers the servos
# servo(angle): Set servo position  Left 180 - 0 Right


import sys
sys.path.append("/home/pi/RWPi/rwpilib")

import PDALib
import myPDALib
import myPyLib
import time
import tiltpan

debugLevel = 0   # 0 off, 1 some,  99 all


ServoStep = 10  # must be integer for range func


PanDegLimitL = 180
PanDegCenter =  90
PanDegLimitR =   0

TiltDegLimitUp = 90
TiltDegCenter  = 0
TiltDegLimitDn = -30


# ### TEST SERVOS
def main():
    global tiltAngle
    print "tiltpanTest.py:main: *** TILT PAN TEST MAIN ***"

    servo_range = [2,3,4,5,6,7,8]
    tiltAngle = 0

    def key_input(event):
        global tiltAngle
        key_press = event  # ALAN  for Tkinter was = event.keysym.lower()
        print(key_press)

        if key_press == '?':
            print """
            2-8: servo position
             ^: tilt sensor platform up 10 deg
            V: tilt sensor platform dn 10 deg            
            c: center servos

            ctrl-c: quit

            """
        if key_press.isdigit():
            if int(key_press) in servo_range:
                tiltpan.servos_on()
                tiltpan.pan_servo((8-int(key_press))*30)
                time.sleep(1)
                tiltpan.servos_off()
        elif key_press == '^':
                tiltpan.servos_on()
                tiltAngle += 10
                cmdDeg = tiltAngle
                print "cmd Tilt Angle: %d", cmdDeg
                actualDeg = tiltpan.tilt_servo(cmdDeg)
                print "Tilt servo set to %f deg" % actualDeg
                time.sleep(1)
                tiltpan.servos_off()
        elif key_press == 'V':
                tiltpan.servos_on()
                tiltAngle -= 10
                cmdDeg = tiltAngle
                print "cmd Tilt Angle: %d", cmdDeg
                actualDeg = tiltpan.tilt_servo(cmdDeg)
                print "Tilt servo set to %f deg" % actualDeg
                time.sleep(1)
                tiltpan.servos_off()
        elif key_press == 'c':
                tiltpan.center_servos()   # calls servos_on() 

    # command = tk.Tk()
    # command.bind_all('<Key>', key_input)  # ALAN  '' changed to '<Key>'
    # command.mainloop()

    ### created for command line execution cntl-C to quit

    while True:
      event=raw_input("cmd? ") 
      key_input(event)




def mainx():
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


