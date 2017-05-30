#!/usr/bin/python
#
# statusClass.py   PRINT RWPi STATUS
#

import PDALib
import myPDALib
import myPyLib
import battery
import currentsensor
from usDistanceClass import UltrasonicDistance
import irDistance
from bumpersClass import Bumpers
import time
from datetime import datetime


class Status():

  def __init__(self,robot_self):
      print "init Status Class"
      self.robotself=robot_self
      

  def testCancel(self):
     print "Status.testCancel() called"
     self.bumpers.cancel()
     self.usDistance.cancel()

  def printStatus(self):

    print "\n********* RWPi STATUS *****"
    print datetime.now()
    vBatt = battery.volts()
    print "battery.volts(): %0.1f" % vBatt
    lifeRem=battery.hoursOfLifeRemaining(vBatt)
    lifeH=int(lifeRem)
    lifeM=(lifeRem-lifeH)*60
    print "battery.hoursOfLifeRemaining(): %d h %.0f m" % (lifeH, lifeM) 
    print "currentsensor.current_sense(): %.0f mA" % currentsensor.current_sense()
    print  "irDistance.inInches: %0.1f" %  irDistance.inInches()
    print  "usDistance.inInches: %0.1f" %  self.robotself.usDistance.inInches(UltrasonicDistance.AVERAGE)
    print  "bumpers.status: %s" % (self.robotself.bumpers.toStr())

  def testStatus(self):
    self.bumpers=Bumpers()                # get instance bumpers
    self.usDistance=UltrasonicDistance()  # get instance ultrasonic sensor
    print "waiting for threads to start"
    time.sleep(2)
    while True:
      self.printStatus()
      time.sleep(3)
    #end while

    

# ##### MAIN ######
def main():
    statusObj=Status()

    # #### SET CNTL-C HANDLER 
    myPyLib.set_cntl_c_handler(statusObj.testCancel)
      
  
    try:
        statusObj.testStatus()
    except SystemExit:
        myPDALib.PiExit()
        print "statusClass Test Main shutting down"



if __name__ == "__main__":
    main()


