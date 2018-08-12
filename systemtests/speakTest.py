#!/usr/bin/python
#
# speakTest.py   Speaker utilities
#
#  speak.say(phrase)  do not include apostrophes in phrase

import sys
sys.path.append("/home/pi/RWPi/rwpilib")
import speak
import time

# ##### MAIN ####
def main():
    speak.say("whats the weather, long quiet?")
    time.sleep(2)
    speak.say("My name is Pogo.")

if __name__ == "__main__":
    main()

