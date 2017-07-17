#!/usr/bin/python
#
# speak.py   Speaker utilities
#

import subprocess

filename = 'speak.py.txt'

def say(phrase):
    file=open(filename,'w')
    file.write(phrase)
    file.close()
    # subprocess.call('festival --tts '+filename, shell=True)
    subprocess.Popen('festival --tts '+filename, shell=True)
    # subprocess.call('rm -f '+filename, shell=True)


# ##### MAIN ####
def main():
    # say("hello from speak dot p y test main")
    say("what's the weather, long quiet?")

if __name__ == "__main__":
    main()

