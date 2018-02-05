#!/usr/bin/python
#
# robot.py   test rwpi class robot 
#

import rwpilib.rwpi as rwpi
import traceback
import time

def main():
  try:
    print "Starting rwpi.py Main"
    
    robot=rwpi.RWPi()
    robot.set_cntl_c_handler()  # Set CNTL-C to cancel all robot processes
    robot.be_scanner()
  except SystemExit:
    print "rwpi.py main: time for threads to quit"
    time.sleep(1)
    print "rwpi.py says: Bye Bye"    
  except:
    print "Exception Raised"
    traceback.print_exc()
    



if __name__ == "__main__":
    main()
