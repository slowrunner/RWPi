#!/usr/bin/python
#
# status.py   PRINT RWPi STATUS
#

import PDALib
import myPDALib
import myPyLib
import battery
import currentsensor
from usDistanceClass import UltrasonicDistance
import irDistance
from bumpersClass import Bumpers
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




def printStatus():
  global b, u

  print "\n********* RWPi STATUS *****"
  print datetime.now()
  vBatt = battery.volts()
  print "battery.volts(): %0.1f" % vBatt
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
  try:
    while True:
        printStatus()
        time.sleep(3)
    #end while
  except SystemExit:
    myPDALib.PiExit()
    print "status.py: exiting"

if __name__ == "__main__":
    main()


