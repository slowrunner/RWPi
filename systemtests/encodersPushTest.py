#!/usr/bin/python
#
# encoders.py   DIRECT READ ENCODERS TEST
#
# 10Jun2016 - changed pins for PDALib v0.93import PDALib
import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import myPDALib
import PDALib
import time
import signal


# ################# Encoder TEST ###########

# Left Encoder - DIO B4 - "PDALib.pin 20"
# Right Encoder- DIO B3 - "PDALib.pin 19" 

LeftEncoder = 20
RightEncoder = 19

# ##################
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  myPDALib.PiExit()
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)
# ##################

# Set up DIO channels as input for now
PDALib.pinMode(LeftEncoder,PDALib.INPUT)
PDALib.pinMode(RightEncoder,PDALib.INPUT)

# Loop displaying encoder values
while True:
    print "Left  Encoder:", PDALib.digitalRead(LeftEncoder)
    print "Right Encoder:", PDALib.digitalRead(RightEncoder)
    print "\n"
    time.sleep(1)
#end while

