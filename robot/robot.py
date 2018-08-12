#!/usr/bin/python
#
# robot.py   test rwpi class robot 
#

import sys
sys.path.append("/home/pi/RWPi/rwpilib")

import rwpi as rwpi
import traceback
import time

def main():
  try:
    print "Starting robot.py Main"

    robot=rwpi.RWPi()
    robot.set_cntl_c_handler()  # Set CNTL-C to cancel all robot processes
    robot.be_scanner()
  except SystemExit:
    print "robot.py main: time for threads to quit"
    time.sleep(1)
    print "robot.py says: Bye Bye"
  except:
    print "Exception Raised"
    traceback.print_exc()


if __name__ == "__main__":
    main()
