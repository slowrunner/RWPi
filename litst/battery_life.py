#!/usr/bin/python
#
# battery_life.py  BATTERY LIFE TEST
#
# The 7v2 unregulated through 2:1 divider must be connected to
#      ADC6 (pin 6) for this test
#
# This test will loop reading the voltage on ADC6 and current (pin 7)
#      UNTIL voltage drops below 6.53v (10 mins left) 4 times,
#      then will issue a shutdown now
#
# Start this test with $ sudo python battery_life.py
#
import sys
sys.path
sys.path.append('/home/pi/RWPi')

import rwpilib.PDALib as PDALib
import rwpilib.myPDALib as myPDALib
import time
import signal
import rwpilib.currentsensor as currentsensor
import rwpilib.battery as battery
import os
import datetime
import sys

def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def getUptime():
  res = os.popen('uptime').readline()
  return res.replace("\n","")

nLow = 0
while True:

  print ("current_sense(): %.0f mA" % currentsensor.current_sense(1000))
  # V_now = myPDALib.readVoltage(6) * 2.0  # 2:1 resistor divider
  V_now = battery.volts()
  if (V_now < 6.53):   #if 7v2 =6.53 10min 6.42 5min to knee!
          nLow+=1
          print "nLow:***************",nLow
  else: nLow = 0
  print ( "voltage: %.2f" % V_now)
  print ( "Life Estimate: %.1f" % battery.hoursOfLifeRemaining(V_now) )
  print datetime.datetime.now().date(), getUptime()
  print "\n"
  if (nLow >3):  # four times lower we're out of here
          os.system("sudo shutdown -h now")
          sys.exit(0)
  time.sleep(5)
# end while

myPDALib.PiExit()

