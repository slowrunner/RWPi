#!/usr/bin/python
#
# center.py   Center servos 
#

import rwpilib.tiltpan as tiltpan
import time


def main():
    tiltpan.setup_servo_pins()
    tiltpan.center_servos()
    time.sleep(1.0)
    tiltpan.servos_off()
    print "Servos Centered"




if __name__ == "__main__":
    main()
