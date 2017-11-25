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



import PDALib
import myPDALib
import myPyLib
import time

debugLevel = 0   # 0 off, 1 some,  99 all

ServoDwellTime = 0.01  #seconds to stay at each position

TILTSERVO = 0
PANSERVO = 1

ServoStep = 10  # must be integer for range func

PanPosLimitL = 2400
PanPosCenter = 1450
PanPosLimitR =  600

PanDegLimitL = 180
PanDegCenter =  90
PanDegLimitR =   0

# pre calculate one deg angle equals how many "pos" increments
PanDeg2PanPosInc = int((PanPosLimitL-PanPosLimitR) / float(PanDegLimitL-PanDegLimitR))
Pan0Deg2PanPos = PanDeg2PanPosInc * -180 + PanPosLimitL


TiltPosLimitUp = 500
TiltPosCenter = 1400
TiltPosLimitDn = 1900 #2435

TiltDegLimitUp = 90
TiltDegCenter  = 0
TiltDegLimitDn = -30

# pre calculate one deg angle equals how many "pos" increments
TiltDeg2TiltPosInc = int((TiltPosLimitUp-TiltPosCenter) / float(TiltDegLimitUp - TiltDegCenter))
Tilt0Deg2TiltPos = TiltPosCenter



def setup_servo_pins():
  PDALib.pinMode(TILTSERVO,PDALib.SERVO)    # init Tilt servo pin to SERVO mode
  PDALib.pinMode(PANSERVO,PDALib.SERVO )  # init motor2 speed control pin

def center_servos():
  servos_on()
  PDALib.servoWrite(TILTSERVO, TiltPosCenter)
  PDALib.servoWrite(PANSERVO, PanPosCenter)
  if (debugLevel): print "center_servos() called"
  

def servos_on():
    PDALib.pinMode(TILTSERVO, PDALib.SERVO)    # init Tilt servo pin to SERVO mode
    PDALib.pinMode(PANSERVO, PDALib.SERVO )    # init Pan  servo pin to SERVO mode
    if (debugLevel): print "servos_on() called"
  

def servos_off():
  PDALib.pinMode(TILTSERVO,PDALib.INPUT)    # init Tilt servo off
  PDALib.pinMode(PANSERVO,PDALib.INPUT)     # init motor2 servo off
  if (debugLevel): print "servos_off() called"

def init_servos():
    if (debugLevel): print "init_servos() called"
    servos_on()
    time.sleep(0.1)
    center_servos()
    # servos_off()

dummy = init_servos()                     # initialize when module is loaded

def pos_servo(servo,pos):
    if (debugLevel): print "rwplib.tiltpan.py:pos_servo(Tilt0Pan1=%d, pos=%d)" % (servo,pos) 
    if (servo == PANSERVO):
        cpos = myPyLib.clamp(pos,PanPosLimitR,PanPosLimitL)
    elif (servo == TILTSERVO):
        cpos = myPyLib.clamp(pos,TiltPosLimitUp,TiltPosLimitDn)
    if (debugLevel): print "setting Tilt0Pan1=%d to pos: %d)" % (servo, cpos) 
    PDALib.servoWrite(servo, cpos)   # set to new position
    return cpos

def gopigoDeg2panPos(angle):
    pos = angle*PanDeg2PanPosInc + Pan0Deg2PanPos
    if (debugLevel):
        print "rwplib.tiltpan.py:gopigoDeg2panPos(angle=%d) called" % angle
        print "rwplib.tiltpan.py:gopigoDeg2panPos: returning pos:",pos
    return pos

def rwpPos2gopigoPanDeg(pos):
    angle = (pos - Pan0Deg2PanPos)/PanDeg2PanPosInc
    if (debugLevel):
        print "rwplib.tiltpan.py:rwpPos2gopioPanDeg(pos=%d) called" % pos
        print "rwplib.tiltpan.py:rwpPos2gopioPanDeg: returning angle:",angle
    return angle
    
def tiltDeg2TiltPos(angle):
    pos = angle*TiltDeg2TiltPosInc + Tilt0Deg2TiltPos
    if (debugLevel):
        print "rwplib.tiltpan.py:tiltDeg2TiltPos(angle=%d) called" % angle
        print "rwplib.tiltpan.py:tiltDeg2TiltPos: returning pos:",pos
    return pos

def rwpTiltPos2TiltDeg(pos):
    angle = (pos-Tilt0Deg2TiltPos)/TiltDeg2TiltPosInc
    if (debugLevel):
        print "rwplib.tiltpan.py:rwpTiltPos2TiltDeg(pos=%d) called" % pos
        print "rwplib.tiltpan.py:rwpTiltPos2TiltDeg: returning angle:",angle
    return angle
    
def tilt_servo(angle):
    if (debugLevel): print "rwplib.tiltpan.py:  tilt_servo(angle=%d) called" % angle 
    pos = tiltDeg2TiltPos(angle)
    cpos = pos_servo(TILTSERVO, pos)
    cangle = rwpTiltPos2TiltDeg(cpos)                 
    if (debugLevel): print "rwplib.tiltpan.py:tilt_servo: pos=%d cpos=%d cangle=%f" % (pos,cpos,cangle)
    return cangle
    

def pan_servo(angle):
    if (debugLevel): print "rwplib.tiltpan.py:  pan_servo(angle=%d) called" % angle 
    pos = gopigoDeg2panPos(angle)
    cpos = pos_servo(PANSERVO, pos)
    cangle = rwpPos2gopigoPanDeg(cpos)                 
    if (debugLevel): print "rwplib.tiltpan.py:pan_servo: pos=%d cpos=%d cangle=%f" % (pos,cpos,cangle)
    return cangle


# ### TEST SERVOS
def main():
    global tiltAngle
    print "rwpilib:tiltpan.py:main: *** TILT PAN TEST MAIN ***"
    
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
                servos_on()
                pan_servo((8-int(key_press))*30)
                time.sleep(1)
                servos_off()
        elif key_press == '^':
                servos_on()
                tiltAngle += 10
                cmdDeg = tiltAngle
                print "cmd Tilt Angle: %d", cmdDeg
                actualDeg = tilt_servo(cmdDeg)
                print "Tilt servo set to %f deg" % actualDeg
                time.sleep(1)
                servos_off()
        elif key_press == 'V':
                servos_on()
                tiltAngle -= 10
                cmdDeg = tiltAngle
                print "cmd Tilt Angle: %d", cmdDeg
                actualDeg = tilt_servo(cmdDeg)
                print "Tilt servo set to %f deg" % actualDeg
                time.sleep(1)
                servos_off()
        elif key_press == 'c':
                center_servos()   # calls servos_on() 
            

    # command = tk.Tk()
    # command.bind_all('<Key>', key_input)  # ALAN  '' changed to '<Key>'
    # command.mainloop()

    ### created for command line execution cntl-C to quit

    while True:
      event=raw_input("cmd? ") 
      key_input(event)




def mainx():
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


