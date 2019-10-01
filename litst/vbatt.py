#!/usr/bin/python3
#
# vbatt.py   get battery voltage
#
# (channel 6 of 0..7 is 3:1 divider test channel)


import sys
sys.path.insert(0, '/home/pi/RWPi/rwpilib')
import PDALib
import myPDALib
import li_batt
import numpy as np

VBATT_LOW = li_batt.VBATT_LOW
VSUPPLY = li_batt.VSUPPLY
VLSB = li_batt.VLSB
VDIV = li_batt.VDIV
BATT_PIN = li_batt.BATT_PIN


NUM_SAMPLES = 10
PIN_TEST = 0   # 6 for battery

v_readings_test = []

for sample in range(NUM_SAMPLES):
        # time.sleep(0.001)
        v_readings_test += [myPDALib.analogRead12bit(PIN_TEST)]

v_ave_test = np.average(v_readings_test) * VLSB * VDIV
print("{:0.2f}".format(round(v_ave_test,2)))

# myPDALib.PiExit()

