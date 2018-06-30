#!/usr/bin/python
#
# lifelog.py   digital entity
#

import time
import sys
import multiprocessing
import logging
import traceback
import signal


# create logger
logger = logging.getLogger('lifelog')
logger.setLevel(logging.INFO)
loghandler = logging.FileHandler('/home/pi/RWPi/life.log')
logformatter = logging.Formatter('%(asctime)s|%(message)s')
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)
logger.info('-------------')  

debugLevel = 0

# ######### CNTL-C #####
# Callback and setup to catch control-C and quit program

_funcToRun=None

def signal_handler(signal, frame):
  if debugLevel: print '\n** Control-C Detected'
  if (_funcToRun != None):
     _funcToRun()
  sys.exit(0)     # raise SystemExit exception

# Setup the callback to catch control-C
def set_cntl_c_handler(toRun=None):
  global _funcToRun
  _funcToRun = toRun
  signal.signal(signal.SIGINT, signal_handler)


class digitalEntity():

  # CLASS VARS (Avail to all instances)
  # Access as X.class_var_name

  pHandle=None   # the SINGLE execution thread for the X class   
  defaultSleep=60.0  # sleep for 1 minute by default

  # end of class vars definition

  def __init__(self,dEname,tSleep=defaultSleep):     #run about once a minute 
    # SINGLETON TEST 
    if (digitalEntity.pHandle!=None): 
        if debugLevel: print "Second digitalEntity, not starting"
        return None

    # INITIALIZE CLASS INSTANCE

    # START A Process
    # process target must be an instance
    digitalEntity.pHandle = multiprocessing.Process(name=dEname, target=self.dEmain, 
                                               args=(tSleep,))
    digitalEntity.pHandle.start()
    if debugLevel: print "%s.digitalEntity told to start" % dEname
  #end init()

  # digitalEntity main process
  def dEmain(self,tSleep=defaultSleep):   
    myname = multiprocessing.current_process().name  
    if debugLevel: print "%s.dEmain started with tSleep=%f" % (myname,tSleep)
    # logger.info('%s.dEmain started',myname)
    i=0
    while True:
        if debugLevel: print "%s.dEmain execution %i" % (myname,i)
        logger.info('%s.dEmain execution: %i',myname, i )
        i+=1
        time.sleep(tSleep)
    

    if debugLevel: print("dEmain end reached")

  def cancel(self):
     myname = multiprocessing.current_process().name  
     if debugLevel: print "%s.cancel() called" % myname
     logger.info('%s.cancel() called',myname)
     if debugLevel: print "\nWaiting for %s dE.workerThread to quit\n" % self.pHandle.name
     self.pHandle.join()
     if debugLevel: print "%s.cancel() complete" % myname     
 

# ##### digitalEntity tt ######
# 

def main():

  tt=digitalEntity(dEname="lifelog",tSleep=3600)  #create 
  set_cntl_c_handler(tt.cancel)

  try:
    while True:
      if debugLevel: print "\n lifelog.py: main()"
      time.sleep(3600)
    #end while
  except SystemExit:
    if debugLevel: print "lifelog.py: Bye Bye"    
  except:
    if debugLevel: print "Exception Raised"
    traceback.print_exc()  

if __name__ == "__main__":
    main()



