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
import argparse
import li_batt




VBATT_LOW = li_batt.VBATT_LOW
VSUPPLY = li_batt.VSUPPLY
VLSB = li_batt.VLSB
VDIV = li_batt.VDIV
BATT_PIN = li_batt.BATT_PIN


LOOP_DELAY = 30
TENTH_HOUR = int(6 * 60 / LOOP_DELAY)
LOW_V_DURATION = 120  # seconds
SHUTDOWN_LIMIT = int(LOW_V_DURATION / LOOP_DELAY)

def signal_handler(signal, frame):
  print('\n** Control-C Detected')
  myPDALib.PiExit()
  sys.exit(0)


def getUptime():
  res = os.popen('uptime').readline()
  return res.replace("\n","")


def main():

    # ARGUMENT PARSING
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--batt", required=True, help="battery name string")
    ap.add_argument("-n", "--noshutdown", default=False, action='store_true', help="will not shutdown, warning only")
    args = vars(ap.parse_args())
    batt_name = args['batt']
    noShutdown = args['noshutdown']

    signal.signal(signal.SIGINT, signal_handler)

    # create logger
    lifelogger = logging.getLogger('lifelog')
    lifelogger.setLevel(logging.INFO)
    lifeloghandler = logging.FileHandler('/home/pi/RWPi/life.log')
    lifelogformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
    lifeloghandler.setFormatter(lifelogformatter)
    lifelogger.addHandler(lifeloghandler)

    # create battery logger
    battlogger = logging.getLogger(batt_name)
    battlogger.setLevel(logging.INFO)
    battloghandler = logging.FileHandler('/home/pi/RWPi/litst/'+batt_name+'.log')
    battlogformatter = logging.Formatter('%(asctime)s|%(message)s',"%Y-%m-%d %H:%M")
    battloghandler.setFormatter(battlogformatter)
    battlogger.addHandler(battloghandler)

    nLow = 0
    loopcount = 0

    print("Starting li_batt_life.py - logging to "+batt_name+".log")
    print("LOOP_DELAY: {}s  TENTH_HOUR: {} loops LIMIT: {} times low".format(LOOP_DELAY, TENTH_HOUR, SHUTDOWN_LIMIT))

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
            strToLog = "** {:.2f} v START {} **".format(round(v_ave,2),batt_name)
            lifelogger.info(strToLog)
            battlogger.info(strToLog)
            print(strTime, strToLog)
        # every 6 minutes (0.1h) log voltage
        if (loopcount % TENTH_HOUR) == 0:
            strToLog = "** {:.2f} v **".format(round(v_ave,2))
            battlogger.info(strToLog)

        if (v_ave < VBATT_LOW):
            nLow+=1
            print("WARNING: *************  nLow: ",nLow)
        else: nLow = 0

        strTime = time.strftime("%H:%M:%S")
        print(strTime,"|** {:.2f} v **".format(round(v_ave,2)))

        if (nLow > SHUTDOWN_LIMIT):  # enough times low, we're out of here
          if (noShutdown is False):
            print("WARNING WARNING WARNING SHUTTING DOWN")
            strToLog = "** {:.2f} v SHUTDOWN {} **".format(round(v_ave,2),batt_name)
            lifelogger.info(strToLog)
            battlogger.info(strToLog)
            print(strTime,strToLog)
            os.system("sudo shutdown -h +1")
            sys.exit(0)
          else:
            print("WARNING WARNING WARNING")
            strToLog = "** {:.2f} volts {} **".format(round(v_ave,2),batt_name)
            lifelogger.info(strToLog)
            battlogger.info(strToLog)
            print(strTime,strToLog)

        time.sleep(LOOP_DELAY-1)  # adjust for activities
    # end while

    myPDALib.PiExit()

if __name__ == "__main__":
    main()
