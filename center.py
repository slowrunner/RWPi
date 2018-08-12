#!/usr/bin/python
#
# center.py   Center servos 
#
import sys
sys.path.append("/home/pi/RWPi/rwpilib")

import tiltpan
import time


def main():
    tiltpan.setup_servo_pins()
    tiltpan.center_servos()
    time.sleep(0.5)
    tiltpan.servos_off()
    print "Servos Centered"




if __name__ == "__main__":
    main()
