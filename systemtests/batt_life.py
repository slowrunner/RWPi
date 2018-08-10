#!/usr/bin/python
#
# batt_life.py   Run Battery down while printing status
#
# The 7v2 unregulated through 2:1 divider must be connected to 
#      ADC6 (pin 6) for this test
#
# This test will loop reading the voltage on ADC6 and current (pin 7)
#      UNTIL voltage drops below 5.9v 4 times,
#      then will issue a shutdown now
#
# Start this test with $ sudo python batt_life.py
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
import sys

import rwpilib.myPyLib as myPyLib
from rwpilib.usDistanceClass import UltrasonicDistance
import rwpilib.irDistance as irDistance
from rwpilib.bumpersClass import Bumpers
from datetime import datetime

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("\n",""))

# Return Clock Freq as a character string                                      
def getClockFreq():
    res = os.popen('vcgencmd measure_clock arm').readline()
    res = int(res.split("=")[1])
    if (res < 1000000000):
        res = str(res/1000000)+" MHz"
    else: res = '{:.2f}'.format(res/1000000000.0)+" GHz"
    return res

# Return throttled flags as a character string                                      
def getThrottled():
    res = os.popen('vcgencmd get_throttled').readline()
    return res.replace("\n","")

def getUptime():
    res = os.popen('uptime').readline()
    return res.replace("\n","")


def printStatus():
  global b, u

  print "\n********* RWPi STATUS *****"
  print datetime.now().date(), getUptime()
  vBatt = battery.volts()
  print "battery.volts(): %0.2f" % vBatt
  lifeRem=battery.hoursOfLifeRemaining(vBatt)
  lifeH=int(lifeRem)
  lifeM=(lifeRem-lifeH)*60
  print "battery.hoursOfLifeRemaining(): %d h %.0f m" % (lifeH, lifeM) 
  print "Processor Temp: %s" % getCPUtemperature()
  print "Clock Frequency: %s" % getClockFreq()
  print "%s" % getThrottled()
  print "currentsensor.current_sense(): %.0f mA" % currentsensor.current_sense()
  print  "irDistance.inInches: %0.1f" %  irDistance.inInches()
  print  "usDistance.inInches: %0.1f" %  u.inInches()
  print  "bumpers:",b.toStr()



# ##### MAIN ######

def handle_ctlc():
  global b, u
  b.cancel()
  u.cancel()

def main():
  global b, u

  # #### SET CNTL-C HANDLER 
  myPyLib.set_cntl_c_handler(handle_ctlc)

  # #### INIT SENSORS 
  b=Bumpers()
  u=UltrasonicDistance()
  batteryLowCount = 0
  print ("Starting status loop at %.2f volts" % battery.volts())  
  try:
    while True:
        printStatus()
        if (battery.batteryTooLow(5.9)): batteryLowCount += 1
        if (batteryLowCount > 3):
          # speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY - SHUTTING DOWN NOW" % battery.volts())
          os.system("sudo shutdown -h now")
          sys.exit(0)
        time.sleep(30)
    #end while
  except SystemExit:
    myPDALib.PiExit()
    print "status.py: exiting"

if __name__ == "__main__":
    main()


