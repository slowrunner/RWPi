#!/usr/bin/python
#
# bumbers.py   BUMPERS SENSOR MODULE
#

import PDALib
import myPDALib
import myPyLib
import time
import sys
import signal


# Bumpers are on 
# DIO 18	Left Front
# DIO 17	Right Front
# DIO 16	Rear
# Wired to use internal pull-ups of the MCP23S17
# Bumper value is negative logic - 0 means bumper activated, normal 1

LeftBumperDIO=18
RightBumperDIO=17
RearBumperDIO=16

NONE     = 0
# Single bumpers
LEFT     = 1
RIGHT    = 2
REAR     = 4
# Combinations
FRONT    = 3
LEFTREAR = 5
RIGHTREAR= 6
ALL      = 7
UNKNOWN  = 8

bumperStrings=["NONE", "LEFT", "RIGHT", "FRONT", "REAR",
               "LEFTREAR", "RIGHTREAR", "ALL", "UNKNOWN"]
		

_leftState=0
_rightState=0
_rearState=0
_state=UNKNOWN

def init():
  # Set Bumper DIO channels as input for now
  PDALib.pinMode(LeftBumperDIO,PDALib.INPUT)
  PDALib.pinMode(RightBumperDIO,PDALib.INPUT)
  PDALib.pinMode(RearBumperDIO,PDALib.INPUT)

  # Set internal pull-ups on bumper channels
  PDALib.setDioBit( PDALib.DIO_GPPU, 8 )  # set LeftBumper  pin 16 pull-up
  PDALib.setDioBit( PDALib.DIO_GPPU, 9 )  # set RightBumper pin 17 pull-up
  PDALib.setDioBit( PDALib.DIO_GPPU, 10 ) # set RearBumper  pin 18 pull-up
#end init()

def read():
    global _leftState, _rightState, _rearState, _state
    _leftState= LEFT-LEFT*PDALib.digitalRead(LeftBumperDIO)
    _rightState= RIGHT-RIGHT*PDALib.digitalRead(RightBumperDIO)
    _rearState=  REAR-REAR*PDALib.digitalRead(RearBumperDIO)
    _state=_leftState + _rightState + _rearState
    return _state

def status():
    global _state
    return _state

def left():
    global _leftState
    return _leftState

def right():
    global _rightState
    return _rightState

def rear():
    global _rearState
    return _rearState
   
def toString(bumpers=UNKNOWN):
    global _state
    if (bumpers==UNKNOWN):
       bumpers=_state
    return bumperStrings[bumpers]

# ##### MAIN ######
def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  init()
  while True:
      read()
      print "\n"
      print "bumpers.state: %d %s" % (status(), toString())
      print "left():%d  rear():%d  right():%d" % (left(),rear(),right()) 
      time.sleep(1)
  #end while
  myPDALib.PiExit()

if __name__ == "__main__":
    main()


