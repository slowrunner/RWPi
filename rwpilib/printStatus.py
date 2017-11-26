#!/usr/bin/python
#
# status.py   PRINT RWPi STATUS
#

import PDALib
import myPDALib
import myPyLib
import battery
import currentsensor
import usDistanceClass
import irDistance
import bumpersClass
import time
from datetime import datetime
import os

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



def PrintStatus(self):

  print "\n********* RWPi STATUS *****"
  print datetime.now().date(), getUptime()
  vBatt = battery.volts()
  print "battery.volts(): %0.1f" % vBatt
  lifeRem=battery.hoursOfLifeRemaining(vBatt)
  lifeH=int(lifeRem)
  lifeM=(lifeRem-lifeH)*60
  print "battery.hoursOfLifeRemaining(): %d h %.0f m" % (lifeH, lifeM) 
  print "currentsensor.current_sense(): %.0f mA" % currentsensor.current_sense()
  print "Processor Temp: %s" % getCPUtemperature()
  print "Clock Frequency: %s" % getClockFreq()
  print "%s" % getThrottled()
  print  "irDistance.inInches: %0.1f" %  irDistance.inInches()
  print  "usDistance.inInches: %0.1f" %  self.usDistance.inInches()
  print  "bumpers:",self.bumpers.toStr()
  print  "\n"


# ##### MAIN ######
def main():

  print "don't know how to write a test"
  print "import printStatus.py to the Robot() class"
  print "in init self.printStatus=PrintStatus()"
  print "usage:  self.printStatus()"
  print "assumes Robot() has usDistance, and bumpers objects"


if __name__ == "__main__":
    main()


