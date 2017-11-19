#!/usr/bin/python
#
# sayStatus.py   Speak RWPi STATUS
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
import speak
import psutil

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

def uptime():
    upseconds = time.time() - psutil.boot_time()
    return time.strftime("%H hours %M minutes", time.gmtime(upseconds))

def SayStatus(self):
  global b, u

  rptstr = "RWPi STATUS"
  speak.say(rptstr)
  #print datetime.now().date(), getUptime()
  rptstr = "Uptime %s" % uptime()
  speak.say(rptstr)
  vBatt = battery.volts()
  rptstr = "battery.volts(): %0.1f" % vBatt
  speak.say(rptstr)
  lifeRem=battery.hoursOfLifeRemaining(vBatt)
  lifeH=int(lifeRem)
  lifeM=(lifeRem-lifeH)*60
  rptstr = "Life Remaining Estimate: %d hours %.0f minutes" % (lifeH, lifeM)
  speak.say(rptstr)
  rptstr = "Processor Temp: %s" % getCPUtemperature()
  speak.say(rptstr)
  rptstr = "Clock Frequency: %s" % getClockFreq()
  speak.say(rptstr)
  rptstr = "%s" % getThrottled()
  speak.say(rptstr)
  rptstr = "drawing %.0f milliamps" % currentsensor.current_sense()
  speak.say(rptstr)
  #print  "irDistance.inInches: %0.1f" %  irDistance.inInches()
  #print  "usDistance.inInches: %0.1f" %  u.inInches()
  #print  "bumpers:",b.toStr()


# ##### MAIN ######
def main():

  print "don't know how to write a test"
  print "import rwpilib.sayStatus as sayStatus"
  print "in init self.sayStatus=sayStatus.SayStatus()"
  print "usage:  self.sayStatus(self)"


if __name__ == "__main__":
    main()


