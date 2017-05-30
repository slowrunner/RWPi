#!/usr/bin/python

import datetime
import time

print 'Starting logfLife at %s' % time.ctime()

f = open('logfLife.log','a')
f.write( 'Starting logLife at %s \n' % time.ctime() )
f.close()

while 1 :
  try: 
    f = open('logfLife.log','a')
    f.write( 'Alive at: %s \n' % time.ctime()   )
    f.close()
    print 'Alive at: %s' % time.ctime()
    time.sleep( 60 )
  except:
    f = open('logfLife.log', 'a')
    f.write( 'Stopping logLife at %s \n' % time.ctime() )
    f.close()
    print'Stopping logLife at %s' % time.ctime()
    break

