#!/usr/bin/python
#
# dioDump.py   DIO Chip MCP23S17 TEST
#

import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import PDALib
import myPDALib
import time
import signal

# ################ Control-C Handling #########
def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# ###############




while True:
  print "\nDIO Chip MCP23S17 Dump"
  print "**** dumpDio() ****"
  PDALib.dumpDio()
  time.sleep(2.0)


myPDALib.PiExit()

