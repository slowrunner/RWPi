#!/usr/bin/python3
#
# adctest.py   Test noise on DC voltage
#
# (channel 0 of 0..7 is 5v supply)
# (channel 6 of 0..7 is 3:1 divider test channel)

# Results -- no capacitor on supply
# SUPPLY: ave:  5.20 min:  5.18 max:  5.20  std: 0.003 lsb: 0.001 snr: 2004
# TEST  : ave: 10.99 min: 10.94 max: 11.11  std: 0.023 lsb: 0.001 snr: 470

import sys
sys.path.insert(0, '/home/pi/RWPi/rwpilib')
import PDALib
import myPDALib
import time
import signal
import li_batt
import numpy as np

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


NUM_SAMPLES = 1000
PIN_SUPPLY = 0
PIN_TEST = 6

v_readings_supply = []
v_readings_test = []

loopcount = 0
LOOPS = 1

print("\nMeasuring SUPPLY and TEST channels ")
while (loopcount < LOOPS):
    loopcount += 1
    for sample in range(NUM_SAMPLES):
        time.sleep(0.001)
        v_readings_supply += [myPDALib.analogRead12bit(PIN_SUPPLY)]
        time.sleep(0.001)
        v_readings_test += [myPDALib.analogRead12bit(PIN_TEST)]

    v_lsb_supply = round(VLSB,3)
    v_ave_supply = np.average(v_readings_supply) * VLSB
    v_min_supply = np.amin(v_readings_supply) * VLSB
    v_max_supply = np.amax(v_readings_supply) * VLSB
    v_std_supply = np.std(v_readings_supply) * VLSB
    if (v_std_supply != 0):
        v_snr_supply = v_ave_supply / v_std_supply
    else:
        v_snr_supply = 999.9

    v_lsb_test = round(VLSB * VDIV, 3)
    v_ave_test = np.average(v_readings_test) * VLSB * VDIV
    v_min_test = np.amin(v_readings_test) * VLSB * VDIV
    v_max_test = np.amax(v_readings_test) * VLSB * VDIV
    v_std_test = np.std(v_readings_test) * VLSB * VDIV
    if (v_std_test != 0):
        v_snr_test = v_ave_test / v_std_test
    else:
        v_snr_test = 999.9

    print("Results --")
    print("SUPPLY: ave:  {:0.2f} min:  {:0.2f} max:  {:0.2f}  std: {:0.3f} lsb: {:0.3f} snr: {:0.0f}".format(
                v_ave_supply, v_min_supply, v_max_supply, v_std_supply, v_lsb_supply, v_snr_supply))
    print("TEST  : ave: {:0.2f} min: {:0.2f} max: {:0.2f}  std: {:0.3f} lsb: {:0.3f} snr: {:0.0f}".format(
                v_ave_test, v_min_test, v_max_test, v_std_test, v_lsb_supply, v_snr_test))
    print("\n")

myPDALib.PiExit()

