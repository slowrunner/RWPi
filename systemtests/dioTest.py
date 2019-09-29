#!/usr/bin/python
#
# dioTest.py   DIO Chip MCP23S17 TEST
#
#  Tests unused lines for input and output
#    and used for input lines
#    Does not test output lines
#
# (PDALib "Pin" 12-15 are motor dir output lines - 4bits)
# PDALib "Pin" 16-18 are Bumper input with pull-up - 3bits
# PDALib "Pin" 19-20 are Encoder input with pull-up, int-enabled, both - 2bits
# PDALib "Pin" 8-11, 21-23 are unused DIO lines - 7bits

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
  print "\nDIO Chip MCP23S17 Test"
  print "**** dumpDio() ****"
  PDALib.dumpDio()
  print "\n"
  print "**Setting all 16 lines to input with pull-up"
  for pin in range(8,23+1):
      stat=PDALib.pinMode(pin,PDALib.INPUT)
      stat=PDALib.setDioBit( PDALib.DIO_GPPU, pin-8 )
      print "pin %2d mode: %d (0=INPUT) PU: %d" % (pin, PDALib.readMode(pin),PDALib.getDioBit(PDALib.DIO_GPPU, pin-8))
  print "\n"
  time.sleep(0.1)
  for pin in range(8,23+1):
      if (pin == 12):
        print ( "R Motor Dir F pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 13):
        print ( "R Motor Dir R pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 14):
        print ( "L Motor Dir F pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 15):
        print ( "L Motor Dir R pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 16):
        print ( "Rear        Bumper pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 17):
        print ( "Right Front Bumper pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 18):
        print ( "Left Front  Bumper pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 19):
        print ( "Right Encoder  pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      elif (pin == 20):
        print ( "Left  Encoder  pin %d  state:: %d" % (pin, PDALib.digitalRead(pin) ) )
      else:
        print ( "pin %2d state:: %d" % (pin, PDALib.digitalRead(pin) ) )
  time.sleep(2.0)


myPDALib.PiExit()

