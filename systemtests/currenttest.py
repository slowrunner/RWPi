#!/usr/bin/python
#
# currenttest.py
#
# Aug 2018: update for 12bit readings
#

import sys
sys.path.insert(0, '/home/pi/RWPi/rwpilib')
import myPDALib
import myPyLib
import currentsensor
import time
import math

ACS712PIN = 7  # Current sensor is on pin 7 (0..7) of the MCP3208

# while True:
for pin in range(0,7+1):
    if pin == 7:
      print "current_sense(): %.0f" %  currentsensor.current_sense(1,1)
    else:
      print "analogRead12bit("+str(pin)+"):",myPDALib.analogRead12bit(pin)

readings = []
values = []
for i in range(0,1000):
  values.append(currentsensor.current_sense(1,1))
  readings.append(myPDALib.analogRead12bit(ACS712PIN))
values.sort()
readings.sort()
middlev = values[400:600]
middler = readings[400:600]
medianr = sum(middler) / float(len(middler))
medianv = sum(middlev) / float(len(middlev))
print("median of 1000 readings: %.0f %.0f mA" % (medianr,medianv) )
averager = float(sum(readings)) / len(readings)
averagev = float(sum(values)) / len(values)
print("average of 1000 readings: %.0f %.0f mA" % (averager,averagev) )
print "min value: %.0f" %  min(values)
print "max value: %.0f" %  max(values)
dev = []
for x in values:
  dev.append(x - averagev)
squares = []
for i in dev:
  squares.append(i * i)
std_dev = math.sqrt(sum(squares)/(len(squares)-1))
print("std dev: %.0f" % std_dev)
myPDALib.PiExit()



