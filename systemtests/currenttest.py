import PDALib
import time
import sys
import signal
import math


def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  PDALib.LibExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ACS712PIN = 7  # Current sensor is on pin 7 (0..7) of the MCP3008

def current_sense():   
    # Sensor puts out 0.185V/A around 2.5v
    #
    #   5000mV          1A        1000A
    #  --ADC---- *   -Sensor-  *  -----  = 26.39358 mA per reading bit
    #   1024           185mV        1A                 around 512
    zero_current = 514.00
    values = []
    for i in range(0,10):
      values.append(PDALib.analogRead(ACS712PIN))
    values.sort()
    middle = values[4:6]
    median = sum(middle) / float(len(middle)) # median 
    average = sum(values) / float(len(values)) # average
    print("average current %.0f" % ((zero_current - average)*26.39358))
    print("median current %.0f" % ((zero_current - median)*26.39358))
    pin_value = median  
    current_now = (zero_current - pin_value)*26.39358
    return [current_now, pin_value]


# while True:
for pin in range(0,7+1):
    if pin == 7:
      print "current_sense():", current_sense()
    else: 
      print "analog("+str(pin)+"):",PDALib.analogRead(pin)

values = []
for i in range(0,1000):
  values.append(PDALib.analogRead(ACS712PIN))
values.sort()
middle = values[400:600]
median = sum(middle) / float(len(middle))
print("median of 1000 zero load readings: %.2f" % median)
average = float(sum(values)) / len(values)
print("average of 1000 zero load readings: %.2f" % average)
print "min value:", min(values)
print "max value:", max(values)
dev = []
for x in values:
  dev.append(x - average)
squares = []
for i in dev:
  squares.append(i * i)
std_dev = math.sqrt(sum(squares)/(len(squares)-1))
print("std dev: %.2f" % std_dev)
PDALib.LibExit()
  
  

