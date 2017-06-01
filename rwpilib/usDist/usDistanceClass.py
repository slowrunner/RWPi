#!/usr/bin/python
#
# usDistanceClass.py   ULTRASONIC DISTANCE SENSOR CLASS
#
# usDistance=UltrasonicDistance([readingsPerSec]) default is 10
#
# readingsPerSecond:  10 takes 0.3% CPU, 30 takes 9.5% PiB+

import PDALib
import pigpio
import myPDALib
import myPyLib
import time
import sys
import threading
import Queue


class UltrasonicDistance:

  # CLASS VARS (Avail to all instances)
  # Access as self.UltrasonicDistance.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the class   
  tSleep=1.0  # time for read_sensor thread to sleep (set in __init__)
  usDistanceInCm=0.0
  AveUsDistanceInCm=0.0
  _qReadings=Queue.Queue()
  MAX_qReadings_QSIZE=10
  AVERAGE=2    # usage: usDistance.inInches(UltrasonicDistance.AVERAGE)
  

  # My configuration
  TrigPin = 26    #GPIO26 is pin 37 of the PiB+ and Pi3B 40pin connector
  EchoPin = 5	 #PDALib "pin" = Servo6 connector (of 1-8) (GPIO23)

 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (UltrasonicDistance.pollThreadHandle!=None): 
        print "Second UltrasonicDistance Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE
    #
    # Setup callbacks for trigger pulse and for echo pulse
    
    self.setEcho()

    # START A THREAD
    # threading target must be an instance
    print "UltrasonicDistance: readingsPerSec:",readingsPerSec
    UltrasonicDistance.tSleep=1.0/readingsPerSec  # compute desired sleep   
    UltrasonicDistance.pollThreadHandle = threading.Thread( 
				target=self.pollUltrasonicDistance, 
                              args=(UltrasonicDistance.tSleep,) )
    UltrasonicDistance.pollThreadHandle.start()
    print "UltrasonicDistance: reading thread told to start"
  #end init()


  # UltrasonicDistance THREAD WORKER METHOD TO READ UltrasonicDistance
  def pollUltrasonicDistance(self,tSleep=0.01):     
    print "pollUltrasonicDistance started with %.3fs cycle" % tSleep
    t = threading.currentThread()   # get handle to self (pollingUltrasonicDistance thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      
      self._qReadings.put(self.read())
      if (self._qReadings.qsize() > UltrasonicDistance.MAX_qReadings_QSIZE):
        self._qReadings.get()
      
      self.AveUsDistanceInCm = sum(self._qReadings.queue, 0.0) / len(self._qReadings.queue)
      time.sleep(tSleep)
    print("do_run went false. Stopping pollUltrasonicDistance thread")

  def _echo1(self, gpio, level, tick):
    self.high = tick
      
  def _echo0(self, gpio, level, tick):
    self.pulseTravelTime = tick - self.high
    self.done = True

  def clearEcho(self):
    self.my_echo1.cancel()
    self.my_echo0.cancel()

  def setEcho(self, srvopin = None):
    if (srvopin == None):
       srvopin = UltrasonicDistance.EchoPin

    #  Echo on servopin - translate to GPIO pin
    self.my_echo1 = PDALib.pi.callback(PDALib.servopin[srvopin], pigpio.RISING_EDGE,  self._echo1)
    self.my_echo0 = PDALib.pi.callback(PDALib.servopin[srvopin], pigpio.FALLING_EDGE, self._echo0)


  # readDistance2gs(trig, _echo) for HC-SR04 only
  # Alan:   g: trigger is connected direct to a PiB+, Pi2, Pi3B gpio pin
  #         s: echo is connected to a PiDroidAlpha servo pin 0..7
  #
  # Alan: trig is gpioPin  (e.g. 26 for GPIO26 on pin 37)
  #       trig is a servoPin 0..7
  #

  def readDistance2gs(self, trig, echo):
    self.done = False
    PDALib.pi.set_mode(trig, pigpio.OUTPUT)
    PDALib.pi.gpio_trigger(trig, 50, 1)
    PDALib.pi.set_mode(PDALib.servopin[echo], pigpio.INPUT)
    time.sleep(0.0001)
    tim = 0
    while not self.done:
      time.sleep(0.001)
      tim = tim+1
      if tim > 50:
         return 0
    return self.pulseTravelTime / 58.068 # return as cm

  # #############################################
  # ULTRASONIC DISTANCE SENSOR INTERFACE METHODS

  # OFFSET TO PIVOT - distance from front of sensor to pan servo pivot point
  offsetInchesToPivot=2.0

  # inCm()
  #
  # return Distance in Centimeters (to sensor circuit board)

  def inCm(self, readings=1):
      if (readings > 1):
        usReading = self.AveUsDistanceInCm
      else:
        #  Distance from a single reading
        usReading =  self.usDistanceInCm
      return usReading 

  # inInches()
  #
  # return Distance in Inches (to sensor circuit board)

  def inInches(self, readings=1):
      if (readings > 1):
        usReading = self.AveUsDistanceInCm * 0.393701
      else:
        #  Distance from a single reading
        usReading =  self.usDistanceInCm * 0.393701
      return usReading 
    
  def read(self):  #READ THE UltrasonicDistance - can be used as poll or directly
      self.usDistanceInCm = self.readDistance2gs(self.TrigPin,self.EchoPin)
      return self.usDistanceInCm

  def readingsList(self):
      tmp = [item for item in self._qReadings.queue]
      # print "readingsList:", tmp
      return tmp

  def cancel(self):
     print "UltrasonicDistance.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for UtrasonicDistance.readThread to quit"
     self.pollThreadHandle.join()



# ##### UltrasonicDistance CLASS TEST METHOD ######
# the first time through the main() while loop, the sensors may not have been read yet
#     so UltrasonicDistance.status() and each UltrasonicDistance may have a value of 8/UNKNOWN 
def main():
  try:
    # note: usDistance is object, UltrasonicDistance is class 
    # create instance, start read (timesPerSec) thread
    usDistance = UltrasonicDistance(readingsPerSec=30)
    print "usDistance.tSleep:",usDistance.tSleep
    myPyLib.set_cntl_c_handler(usDistance.cancel)  # Set CNTL-C handler 
    while True:
      print "\n"
      print( "AveUsDistanceInCm: %.1f cm" %  usDistance.AveUsDistanceInCm )
      print  "usDistance.MAX_qReadings_QSIZE:",usDistance.MAX_qReadings_QSIZE
      print( "usDistance.inInches(1):%.2f, (%d):%.2f" % (usDistance.inInches(1),
		usDistance.MAX_qReadings_QSIZE,
		usDistance.inInches(UltrasonicDistance.MAX_qReadings_QSIZE) ))
      print "qReadings:" , usDistance.readingsList() 
      time.sleep(1)
    #end while
  except SystemExit:
    myPDALib.PiExit()
    print "usDistanceClass Test Main shutting down"
#  except:
#     print "Exception Raised"
#     usDistance.cancel()
#     myPDALib.PiExit()


if __name__ == "__main__":
    main()


