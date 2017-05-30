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
# Data points from batery_life.py using 6.53v as 0 life remaining 
#   for 10 min safety factor. 
#  (V , Tremaining)

lifePoints= (
 (10.0, 10.77),   # added - exception'd at 9.1v during recharge
 (9.00, 10.76),       
 (8.30, 10.75),   # 10h55m (w/o 10m safety) life test began off charge
 (7.90, 10.00),
 (7.80, 9.75),
 (7.76, 9.47),
 (7.69, 9.25),
 (7.68, 9.17),
 (7.64, 9.08),
 (7.45, 8.53),   # got 8.5 hrs 7/18/16
 (7.40, 8.42),    
 (7.35, 8.17),
 (7.31, 7.92),
 (7.27, 7.42),
 (7.22, 6.92),
 (7.19, 6.42),
 (7.15, 5.92),
 (7.12, 5.42),
 (7.04, 4.92),
 (7.00, 4.42),
 (6.97, 3.92),
 (6.94, 3.42),
 (6.91, 2.92),
 (6.88, 2.42),
 (6.87, 1.90),
 (6.86, 1.40),
 (6.77, 0.92),
 (6.73, 0.75),
 (6.72, 0.58), 
 (6.70, 0.42), 
 (6.67, 0.25),
 (6.60, 0.08),
 (6.53, 0.00),
 (6.42, -0.08),
 (6.00, -0.16),
 (0.0, -1.0)
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


