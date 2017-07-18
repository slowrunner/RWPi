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
# Data points from batery_life.py using 6.53v as 0 life remaining 
#   for 10 min safety factor. 
#  (V , Tremaining)

lifePoints= (
 (10.0, 10.77),   # added - exception'd at 9.1v during recharge
 (9.00, 10.76),       
 (8.34, 6.3),   # 10h55m (w/o 10m safety) life test began off charge
 (8.18, 6.13),
 (8.08, 5.97),
 (7.99, 5.8),
 (7.91, 5.63),
 (7.68, 5.47),
 (7.64, 5.3),
 (7.47, 4.8),   # got 8.5 hrs 7/18/16  4.8h 7/17/17
 (7.42, 4.63),    
 (7.38, 4.47),
 (7.35, 4.3),
 (7.32, 4.13),
 (7.3,  3.97),
 (7.26, 3.8),
 (7.24, 3.63),
 (7.2,  3.47),
 (7.19, 3.30),
 (7.18, 3.13),
 (7.17, 2.97),
 (7.16, 2.80),
 (7.14, 2.63),
 (7.13, 2.47),
 (7.12, 2.30),
 (7.11, 2.13),
 (7.1,  1.97),
 (7.09, 1.80),
 (7.08, 1.63),
 (7.07, 1.47),
 (7.06, 1.30),
 (7.05, 1.13), 
 (7.04, 0.97), 
 (7.04, 0.80),
 (7.03, 0.63),
 (7.02, 0.47),
 (6.8,  0.30),
 (6.76, 0.05),
 (6.53, 0.00),
 (5.13, -0.16),
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

BatteryCutOff = 6.5

def batteryTooLow():
  if (volts() < BatteryCutOff): return True
  else:                         return False


# ##### MAIN ######
def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  while True:
      print "\n"
      # printLifeTable()
      printStatus()
      print "batteryTooLow(): ",batteryTooLow()
      time.sleep(1)
  #end while
  myPDALib.PiExit()

if __name__ == "__main__":
    main()


