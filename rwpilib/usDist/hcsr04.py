#
# hcsr04.py    HC-SR04 sensor interface library
#
import time
import pigpio
import PDALib


def _echo1(gpio, level, tick):
   global _high
   _high = tick
      
def _echo0(gpio, level, tick):
   global _done, _high, _time
   _time = tick - _high
   _done = True


def clearEcho():
       global my_echo0, my_echo1
       my_echo1.cancel()
       my_echo0.cancel()

def setEcho(srvopin):
  global my_echo0, my_echo1
  # my_echo1 = pi.callback(22, pigpio.RISING_EDGE,  _echo1)
  # my_echo0 = pi.callback(22, pigpio.FALLING_EDGE, _echo0)

  # Alan - 14Jun2016 Echo on servopin 
  my_echo1 = PDALib.pi.callback(PDALib.servopin[srvopin], pigpio.RISING_EDGE,  _echo1)
  my_echo0 = PDALib.pi.callback(PDALib.servopin[srvopin], pigpio.FALLING_EDGE, _echo0)



# Alan McDonley
# readDistance2gs(_trig, _echo) for HC-SR04 only
# Alan:   g: trigger is connected direct to a PiB+, Pi2, Pi3B gpio pin
#         s: echo is connected to a PiDroidAlpha servo pin 0..7
#
# Alan: _trig is gpioPin  (e.g. 26 for GPIO26 on pin 37)
#       _echo is a servoPin 0..7
#


def readDistance2gs(_trig, _echo):
   global pi, _done, _time
   _done = False
   PDALib.pi.set_mode(_trig, pigpio.OUTPUT)
   PDALib.pi.gpio_trigger(_trig,50,1)
   PDALib.pi.set_mode(PDALib.servopin[_echo], pigpio.INPUT)
   time.sleep(0.0001)
   tim = 0
   while not _done:
      time.sleep(0.001)
      tim = tim+1
      if tim > 50:
         return 0
   return _time / 58.068 # return as cm

