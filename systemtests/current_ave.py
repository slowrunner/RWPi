#!/usr/bin/python

import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import PDALib
import myPDALib
import time
import sys
import signal
import math
import currentsensor

def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ACS712PIN = 7  # Current sensor is on pin 7 (0..7) of the MCP3008


# while True:
print ("\ncurrent: %.0f \n" % currentsensor.current_sense(1))
print("average of 1000 readings: %.2f" % currentsensor.current_sense(1000))
print("average of 1000 readings: %.2f" % currentsensor.current_sense(1000))
print("average of 1000 readings: %.2f" % currentsensor.current_sense(1000))
print("average of 1000 readings: %.2f" % currentsensor.current_sense(1000))
print("average of 1000 readings: %.2f" % currentsensor.current_sense(1000))
print "\n"
print("average of 4 readings: %.2f" % currentsensor.current_sense(4))
print("average of 4 readings: %.2f" % currentsensor.current_sense(4))
print("average of 4 readings: %.2f" % currentsensor.current_sense(4))
print("average of 4 readings: %.2f" % currentsensor.current_sense(4))
print("average of 4 readings: %.2f" % currentsensor.current_sense(4))
print "\n"
print("average of 10 readings: %.2f" % currentsensor.current_sense(10))
print("average of 10 readings: %.2f" % currentsensor.current_sense(10))
print("average of 10 readings: %.2f" % currentsensor.current_sense(10))
print("average of 10 readings: %.2f" % currentsensor.current_sense(10))
print("average of 10 readings: %.2f" % currentsensor.current_sense(10))
print "\n"
print("average of 20 readings: %.2f" % currentsensor.current_sense(20))
print("average of 20 readings: %.2f" % currentsensor.current_sense(20))
print("average of 20 readings: %.2f" % currentsensor.current_sense(20))
print("average of 20 readings: %.2f" % currentsensor.current_sense(20))
print("average of 20 readings: %.2f" % currentsensor.current_sense(20))
print "\n"
print("average of 33 readings: %.2f" % currentsensor.current_sense(33))
print("average of 33 readings: %.2f" % currentsensor.current_sense(33))
print("average of 33 readings: %.2f" % currentsensor.current_sense(33))
print("average of 33 readings: %.2f" % currentsensor.current_sense(33))
print("average of 33 readings: %.2f" % currentsensor.current_sense(33))
print "\n"
print("average of 75 readings: %.2f" % currentsensor.current_sense(75))
print("average of 75 readings: %.2f" % currentsensor.current_sense(75))
print("average of 75 readings: %.2f" % currentsensor.current_sense(75))
print("average of 75 readings: %.2f" % currentsensor.current_sense(75))
print("average of 75 readings: %.2f" % currentsensor.current_sense(75))
print ("\ncurrent: %.0f \n" % currentsensor.current_sense(1))

print "Done"

myPDALib.PiExit()
  
  

