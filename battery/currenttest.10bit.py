#!/usr/bin/python

import PDALib
import myPyLib
import time
import sys
import signal
import math
import currentsensor

# ######### SET CNTL-C HANDLER #####
myPyLib.set_cntl_c_handler()


# while True:
print "Sleeping"
time.sleep(10)
print ("\ncurrent 1: %.0f \n" % currentsensor.current_sense(1))
print "\nSleeping"
time.sleep(10)
print("average of 4 readings: %.2f" % currentsensor.current_sense(4))
time.sleep(10)
print("average of 10 readings: %.2f" % currentsensor.current_sense(10))
print "\n"
time.sleep(10)
print("average of 20 readings: %.2f" % currentsensor.current_sense(20))
print "\n"
time.sleep(10)
print("average of 33 readings: %.2f" % currentsensor.current_sense(33))
print "\n"
time.sleep(10)
print ("\ncurrent 1: %.0f \n" % currentsensor.current_sense(1))

print "Done"

myPDALib.PiExit()
  
  

