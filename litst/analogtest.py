#!/usr/bin/python
#
# analogtest.py   Pure ADC CHANNELS TEST
#
# (channel 0 of 0..7 is Pololu IR 10-180cm=3v)
# (channel 6 of 0..7 is 7v2 unreg (9v max) 2:1 divider
# (channel 7 of 0..7 is the ACS712-05 current sensor output voltage)
#

import sys
sys.path.insert(0, '/home/pi/RWPi/rwpilib')
import PDALib
import myPDALib
import time
import signal
import li_batt

VBATT_LOW = li_batt.VBATT_LOW
VSUPPLY = li_batt.VSUPPLY
VLSB = li_batt.VLSB
VDIV = li_batt.VDIV
BATT_PIN = li_batt.BATT_PIN


# ################ Control-C Handling #########
def signal_handler(signal, frame):
  print('\n** Control-C Detected')
  myPDALib.PiExit()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# ###############




while True:
  print("\n")
  for pin in range(0,7+1):
      reading = myPDALib.analogRead12bit(pin)
      v_adc = reading * VLSB
      v_tst = v_adc * VDIV
      if (pin == BATT_PIN):
          print ( "pin %d reading: %d v_adc: %.2f v_tst: %.2f" % (pin, reading, round(v_adc,2), round(v_tst,2)) )
      else:
          print ( "pin %d reading: %d v_adc: %.2f" % (pin, reading, round(v_adc,2)) )
  time.sleep(1.0)


myPDALib.PiExit()
  
  

