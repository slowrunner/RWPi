#!/usr/bin/python
#
# irDist.py   IR DISTANCE SENSOR OBJECT
#
# At 12" -   7 readings = 3% uncertainty (0.4), 75 readings = 1% (0.1 inch)
# At 48" - 150 readings = 3% uncertainty (1.4), 75 readings = 6% (3.0 inches)

import myPDALib
import myPyLib
import time
import traceback


# # ########## IR DISTANCE SENSOR
# irDist(readings=75)
#
IRDISTPIN = 0  # ADC0 connected to IR Distance 10-150cm/4-60" spec
#
# Data points
#  (reading , dist in inches to front of sensor))
#  At 2.5 inches the readings start going back up - not valid
#  Readings re-evaluated Aug 2018 for 5.27v Vsupply/Vref

irDistPoints= (
 (000, 999.0),
 (553, 66.0),
 (575, 60.0),
 (618, 48.0),    # (725, 48.0),
 (661, 39.0),    # (731, 39.0),
 (674, 36.0),    # (738, 36.0),
 (703, 33.0),    # (765, 33.0),
 (729, 30.0),    # (778, 30.0),
 (767, 27.0),    # (806, 27.0),
 (806, 24.0),    # (849, 24.0),
 (858, 21.0),    # (904, 21.0),
 (922, 18.0),    # (973, 18.0),
 (1025,15.0),    # (1069, 15.0),
 (1170,12.0),    # (1235, 12.0),
 (1235,11.0),    # (1304, 11.0),
 (1330,10.0),    # (1394, 10.0),
 (1418, 9.0),    # (1486, 9.0),
 (1560, 8.0),    # (1635, 8.0),
 (1950, 6.0),    # (2071, 6.0),
 (2695, 4.0),    # (2816, 4.0),
 (3350, 2.5),    # (3535, 2.5),
 (4096, 0.0)
 )

readingDistInchesArray = myPyLib.InterpolatedArray(irDistPoints)

def reading(readings=150):
    if (readings > 1):
      values = []
      for i in range(0,readings):
        values.append(myPDALib.analogRead12bit(IRDISTPIN))
        # time.sleep(0.01)
      values.sort()
      irReading = sum(values) / float(len(values)) # average
    else:
      # ir Distance from a single analog reading
      irReading =  myPDALib.analogRead12bit(IRDISTPIN)
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


# ### TEST MAIN() ######################


def main():

  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  try:
    print "\nIR DISTANCE TEST"
    while True:
       r = reading()  # average of 150 readings
       print "ir sensor reading %4d distance: %4.1f inches" % (r,readingToInches(r))
       time.sleep(1)


  except SystemExit:
    myPDALib.PiExit()
    print "IR DISTANCE TEST: Bye Bye"

  except:
    print "Exception Raised"
    traceback.print_exc()



if __name__ == "__main__":
    main()

