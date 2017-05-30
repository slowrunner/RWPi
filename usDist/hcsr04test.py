#!/usr/bin/python
#
# HC-SR04 interface test using PDALib, myPDALib and hcs04.py
#
# Alan McDonley 17 June 2016

import PDALib
import myPDALib
import hcsr04
import time
import sys
import signal
import currentsensor

TrigPin = 26    #GPIO26 is pin 37 of the PiB+ and Pi3B 40pin connector
EchoPin = 5	 #PDALib "pin" = Servo3 connector (of 1-8) (GPIO18)

# ################## CONTROL-C HANDLER
# Callback and setup to catch control-C and quit program
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  hcsr04.clearEcho()
  myPDALib.PiExit()  
  sys.exit(0)

# Setup the callback to catch control-C
signal.signal(signal.SIGINT, signal_handler)
# ##################


hcsr04.setEcho(EchoPin)
while 1:
      # print(readDistance2(18,22)/58)
      print( "Dist: %.2f cm %.0f mA" % (hcsr04.readDistance2gs(TrigPin,EchoPin),currentsensor.current_sense()))
      time.sleep(1.0)


#   my_echo1.cancel()
#   my_echo0.cancel()

