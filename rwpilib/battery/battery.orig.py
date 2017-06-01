#!/usr/bin/python
#
# battery.py   BATTERY OBJECT
#

import PDALib
import myPDALib
import myPyLib
import datetime

import time

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
        values.append(PDALib.analogRead(BATTERYPIN))
        time.sleep(0.01)
      values.sort()
      reading = sum(values) / float(len(values)) # average
    else:
      # a single analog reading
      reading =  PDALib.analogRead(BATTERYPIN)
    return reading  

VperBit = (4.87/1024)  #4.89 gives same value as multi-meter at 4.68v

def readingToVolts(reading):
    return 2.0 * VperBit * reading


# ########## HOURS OF LIFE REMAINING
# hoursOfLifeRemaining(Vbatt)
#
# Data points from batery_life.py using 6.71v as 0 life remaining 
#   for 10 min safety factor. 
#  (V , Tremaining)

lifePoints= (
 (10.0, 10.77),   # added - exception'd at 9.1v during recharge
 (9.00, 10.76),       
 (8.30, 10.75),
 (7.90, 10.00),
 (7.80, 9.75),
 (7.76, 9.47),
 (7.69, 9.25),
 (7.68, 9.17),
 (7.64, 9.08),
 (7.55, 8.50),
 (7.46, 7.50),
 (7.43, 7.00),
 (7.40, 6.50),
 (7.37, 5.50),
 (7.33, 4.75),
 (7.31, 4.25),
 (7.24, 3.50),
 (7.23, 2.75),
 (7.17, 2.25),
 (7.14, 1.75),
 (7.12, 1.50),
 (7.07, 1.00),
 (7.04, 0.83),
 (7.03, 0.75),
 (6.99, 0.50),
 (6.91, 0.25),
 (6.81, 0.08),
 (6.71, 0.00),
 (0.0, 0.00),
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




# ##### MAIN ######
def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  while True:
      print "\n"
      # printLifeTable()
      printStatus()
      time.sleep(1)
  #end while
  myPDALib.PiExit()

if __name__ == "__main__":
    main()


