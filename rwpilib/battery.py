#!/usr/bin/python
#
# battery.py   BATTERY OBJECT
#

import PDALib
import myPDALib
import myPyLib
import datetime
import sys
import time
import os

# ########## GET BATTERY VOLTAGE
# volts(readings=75)
#
BATTERYPIN = 6  # ADC6 (0..7) is 2:1 divider to 7.2v battery
#
def volts(readings=75):
    if (readings > 1):
      values = []
      for i in range(0,readings):
        values.append(2.0 * myPDALib.readVoltage(BATTERYPIN))
      values.sort()
      voltage_now = sum(values) / float(len(values)) # average
    else:
      # voltage from a single analog reading
      voltage_now = 2.0 * myPDALib.readVoltage(BATTERYPIN)
    return voltage_now

def reading(readings=75):
    if (readings > 1):
      values = []
      for i in range(0,readings):
        values.append(myPDALib.analogRead12bit(BATTERYPIN))
        time.sleep(0.01)
      values.sort()
      reading = sum(values) / float(len(values)) # average
    else:
      # a single analog reading
      reading =  PDALib.analogRead12bit(BATTERYPIN)
    return reading  

#VperBit = (4.87/1024)  #4.89 gives same value as multi-meter at 4.68v

VperBit = (4.94/4095)   #4.94 gives same value as multi-meter at 4.94v

def readingToVolts(reading):
    return 2.0 * VperBit * reading


# ########## HOURS OF LIFE REMAINING
# hoursOfLifeRemaining(Vbatt)
#
# Data points from batery_life.py using 4 times under 6.53v as 0 life remaining 
# Battery Too Low point (10 min left) is 6.53 7/2017
#
# Historical:  
#   July 2016 8.5h and 10h 55m  (6 new Tenergy cells)
#   July 2017 6.5, 12.5h, 12.17h, 12.65h, 11h55m,
#             (2x 3yr old EBL cells, 4x 1yr old Tenergy cells)
#   Nov 2017  8.25 running status.sh - (first hit of battery too low shutdown)            
#   Feb 2018  8.5-9.5 hrs to four low batt 6.53v readings

#  (V , Time remaining)

lifePoints= (
 (10.0,  11.00),   # guess - exception'd at 9.1v during recharge
 (9.00,  10.25),   #     
 (8.50,  10.00),   # 
 (7.60,  8.25),    # 
 (6.93,  1.00),
 (6.78,  0.17),  # about 10 min till safe shutdown
 (6.53,  0.00),  # safe shutdown with about 10 min juice)
 (0.00, -1.00)
 )

hoursOfLifeRemainingArray = myPyLib.InterpolatedArray(lifePoints)

def hoursOfLifeRemaining(Vbatt=reading()):
   return hoursOfLifeRemainingArray[Vbatt]

def printStatus():
  print datetime.datetime.now().strftime("%c") # %I:%M:%S%p")
  print "battery.volts(1): %0.2f" % volts(1)
  vBatt = volts()
  print "battery.volts(): %0.2f" % vBatt
  print "battery.hoursOfLifeRemaining(): %0.1f" % hoursOfLifeRemaining(vBatt)

def printLifeTable():
  testVs = [ float(x)/10 for x in range(90,50, -2) ]

  print "V   Hours Remaining"
  for v in testVs:
    print "%0.1f  %0.1f" % (v, hoursOfLifeRemaining(v))

BatteryCutOff = 6.53  # 10 minutes 7/2017

def batteryTooLow(limit=BatteryCutOff):
  if (volts() < limit): return True
  else:                 return False


# ##### MAIN ######
def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  while True:
      print "\n"
      # printLifeTable()
      printStatus()
      shutdownnow = batteryTooLow()
      print "batteryTooLow(): ",shutdownnow
      if (shutdownnow == True):
          print "Battery.py issuing shutdown -h now"
          os.system("sudo shutdown -h now")
          sys.exit(0)
      time.sleep(1)
  #end while
  myPDALib.PiExit()

if __name__ == "__main__":
    main()


