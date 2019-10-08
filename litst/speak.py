#!/usr/bin/python3

# speak.py

import subprocess
import sys


def say_flite(phrase):
    try:
        subprocess.check_output(['flite -t {}'.format(phrase)], stderr=subprocess.STDOUT, shell=True)
    except KeyboardInterrupt:
        sys.exit(0)

def say(phrase):
    say_flite(phrase)
    print("saying:",phrase)


def main():
    if (len(sys.argv) > 1):
        strToSay = sys.argv[1]
        say(strToSay)
    else:
        print("Usage: ./speak.py \"phrase to say\" ")
