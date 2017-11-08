#!/usr/bin/python
#
# speak.py   Speaker utilities
#
#  say(phrase)  do not include apostrophes in phrase

import subprocess
import time

filename = 'speak.py.txt'

def say_festival(phrase):
    file=open(filename,'w')
    file.write(phrase)
    file.close()
    # subprocess.call('festival --tts '+filename, shell=True)
    subprocess.Popen('festival --tts '+filename, shell=True)
    # subprocess.call('rm -f '+filename, shell=True)

def say_espeak(phrase):
    subprocess.check_output(['espeak',phrase], stderr=subprocess.STDOUT)

def say(phrase):
    say_espeak(phrase)

# ##### MAIN ####
def main():
    # say("hello from speak dot p y test main")
    # say_festival("what's the weather, long quiet?")
    # say_espeak("whats the weather, long quiet?")
    say("My name is Pogo.")

if __name__ == "__main__":
    main()

