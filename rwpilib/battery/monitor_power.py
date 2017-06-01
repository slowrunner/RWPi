#
# monitor_power.py  MONITOR BATTERY AND CURRENT
# 
# The 7v2 unregulated through 2:1 divider must be connected to 
#      ADC6 (pin 6) for this test
#
# This test will loop reading the voltage on ADC6 and current (pin 7)
#

import PDALib
import myPDALib
import time
import sys
import signal
import currentsensor
import os
import datetime
import sys

def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

VperBit = (4.87/1024)  #4.89 gives same value as multi-meter at 4.68v

while True:
  print "\n"
  print datetime.datetime.now()

  for pin in range(6,7+1):
    if pin == 7:
      print ("current_sense(): %.0f mA" % currentsensor.current_sense())
      time.sleep(0.1)
    else:
      if pin == 6:
        V_now = myPDALib.readVoltage(6)*2.0
      print ( "battery voltage: %.2f" % V_now)
      time.sleep(0.1)
  time.sleep(1)

myPDALib.PiExit()
  
  

