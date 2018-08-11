#!/usr/bin/python
#
# test_myPyLib.py   TEST FOR myPyLib.py
#

#import PDALib
#import myPDALib
import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import myPyLib
import time

# ######### Define a call back func
def ctrl_c_callback():
  print "ctrl_c_callback() called"

# ######### SET CNTL-C HANDLER #####
myPyLib.set_cntl_c_handler(ctrl_c_callback)

while True:
    print "Test myPyLib - type cntl-c"
    time.sleep(1)
#end while

