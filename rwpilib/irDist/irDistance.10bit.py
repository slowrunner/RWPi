#!/usr/bin/python
#
# irDistance.10bit.py   IR DISTANCE SENSOR OBJECT - 10 Bit version
#  This file is for Pi Droid Alpha with original MCP3008 which was 10 bit 
#         (I replaced with 3208 12-bit device)
# At 12" -   7 readings = 3% uncertainty (0.4), 75 readings = 1% (0.1 inch)
# At 48" - 150 readings = 3% uncertainty (1.4), 75 readings = 6% (3.0 inches)

import PDALib
import myPDALib
import myPyLib

import time



# # ########## IR DISTANCE SENSOR
# irDist(readings=75)
#
IRDISTPIN = 0  # ADC0 connected to IR Distance 10-150cm/4-60" spec
# Data points  
#  (reading , dist in inches to center of pan servo axis)

irDistPoints= (
 (000, 48.0),
 (185, 48,0),
 (186, 45.0),
 (187, 42.0),
 (188, 39.0),
 (190, 36.0),
 (193, 33.0),
 (199, 30.0), 
 (206, 27.0), 
 (217, 24.0), 
 (231, 21.0), 
 (251, 18.0), 
 (282, 15.0), 
 (328, 12.0), 
 (351, 11.0), 
 (374, 10.0), 
 (412, 9.0), 
 (462, 8.0), 
 (600, 6.0), 
 (826, 4.0), 
 (1024, 4.0),
 )

readingDistInchesArray = myPyLib.InterpolatedArray(irDistPoints)

def reading(readings=150):
    if (readings > 1):
      values = []
      for i in range(0,readings):
        values.append(PDALib.analogRead(IRDISTPIN))
        # time.sleep(0.01)
      values.sort()
      irReading = sum(values) / float(len(values)) # average
    else:
      # ir Distance from a single analog reading
      irReading =  PDALib.analogRead(IRDISTPIN)
    return irReading 

def inInches(readings=150):
    return readingDistInchesArray[reading(readings)]

def readingToInches(reading):
    return readingDistInchesArray[reading]

# test:
# import irDistance
# testReadings = [ float(x)/10 for x in range(60,0, -1) ]
# for reading in testReadings:
#   print v, irDistance.inInches(reading)

