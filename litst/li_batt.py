#!/usr/bin/python3

# li_batt.py    # lithium battery constants

VBATT_FULL = 12.6
VBATT_LOW = 10.8

# Supply and reference voltages when running on lithium battery

VSUPPLY = 5.20  # 5.07
VLSB = VSUPPLY / 4095.0
# 198.4 K ohm resister from 12v test to input of ADC, 
# 99K resister from 12v test/ADC input to 12v ground
# 12v ground not connected to ADC ground
VDIV = 3.5 # 0.2845 = 1v ??  3.156   # roughly 3:1  0.317v = 1v
BATT_PIN = 6

