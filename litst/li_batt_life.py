#!/usr/bin/python3
#
# li_batt_life.py  Lithium BATTERY LIFE TEST
#
# The 12.6v - 10.8v battery voltage through 0.318:1 divider should be connected to
#      ADC6 (pin 6) for this test
#
# This test will loop reading the voltage on ADC6 and current (pin 7)
#      UNTIL voltage drops below 10.8v  5 times,
#      then will issue a shutdown 
#
# Start this test with $ ./li_batt_life.py
#
import sys
sys.path
sys.path.append('/home/pi/RWPi')

import rwpilib.PDALib as PDALib
import rwpilib.myPDALib as myPDALib
import time
import signal
# import rwpilib.currentsensor as currentsensor
import os
import numpy as np
import logging


# create logger
# logger = logging.getLogger(__name__)
logger = logging.getLogger('lifelog')
logger.setLevel(logging.INFO)

# Uncomment the following to test lifeLog.py locally
# loghandler = logging.FileHandler('/home/pi/Carl/Projects/LifeLog/test_life.log')
# Uncomment the following in plib
loghandler = logging.FileHandler('/home/pi/RWPi/life.log')

logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)



VBATT_LOW = 10.8
VSUPPLY = 5.20  # 5.07
VLSB = VSUPPLY / 4095.0
VDIV = 3.156   # roughly 3:1  0.317v = 1v
BATT_PIN = 6

def signal_handler(signal, frame):
  print('\n** Control-C Detected')
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def getUptime():
  res = os.popen('uptime').readline()
  return res.replace("\n","")

nLow = 0
loopcount = 0

while True:

  #print ("current_sense(): %.0f mA" % currentsensor.current_sense(1000))
  v_list = []
  for i in range(10):
      adc_reading = myPDALib.analogRead12bit(BATT_PIN)
      v_reading = VLSB * adc_reading
      v_now = v_reading * VDIV
      v_list += [v_now]
      time.sleep(0.1)
  # print("v_list:",v_list)
  v_ave = np.average(v_list)
  loopcount +=1
  strTime = time.strftime("%H:%M:%S")

  if loopcount == 1:
      strToLog = "** Start at {} {:.2f}v **".format(strTime, round(v_ave,2))
      logger.info(strToLog)

  if (v_ave < VBATT_LOW):
          nLow+=1
          print("WARNING: *************  nLow: ",nLow)
  else: nLow = 0
  strTime = time.strftime("%H:%M:%S")
  print(strTime,", {:.2f}".format(round(v_ave,2)))
  if (nLow >4):  # five times lower we're out of here
          print("WARNING WARNING WARNING SHUTTING DOWN")
          strToLog = "** Shutting Down at {} {:.2f}v **".format(strTime, round(v_ave,2))
          logger.info(strToLog)
          os.system("sudo shutdown -h +1")
          sys.exit(0)
  time.sleep(5)
# end while

myPDALib.PiExit()

