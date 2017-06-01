#!/usr/bin/python
#
# PDALibThreadTest.py   PDALib THREADING TEST
#

import PDALib
import myPyLib
import time
import sys
import threading
import signal
from datetime import datetime

# DIO 8..11 will be used as input testing

  # DIO 12 (A4)	Motor 1 Dir A (0=coast 1=F/Brake)
  # DIO 13 (A5)	Motor 1 Dir B (0=coast 1=R/Brake)

  # DIO 14 (A6)	Motor 2 Dir A (0=coast 1=F/Brake)
  # DIO 15 (A7)	Motor 2 Dir B (0=coast 1=R/Brake)

M1DirA = 12
M1DirB = 13
M2DirA = 14
M2DirB = 15

# SRV 4 (pin 3 of 0..7)  is unassigned (on my bot), use for servo read/write
SRVpin = 3




# ### PIN MODE INPUT CLASS ##################

class PinModeInput():

  # CLASS VARS (Avail to all instances)
  # Access as PinModeInput.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the PinModeInput class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (PinModeInput.pollThreadHandle!=None): 
        print "Second PinModeInput Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "PinModeInput worker thread readingsPerSec:",readingsPerSec
    PinModeInput.tSleep=1.0/readingsPerSec    #compute desired sleep
    PinModeInput.pollThreadHandle = threading.Thread( target=self.pollPinModeInput, 
                                               args=(PinModeInput.tSleep,))
    PinModeInput.pollThreadHandle.start()
    print "PinModeInput worker thread told to start"
  #end init()

  # PinModeInput THREAD WORKER METHOD TO READ PinModeInput
  def pollPinModeInput(self,tSleep=0.1):     
    print "pollPinModeInput started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingPinModeInput thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.do()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollPinModeInput thread")

    
  def do(self):  #set PinMode to Input - can be used as poll or directly
      for pin in range(8,11+1):
          PDALib.pinMode(pin,PDALib.INPUT) 
      print "pinMode(8..11) set to input "
       
       
      return   # PinModeInput.do


  def cancel(self):
     print "PinModeInput.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for PinModeInput.workerThread to quit"
     self.pollThreadHandle.join()

# ### END OF PIN MODE INPUT


# ### PIN MODE OUTPUT CLASS #########################

class PinModeOutput():

  # CLASS VARS (Avail to all instances)
  # Access as PinModeOutput.class_var_name


  pollThreadHandle=None   # the SINGLE read sensor thread for the PinModeOutput class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (PinModeOutput.pollThreadHandle!=None): 
        print "Second PinModeOutput Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "PinModeOutput worker thread readingsPerSec:",readingsPerSec
    PinModeOutput.tSleep=1.0/readingsPerSec    #compute desired sleep
    PinModeOutput.pollThreadHandle = threading.Thread( target=self.pollPinModeOutput, 
                                               args=(PinModeOutput.tSleep,))
    PinModeOutput.pollThreadHandle.start()
    print "PinModeOutput worker thread told to start"
  #end init()

  # PinModeOutput THREAD WORKER METHOD TO READ PinModeOutput
  def pollPinModeOutput(self,tSleep=0.1):     
    print "pollPinModeOutput started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingPinModeOutput thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.do()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollPinModeOutput thread")

    
  def do(self):  #set PinMode to Input - can be used as poll or directly
      PDALib.pinMode(M1DirA,PDALib.OUTPUT)  #init motor1 dirA/Fwd    enable
      PDALib.pinMode(M1DirB,PDALib.OUTPUT)  #init motor1 dirB/Bkwd  enable
      PDALib.pinMode(M2DirA,PDALib.OUTPUT)  #init motor2 dirA/Fwd    enable
      PDALib.pinMode(M2DirB,PDALib.OUTPUT)  #init motor2 dirB/Bkwd  enable
      print "pinMode(12..15) set to OUTPUT "
       
       
      return   # PinModeOutput.do


  def cancel(self):
     print "PinModeOutput.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for PinModeOutput.workerThread to quit"
     self.pollThreadHandle.join()

# ### END OF PIN MODE OUTPUT

# ### MOTOR DIRECTION CLASS ############################

class MotorDirs():

  # CLASS VARS (Avail to all instances)
  # Access as MotorDirs.class_var_name
  motorDir = 0


  pollThreadHandle=None   # the SINGLE read sensor thread for the MotorDirs class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (MotorDirs.pollThreadHandle!=None): 
        print "Second MotorDirs Class Object, not starting pollingThread"
        return None
    PDALib.pinMode(M1DirA,PDALib.OUTPUT)  #init motor1 dirA/Fwd    enable
    PDALib.pinMode(M1DirB,PDALib.OUTPUT)  #init motor1 dirB/Bkwd  enable
    PDALib.pinMode(M2DirA,PDALib.OUTPUT)  #init motor2 dirA/Fwd    enable
    PDALib.pinMode(M2DirB,PDALib.OUTPUT)  #init motor2 dirB/Bkwd  enable


    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "MotorDirs worker thread readingsPerSec:",readingsPerSec
    MotorDirs.tSleep=1.0/readingsPerSec    #compute desired sleep
    MotorDirs.pollThreadHandle = threading.Thread( target=self.pollMotorDirs, 
                                               args=(MotorDirs.tSleep,))
    MotorDirs.pollThreadHandle.start()
    print "MotorDirs worker thread told to start"
  #end init()

  # MotorDirs THREAD WORKER METHOD TO READ MotorDirs
  def pollMotorDirs(self,tSleep=0.1):     
    print "pollMotorDirs started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingMotorDirs thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.do()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollMotorDirs thread")

    
  def do(self):  #set motor dirs to all 0 - can be used as poll or directly

      # toggle all direction pins 
      self.motorDir = (self.motorDir + 1) % 2
      PDALib.digitalWrite(M1DirA,self.motorDir)  #set 
      PDALib.digitalWrite(M1DirB,self.motorDir)  #set
      PDALib.digitalWrite(M2DirA,self.motorDir)  #set 
      PDALib.digitalWrite(M2DirB,self.motorDir)  #set 
      print "digitalWrite MotorDirs to %d " % self.motorDir
      
       
       
      return   # MotorDirs.do


  def cancel(self):
     print "MotorDirs.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for MotorDirs.workerThread to quit"
     self.pollThreadHandle.join()

# ### END OF MOTOR DIRS

     


# ### READ MODE CLASS #######################################

class ReadMode():

  # CLASS VARS (Avail to all instances)
  # Access as ReadMode.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the ReadMode class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (ReadMode.pollThreadHandle!=None): 
        print "Second ReadMode Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "ReadMode worker thread readingsPerSec:",readingsPerSec
    ReadMode.tSleep=1.0/readingsPerSec    #compute desired sleep
    ReadMode.pollThreadHandle = threading.Thread( target=self.pollReadMode, 
                                               args=(ReadMode.tSleep,))
    ReadMode.pollThreadHandle.start()
    print "ReadMode worker thread told to start"
  #end init()

  # ReadMode THREAD WORKER METHOD TO READ ReadMode
  def pollReadMode(self,tSleep=0.1):     
    print "pollReadMode started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingReadMode thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.read()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollReadMode thread")

    
  def read(self):  #READ THE ReadMode - can be used as poll or directly
      pinmode=[]
      for pin in range(0,23+1):
          pinmode.append( PDALib.readMode(pin) )
      print "readMode(0..23): ",pinmode
      return   # ReadMode.state


  def cancel(self):
     print "ReadMode.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for ReadMode.workerThread to quit"
     self.pollThreadHandle.join()

# ### END OF READ MODE

# ### READ ANALOG CLASS #################################

class ReadAnalog():

  # CLASS VARS (Avail to all instances)
  # Access as ReadAnalog.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the ReadAnalog class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (ReadAnalog.pollThreadHandle!=None): 
        print "Second ReadAnalog Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "ReadAnalog worker thread readingsPerSec:",readingsPerSec
    ReadAnalog.tSleep=1.0/readingsPerSec    #compute desired sleep
    ReadAnalog.pollThreadHandle = threading.Thread( target=self.pollReadAnalog, 
                                               args=(ReadAnalog.tSleep,))
    ReadAnalog.pollThreadHandle.start()
    print "ReadAnalog worker thread told to start"
  #end init()

  # ReadAnalog THREAD WORKER METHOD TO READ ReadAnalog
  def pollReadAnalog(self,tSleep=0.1):     
    print "pollReadAnalog started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingReadAnalog thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.read()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollReadAnalog thread")

    
  def read(self):  #READ THE ReadAnalog - can be used as poll or directly
      valueDAC=[]
      for pin in range(0,7+1):
          valueDAC.append( PDALib.analogRead(pin) )
      print "analogRead(0..7): ",valueDAC
      return   # ReadAnalog.read

  def cancel(self):
     print "ReadAnalog.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for ReadAnalog.workerThread to quit"
     self.pollThreadHandle.join()

# ### END OF READ ANALOG

# ### SERVO READ CLASS ####################################

class ServoRead():

  # CLASS VARS (Avail to all instances)
  # Access as ServoRead.class_var_name

  pollThreadHandle=None   # the SINGLE read sensor thread for the ServoRead class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (ServoRead.pollThreadHandle!=None): 
        print "Second ServoRead Class Object, not starting pollingThread"
        return None
    PDALib.pinMode(SRVpin,PDALib.PWM)  # init free pin to PWM

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "ServoRead worker thread readingsPerSec:",readingsPerSec
    ServoRead.tSleep=1.0/readingsPerSec    #compute desired sleep
    ServoRead.pollThreadHandle = threading.Thread( target=self.pollServoRead, 
                                               args=(ServoRead.tSleep,))
    ServoRead.pollThreadHandle.start()
    print "ServoRead worker thread told to start"
  #end init()

  # ServoRead THREAD WORKER METHOD TO READ ServoRead
  def pollServoRead(self,tSleep=0.1):     
    print "pollServoRead started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingServoRead thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.read()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollServoRead thread")

    
  def read(self):  #READ THE ServoRead - can be used as poll or directly
       srvValue=PDALib.servoRead(SRVpin)
       print "SERVOREAD: servoRead(%d) = %d uS" % (SRVpin, srvValue)
       return   # ServoRead.state


  def cancel(self):
     print "ServoRead.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for ServoRead.workerThread to quit"
     self.pollThreadHandle.join()

# END OF ServoRead CLASS


# ### SERVO WRITE CLASS #########################################

class ServoWrite():

  # CLASS VARS (Avail to all instances)
  # Access as ServoWrite.class_var_name
  lastServoSetting = 1250  # start at center of range

  pollThreadHandle=None   # the SINGLE read sensor thread for the ServoWrite class   
  tSleep=0.1            # time for read_sensor thread to sleep 
 

  # end of class vars definition

  def __init__(self,readingsPerSec=10):
    # SINGLETON TEST 
    if (ServoWrite.pollThreadHandle!=None): 
        print "Second ServoWrite Class Object, not starting pollingThread"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A THREAD
    # threading target must be an instance
    print "ServoWrite worker thread readingsPerSec:",readingsPerSec
    ServoWrite.tSleep=1.0/readingsPerSec    #compute desired sleep
    ServoWrite.pollThreadHandle = threading.Thread( target=self.pollServoWrite, 
                                               args=(ServoWrite.tSleep,))
    ServoWrite.pollThreadHandle.start()
    print "ServoWrite worker thread told to start"
  #end init()

  # ServoWrite THREAD WORKER METHOD TO READ ServoWrite
  def pollServoWrite(self,tSleep=0.1):     
    print "pollServoWrite started with %f" % tSleep
    t = threading.currentThread()   # get handle to self (pollingServoWrite thread)
    while getattr(t, "do_run", True):  # check the do_run thread attribute
      self.do()
      time.sleep(tSleep)
    print("do_run went false. Stopping pollServoWrite thread")

    
  def do(self):  #do THE ServoWrite - can be used as poll or directly
       self.lastServoSetting = (self.lastServoSetting + 1) % 2501
       PDALib.servoWrite(SRVpin,self.lastServoSetting) # set to new position
       return   # ServoWrite.do


  def cancel(self):
     print "ServoWrite.cancel() called"
     self.pollThreadHandle.do_run = False
     print "Waiting for ServoWrite.workerThread to quit"
     self.pollThreadHandle.join()

# END OF ServoWrite CLASS


# ##### PDALib MULTI-THREAD TEST #########################################


# ######### CNTL-C ##############################
# Callback and setup to catch control-C and quit program

_funcToRun=None

def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  if (_funcToRun != None):
     _funcToRun()
  sys.exit(0)     # raise SystemExit exception

# Setup the callback to catch control-C
def set_cntl_c_handler(toRun=None):
  global _funcToRun
  _funcToRun = toRun
  signal.signal(signal.SIGINT, signal_handler)

# #########



# CANCEL ALL THREADS - Control-C callback function

def cancelAll():
    global readMode,pinModeInput,pinModeOutput,motorDirs,readServo,writeServo

    readMode.cancel()
    pinModeInput.cancel()
    pinModeOutput.cancel()
    motorDirs.cancel()
    readDAC.cancel()
    readServo.cancel()
    writeServo.cancel()
  

###################  PDALib Threading Test Main() ########

def main():
  global readMode,pinModeInput,pinModeOutput,motorDirs,readDAC,readServo,writeServo
  # note: lowercase X is object, uppercase X is class (everywhere in code)

  print "PDALib Thread Test Started.  Ctrl-C to end" 
  
  # Create all threads (loops per second)
  readMode=ReadMode(11)  #create an instance which starts the readMode thread
  pinModeInput=PinModeInput(12)
  pinModeOutput=PinModeOutput(13)
  motorDirs=MotorDirs(14)
  readDAC=ReadAnalog(15)
  readServo=ServoRead(16)
  writeServo=ServoWrite(17)

  set_cntl_c_handler(cancelAll)  # Set CNTL-C handler 
   
  try:
    while True:
      print "\n MAIN executing", datetime.now
      time.sleep(1)
    #end while
  except SystemExit:
    PDALib.RoboPiExit()
    print "PDALib Thread Test: Bye Bye"    
  except:
    print "Exception Raised"
    cancelAll()
    traceback.print_exc()  

# TO RUN THIS TEST:   ##############################
# chmod a+x PDALibThreadTest.py
# ./PDALibThreadTest.py

if __name__ == "__main__":
    main()


