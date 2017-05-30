#!/usr/bin/python
#
# HC-SR04 interface test using PDALib 
#
# Alan McDonley 10 June 2016

import PDALib
import time
import sys
import signal
import currentsensor

EchoPin = 26    #GPIO26 is pin 37 of the PiB+ and Pi3B 40pin connector
TrigPin = 2	 #PDALib "pin" = Servo3 connector (of 1-8) (GPIO18)

# ################## CONTROL-C HANDLER
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  PDALib.clearEcho(EchoPin)
  PDALib.LibExit()  
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)
# ##################


#  my_echo1 = pi.callback(22, pigpio.RISING_EDGE,  _echo1)
#  my_echo0 = pi.callback(22, pigpio.FALLING_EDGE, _echo0)

# Use modified PDALib.v93.py pinMode(pin,ECHO) for GPIO22 ("pin 4" even though connection is direct to GPIO22)
# Use setEcho(gpioNUM) for GPIO27 (pin 37 on PiB+ and Pi3B connector)

#   pinMode(EchoPin,ECHO)
PDALib.setEcho(EchoPin)
while 1:
      # print(readDistance2(18,22)/58)
      print( "Dist: %.2f cm" % PDALib.readDistance2(TrigPin,EchoPin))
      time.sleep(1.0)

#   my_echo1.cancel()
#   my_echo0.cancel()

