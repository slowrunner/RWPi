#!/usr/bin/python
#
# test_myPyLib.py   TEST FOR myPyLib.py
#

#import PDALib
#import myPDALib
import myPyLib
import time

# ######### SET CNTL-C HANDLER #####
myPyLib.set_cntl_c_handler()

while True:
    print "Test myPyLib"
    time.sleep(1)
#end while

