#!/usr/bin/python
#
# rwp_motors.py   RWP_MOTORS PRIMITIVES
#
#	init_motors()		enable motors
#	stop()			stop both motors
#	motor(int motor, int pcnt_vel) 0=lft,1=rt +/-100%
#	drive(int transv,int rotv) openloop +/-100% +=fwd,ccw

import PDALib
import myPyLib
import time

# #### _vars AND CONSTANTS

LEFT = 0     # LEFT MOTOR
RIGHT = 1    # RIGHT MOTOR

# Motor Pins 
# SRV 6		Motor 1 Speed (PWM)
# SRV 7		Motor 2 Speed (PWM)

RMotor = 6
LMotor = 7

MotorPin = [7,6]  # MotorPin[0] Left, MotorPin[1] Right

# DIO 12 (A4)	Motor 1 Dir A (0=coast 1=F/Brake)
# DIO 13 (A5)	Motor 1 Dir B (0=coast 1=R/Brake)

# DIO 14 (A6)	Motor 2 Dir A (0=coast 1=F/Brake)
# DIO 15 (A7)	Motor 2 Dir B (0=coast 1=R/Brake)

M1DirA = 12
M1DirB = 13
M2DirA = 14
M2DirB = 15
MotorDirA = [14,12]  # 0 left 1 right
MotorDirB = [15,13]  # 0 left 1 right

MinPwr2Move = 100
MaxPwr = 255


# ### INIT_MOTORS()

def init_motors():   # set up the pwm and two dir pins for each motor

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

# ### MOTOR(INDEX,VEL)

def motor(index,vel):  #mtr 0=lft, 1=rt, +/-100%
    avel = vel
    if (vel == 0):
        PDALib.analogWrite(MotorPin[index],0)  #set motor to zero speed
        return
    if (vel > 0):  # set forward
        PDALib.digitalWrite(MotorDirA[index],1)  #set to fwd
        PDALib.digitalWrite(MotorDirB[index],0)  #set to off/coast
    else:
        avel = -vel        
        PDALib.digitalWrite(MotorDirA[index],0)  #set to off/coast
        PDALib.digitalWrite(MotorDirB[index],1)  #set to bwd
    pwr = int( (MaxPwr - MinPwr2Move) * vel)  # compute pct to pwr
    PDALib.analogWrite(MotorPin[index], pwr)  #set motor pwr level

# ### DRIVE(TRANS_VEL, ROT_VEL)

def drive(trans_vel, rot_vel):  + = fwd, ccw
    motor(LEFT,  trans_vel - rot_vel)
    motor(RIGHT, trans_vel + rot_vel)

# get ready to go forward
PDALib.digitalWrite(M1DirA,1)  #set to forward
PDALib.digitalWrite(M2DirA,1)  #set to forward

# setting speed will start us going  (zero to fast in one command for this test)
PDALib.analogWrite(RMotor,127)  #set motor1 to half speed 
PDALib.analogWrite(LMotor,127)  #set motor2 to half speed


# ### STOP()

def stop():
    # turn off the speed pin 
    PDALib.analogWrite(RMotor,0)  #set motor1 to zero speed 
    PDALib.analogWrite(LMotor,0)  #set motor2 to zero speed


# ### TEST MAIN() ######################

def main():

  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  try:
    print "\nRWP_MOTORS TEST"
    init_motors()
  
    motor(LEFT,100)
    time.sleep(2)
    stop()

    motor(RIGHT,100)
    time.sleep(2)
    stop()

    drive(50,0)
    time.sleep(2)
    drive(-50,0)
    time.sleep(2)
    stop()

    drive(0,50)
    time.sleep(2)
    drive(0,-50)
    time.sleep(2)
    stop()

    drive(50,50)
    time.sleep(1)
    drive(50,-50)
    time.sleep(1)
    stop()
    drive(-50,50)
    time.sleep(1)
    drive(-50,-50)
    time.sleep(1)
    stop()

  except SystemExit:
    myPDALib.PiExit()
    print "RWP_MOTORS TEST: Bye Bye"    
  except:
    print "Exception Raised"
    stop()
    traceback.print_exc()  



if __name__ == "__main__":
    main()


