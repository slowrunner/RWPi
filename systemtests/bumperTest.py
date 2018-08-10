#!/usr/bin/python
#
# bumbersTest.py   BUMPERS CLASS TEST
#

# METHODS
#
#  Bumpers(readingsPerSec=10) # Create instance and start thread to watch bumpers
#  read()       # checks physical bumpers, and returns bumpers status
#  status()     # returns {Bumpers.NONE,LEFT,RIGHT,FRONT,REAR,LEFTREAR,RIGHTREAR}
#  left()       # returns 0 or Bumpers.LEFT
#  right()      # returns 0 or Bumpers.RIGHT
#  rear()       # returns 0 or Bumpers.REAR
#  toStr()      # returns string version of bumpers status or passed value
#  cancel()     # initiates closing the bumper polling thread
#
# CONSTANTS
#
#  NONE,LEFT,RIGHT,REAR,FRONT,LEFTREAR,RIGHTREAR,ALL,UNKNOWN
#

import sys
sys.path.append("/home/pi/RWPi/rwpilib")
from bumpersClass import Bumpers
import myPDALib
import myPyLib
import time


# ##### BUMPER CLASS TEST METHOD ######
# creates two instances, only the first should start the read() thread
# the first time through the main() while loop, the sensors may not have been read yet
#     so bumpers.status() and each bumper may have a value of 8/UNKNOWN 
def main():
  # note: lowercase bumpers is object, uppercase Bumpers is class (everywhere in code)
  bumpers=Bumpers()  #create an instance which starts the read bumpers thread
  # bumpersNoThreadStart=Bumpers()  # Test a second instance of class
  myPyLib.set_cntl_c_handler(bumpers.cancel)  # Set CNTL-C handler 
  try:
    while True:
      print "\n"
      print "bumpers.state: %d %s" % (bumpers.status(), bumpers.toStr())
      print "left():%d  rear():%d  right():%d" % (
	bumpers.left(),
	bumpers.rear(),
	bumpers.right() ) 
      print "direct bumpers.read():",bumpers.read()
      time.sleep(1)
    #end while
  except SystemExit:
    myPDALib.PiExit()
    print "bumpersClass Test Main shutting down"


if __name__ == "__main__":
    main()


