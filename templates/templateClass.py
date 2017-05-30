#!/usr/bin/python
#
# templateClass.py   TEMPLATE CLASS
#

import PDALib
import myPDALib
import myPyLib
import time
import sys
import threading


class X():

  # CLASS VARS (Avail to all instances)
  # Access as X.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the X class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (X.pollThreadHandle!=None): 
        print "Second X Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "X worker thread readingsPerSec:",readingsPerSec
    X.tSleep=1.0/readingsPerSec    #compute desired sleep
    X.pollThreadHandle = threading.Thread( target=self.pollX, 
                                               args=(X.tSleep,))
    X.pollThreadHandle.start()
    print "X worker thread told to start"
  #end init()

  # X THREAD WORKER METHOD TO READ X
  def pollX(self,tSleep=0.1):     
    print "pollX started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingX thread)
    while getattr(t, "do_run", True):  # check the dorun thread attribute
      self.read()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollX thread")

    
  def read(self):  #READ THE X - can be used as poll or directly
       return   # X.state


  def cancel(self):
     print "X.cancel() called"
     self.pollThreadHandle.dorun = False
     print "Waiting for X.workerThread to quit"
     self.pollThreadHandle.join()


# ##### X CLASS TEST METHOD ######
# the first time through the main() while loop, the sensors may not have been read yet
#     so X.status() and each X may have a value of 8/UNKNOWN 
def main():
  # note: lowercase X is object, uppercase X is class (everywhere in code)
  X=X()  #create an instance which starts the read X thread
  myPyLib.set_cntl_c_handler(X.cancel)  # Set CNTL-C handler 
  try:
    while True:
      print "\n"
      time.sleep(1)
    #end while
  except SystemExit:
    myPDALib.PiExit()
    print "x: Bye Bye"    
  except:
    print "Exception Raised"
    x.cancel()
    traceback.print_exc()  

if __name__ == "__main__":
    main()


