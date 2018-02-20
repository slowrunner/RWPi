#!/usr/bin/python
#
# bumbersClass.py   BUMPERS SENSOR CLASS
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
#  ### INTERNAL METHODS AND VARS

#  __init__(readingsPerSec=10)          # initialize instance of class
#  pollBumpers(tSleep=0.01)             # thread that reads bumpers
#
#  pollThreadHandle
#  tSleep
#  leftstate, rightstate, rearstate, state
#  bumperStrings
#  pollThreadHandle.do_run
#

import PDALib
import myPDALib
import myPyLib
import time
import sys
import threading


class Bumpers():

  # CLASS VARS (Avail to all instances)
  # Access as Bumpers.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the Bumpers class   
  tSleep=0.1              # time for read_sensor thread to sleep after each read op
 
  # Bumpers are on the Pi Droid Alpha MCP23S17 DIO expander 
  # Wired to use internal pull-up power of the MCP23S17
  # Bumper value is negative logic - 0 means bumper activated, normal 1

  LeftBumperPin=18   #PDALib pin number
  RightBumperPin=17  #PDALib pin number  
  RearBumperPin=16   #PDALib pin number

  LeftBumperDioBit  = LeftBumperPin - 8     #PDALib.setDio bit number
  RightBumperDioBit = RightBumperPin - 8    #PDALib.setDio bit number  
  RearBumperDioBit  = RearBumperPin - 8     #PDALib.setDio bit number
  

  # Allowable Bumpers.state values
  NONE     = 0
  # Single bumpers
  LEFT     = 1   
  RIGHT    = 2
  REAR     = 4
  # Combinations
  FRONT    = 3
  LEFTREAR = 5
  RIGHTREAR= 6
  ALL      = 7
  # Not possible
  UNKNOWN  = 8
  
  # THE STATE OF EACH BUMPER and the combined BUMPERS state 
  # (class vars because there are only one physical bumper)
  # note: can get rid of left(), right(), rear() methods by using these vars direct
  leftState= UNKNOWN
  rightState=UNKNOWN
  rearState= UNKNOWN
  state=     UNKNOWN  #0,1=L,2=R,3=L+R(front),4=Rear,...

  # use to print Bumper.state var 
  bumperStrings=["NONE", "LEFT", "RIGHT", "FRONT", "REAR",
               "LEFTREAR", "RIGHTREAR", "ALL", "UNKNOWN"]
		
  # end of class vars definition

  def __init__(self):
    # SINGLETON TEST 
    if (Bumpers.pollThreadHandle!=None): 
        print "Second Bumpers Class Object, not starting pollingThread"
        return None
 
    # Set Bumper DIO channels as input for now
    PDALib.pinMode(Bumpers.LeftBumperPin, PDALib.INPUT)
    PDALib.pinMode(Bumpers.RightBumperPin,PDALib.INPUT)
    PDALib.pinMode(Bumpers.RearBumperPin, PDALib.INPUT)

    # Set internal pull-ups on bumper channels
    PDALib.setDioBit( PDALib.DIO_GPPU, Bumpers.LeftBumperDioBit ) # set LeftBumper  pin 18 pull-up
    PDALib.setDioBit( PDALib.DIO_GPPU, Bumpers.RightBumperDioBit )# set RightBumper pin 17 pull-up
    PDALib.setDioBit( PDALib.DIO_GPPU, Bumpers.RearBumperDioBit ) # set RearBumper  pin 16 pull-up

    # threading target must be an instance
    Bumpers.pollThreadHandle = threading.Thread( target=self.pollBumpers, 
                                               args=(Bumpers.tSleep,))
    Bumpers.pollThreadHandle.start()
  #end init()

  # BUMPER THREAD WORKER METHOD TO READ BUMPERS
  def pollBumpers(self,tSleep=0.01):     
    print "pollBumpers started with %.3f interval" % tSleep
    t = threading.currentThread()   # get handle to self (pollingBumpers thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.read()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollBumpers thread")

    
  def read(self):  #READ THE BUMPERS - can be used as poll or directly
      Bumpers.leftState= Bumpers.LEFT - Bumpers.LEFT * \
			   		  PDALib.digitalRead(Bumpers.LeftBumperPin)
      Bumpers.rightState= Bumpers.RIGHT - Bumpers.RIGHT * \
			   		    PDALib.digitalRead(Bumpers.RightBumperPin)
      Bumpers.rearState=  Bumpers.REAR - Bumpers.REAR * \
					   PDALib.digitalRead(Bumpers.RearBumperPin)
      Bumpers.state = Bumpers.leftState + Bumpers.rightState + Bumpers.rearState
      return Bumpers.state

  def status(self):
    return Bumpers.state

  def left(self):
    return Bumpers.leftState

  def right(self):
    return Bumpers.rightState

  def rear(self):
    return Bumpers.rearState
   
  def toStr(self,bumperState=UNKNOWN):  
    if (bumperState==Bumpers.UNKNOWN):
       bumperState= Bumpers.state
    return Bumpers.bumperStrings[bumperState]

  def cancel(self):
     print "bumpers.cancel() called"
     self.pollThreadHandle.do_run = False
 


# ##### BUMPER CLASS TEST METHOD ######
# creates two instances, only the first should start the read() thread
# the first time through the main() while loop, the sensors may not have been read yet
#     so bumpers.status() and each bumper may have a value of 8/UNKNOWN 
def main():
  # note: lowercase bumpers is object, uppercase Bumpers is class (everywhere in code)
  bumpers=Bumpers()  #create an instance which starts the read bumpers thread
  bumpersNoThreadStart=Bumpers()  # Test a second instance of class
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


