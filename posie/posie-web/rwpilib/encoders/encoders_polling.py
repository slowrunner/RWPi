#!/usr/bin/python
#
# encoders.py   ENCODERS TEST
#
# 10Jun2016 - changed pins for PDALib v0.93import PDALib

import PDALib
import myPDALib
import myPyLib
import time
import sys
import signal


# ################# Encoder TEST ###########

# Left Encoder - DIO B4 - "PDALib.pin 20"
# Right Encoder- DIO B3 - "PDALib.pin 19" 

LeftEncoder = 20
RightEncoder = 19

_leftEncoderState=0
_rightEncoderState=0
_leftEncoderCount=0
_rightEncoderCount=0
_ccwBias=0
_lastLeftEncoderState=0
_lastLeftEncoderState=0

# ##################
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  PDALib.LibExit()
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)

# ##################
def init():
  # Set up DIO channels as input for now
  PDALib.pinMode(LeftEncoder,PDALib.INPUT)
  PDALib.pinMode(RightEncoder,PDALib.INPUT)
  reset()

def reset():
    global _leftEncoderState,  _lastLeftEncoderState,  _leftEncoderCount
    global _rightEncoderState, _lastRightEncoderState, _rightEncoderCount
    global _ccwBias

    _leftEncoderState=PDALib.digitalRead(LeftEncoder)
    _rightEncoderState=PDALib.digitalRead(RightEncoder)

    _lastLeftEncoderState  = _leftEncoderState
    _lastRightEncoderState = _rightEncoderState

    _leftEncoderCount=0
    _rightEncoderCount=0

    _ccwBias=0

def readEncoders():
    global _leftEncoderState,  _lastLeftEncoderState,  _leftEncoderCount
    global _rightEncoderState, _lastRightEncoderState, _rightEncoderCount
    global _ccwBias

    _leftEncoderState=PDALib.digitalRead(LeftEncoder)
    _rightEncoderState=PDALib.digitalRead(RightEncoder)

    if (_leftEncoderState != _lastLeftEncoderState):
        _leftEncoderCount+=1
        _lastLeftEncoderState=_leftEncoderState

    if (_rightEncoderState != _lastRightEncoderState):
        _rightEncoderCount+=1
        _lastRightEncoderState=_rightEncoderState

    _ccwBias= _rightEncoderCount - _leftEncoderCount

def leftState():
  global _leftEncoderState
  return _leftEncoderState

def rightState():
  global _rightEncoderState
  return _rightEncoderState

def leftCount():
  global _leftEncoderCount
  return _leftEncoderCount

def rightCount():
  global _rightEncoderCount
  return _rightEncoderCount

def ccwBias():
  global _ccwBias
  return _ccwBias

  



# ##### MAIN ######
def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  init()
  # Loop displaying encoder values
  while True:
      readEncoders()
      print "\n"
      print "left.state: %d count: %d | RIGHT: %d count: %d | ccwBIAS: %d" % (
            leftState(), leftCount(), rightState(), rightCount(), ccwBias() )
      
  #end while
  myPDALib.PiExit()

if __name__ == "__main__":
    main()

