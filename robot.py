#!/usr/bin/python
#
# robot.py   test rwpi class robot 
#

import rwpilib.rwpi as rwpi



def main():
  try:
    print "Starting rwpi.py Main"
    
    robot=rwpi.RWPi()
    myPyLib.set_cntl_c_handler(robot.cancel)  # Set CNTL-C handler 
    robot.be_scanner()
  except SystemExit:
    myPDALib.PiExit()
    print "rwpi.py main: time for threads to quit"
    time.sleep(1)
    print "rwpi.py says: Bye Bye"    
  except:
    print "Exception Raised"
    # r.cancel()
    traceback.print_exc()
    



if __name__ == "__main__":
    main()
