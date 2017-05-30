#!/usr/bin/python
#
# template.py   TEMPLATE
#

import PDALib
import myPDALib
import myPyLib

import time






# ##### MAIN ######
def main():
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  while True:
      print "Begin Template"
      time.sleep(1)
  #end while

if __name__ == "__main__":
    main()

