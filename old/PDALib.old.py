#
# PDALib.py	Python API for Pi Droid Alpha educational robot controller
#
# Copyright 2015 William Henning
# http://Mikronauts.com
#
# PDALib provides an implementation of the RoboPi advanced robot controller for
# the Pi Droid Alpha educational robot controller.
#
# Please see the Pi Droid Alpha User Manual for documentation
#
# Aug.25/2015: v0.90 release (readDistance() not reliable)
# Aug.29/2015: v0.90.1 Alan McDonley proposed edits

import spidev
import pigpio

# pin 0-7  = Pi GPIO's
# pin 8-23 = Dio bits

INPUT  = 0
OUTPUT = 1
PWM    = 2
SERVO  = 3
PING   = 4

PWM_f  = 490  # Mikronauts default: 490

mode     = [0,0,0,0,0,0,0,0]
diomode  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
servopin = [4, 17, 18, 27, 22, 23, 24, 25]
servoval = [0, 0, 0, 0, 0, 0, 0, 0]
req12    = [[6,0,0], [6,64,0],[6,128,0],[6,192,0],[7,0,0], [7,64,0],[7,128,0],[7,192,0]]
req10    = [[1,128,0], [1,144,0],[1,160,0],[1,176,0],[1,192,0], [1,208,0],[1,224,0],[1,240,0]]

DIO_DIR  = 0x00 # I/O direction register, 0=output, 1=input
DIO_POL  = 0x02 # polarity invert config, if 1 inverted logic for pin
DIO_GPPU = 0x0C # pullup configuration register, 1 enables pullup for pin
DIO_GPIO = 0x12 # pin values
DIO_OLAT = 0x14 # output latch

pi       = pigpio.pi()
spi      = spidev.SpiDev()

spi.open(0,0)              # open(port,CS) port=0, CS=0|1
spi.max_speed_hz=1953000   # default speed undervalued divided voltages
spi.xfer([0x40,0xff,0xff]) # sets all pins as inputs
spi.close()                # A. McDonley


#
# Initialize library - for RoboPi compatibility, ignores arguments
#

def RoboPiInit(device, bps):
  return 0


#
# Shut down library (close connections and open file handles)
#

def RoboPiExit():
  pi.stop()

def LibExit():          # A. McDonley
  pi.stop()

#
# return the current mode of digital pins (0..23)
#
# 0..7  are Raspberry Pi pins on the Servo header (PWM, SERVO, INPUT, OUTPUT, PING)
# 8..23 are DIO A0-A7 and B0-B7 respectively (INPUT, OUTPUT)
#

def readMode(pin):
  if pin < 0:
    return -1
  if pin < 8:
    return mode[pin]
  if pin < 24:
    return diomode[pin-8]
  return -1

#
# set the current mode of digital pins (0..23)
#
# 0..7  are Raspberry Pi pins on the Servo header (PWM, SERVO, INPUT, OUTPUT, PING)
# 8..23 are DIO A0-A7 and B0-B7 respectively (INPUT, OUTPUT)
#

def pinMode(pin,newmode):
  if pin < 0:
    return -1
  if pin < 8: # only accept valid modes
    if mode[pin] == PWM: # stop PWM if setting for input or output
       pi.set_PWM_dutycycle(servopin[pin],0)
    if newmode == INPUT:
       mode[pin] = newmode
       pi.set_mode(servopin[pin], pi.INPUT)
    if newmode == OUTPUT:
       mode[pin] = newmode
       pi.set_mode(servopin[pin], pi.OUTPUT)
    if newmode == PWM:
       mode[pin] = newmode
       pi.set_PWM_frequency(servopin[pin],PWM_f)   # A. McDonley
    if newmode == PING:
       mode[pin] = newmode
    return 0
  if pin < 24: # only accept valid modes 
    if newmode == INPUT:
       diomode[pin-8] = newmode
       setDioBit(0,pin-8)
       return 0
    if newmode == OUTPUT:
       diomode[pin-8] = newmode
       clearDioBit(0,pin-8)
       return 0
  return -1
  
#
# Read current value of digital pin (0..23)
#
# 0..7  are Raspberry Pi pins on the Servo header (PWM, SERVO, INPUT, OUTPUT, PING)
# 8..23 are DIO A0-A7 and B0-B7 respectively (INPUT, OUTPUT)
#

def digitalRead(pin):
  if pin < 0:
    return -1
  if pin < 8:
    return pi.read(servopin[pin])
  if pin < 24:
    return getDioBit(DIO_GPIO,pin-8)
  return -1
  
#
# Set the value of digital pins (0..23)
#
# 0..7  are Raspberry Pi pins on the Servo header (PWM, SERVO, INPUT, OUTPUT, PING)
# 8..23 are DIO A0-A7 and B0-B7 respectively (INPUT, OUTPUT)
#

def digitalWrite(pin,val):
  if pin < 0:
    return -1
  if pin < 8:
    return pi.write(servopin[pin],val)
  if pin < 24:
    if val:   
      return setDioBit(DIO_OLAT,pin-8)
    else:
      return clearDioBit(DIO_OLAT,pin-8)
  return -1
  
def digitalWrite(pin,val):
  if pin < 0:
    return -1
  if pin < 8:
    return pi.write(servopin[pin],val)
  if pin < 24:
    if val:   
      return setDioBit(DIO_OLAT,pin-8)
    else:
      return clearDioBit(DIO_OLAT,pin-8)
  return -1
  
#
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
#

def analogRead(adcnum):
  if adcnum < 0:
    return -1   
  if adcnum > 7:
    return -1   
  spi.open(0,1) 
  r = spi.xfer2(req10[adcnum])
  adcout = ((r[1]&3) << 8) + r[2]
  spi.close()               		#A. McDonley
  return adcout
    
#
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
#
# shift left two bits to present 10 bit result as 12 bit result
# for RoboPi compatibility
#

def analogReadRaw(adcnum):
  return analogRead(adcnum)<<2
  
#
# Set motor speed 0..255 for specified pin (mode must be PWM)
#
# default to 490Hz like Arduino
#

def analogWrite(pin,val):
  if pin < 0:
    return -1
  if pin > 7:
    return -1
  pi.set_PWM_dutycycle(servopin[pin],val)
  return 0
  
#
# Get servo position last written to specified pin
#
  
def servoRead(pin):
  if pin < 0:
    return -1
  if pin > 7:
    return -1
  return servoval[pin]

#
# Set servo position for specified pin (mode must be SERVO)
#
  
def servoWrite(pin,val):
  if pin < 0:
    return -1
  if pin > 7:
    return -1
  servoval[pin] = val
  pi.set_servo_pulsewidth(servopin[pin], val)
  return 0
  
#
# readDistance() is not working properly yet - look for it in future releases
#

def readDistance(pin):
  if pin < 0:
    return -1
  if pin > 7:
    return -1
  if mode[pin] == PING:
    pi.set_mode(servopin[pin], pi.OUTPUT)
    pi.gpio_trigger(servopin[pin], 50, 1) # 50us, high pulse
    pi.set_mode(servopin[pin], pi.INPUT)
    ok = pi.wait_for_edge(servopin[pin], pigpio.RISING_EDGE, 0.01)
    if ok:
      t0 = pi.get_current_tick()
      ok = pi.wait_for_edge(servopin[pin], pigpio.FALLING_EDGE, 0.1)
      if ok:
        t1 = pi.get_current_tick()
        return (t1 - t0) # returns microseconds     
  return -1

#
# The following functions are not meant for public use, and may not be supported
# in the future. If you use them, do not be surprised if future versions of the
# library do not make them available.
#
# The following functions are NOT available on RoboPi
#

#
# Read specified MCP23S17 register (16 bits)
#

def readDio(reg):
  spi.open(0,0)                	  # A. McDonley
  r = spi.xfer([0x41,reg,0,0])
  spi.close()                     # A. McDonley
  return ((r[2]<<8)+r[3])
#
# Write to specified MCP23S17 register (16 bits)
#

def writeDio(reg,val):
    spi.open(0,0)             # A. McDonley
    r = spi.xfer([0x40,reg,val>>8,val&255])
    spi.close()		      # A. McDonley
    return r
#
# Set specific bit in specified register
#
    
def setDioBit(reg,bit):
  if bit < 0:
    return -1
  if bit > 15:
    return -1 
  t = readDio(reg)
  t = t | (1<<bit)
  writeDio(reg,t) 
  return 0

#
# Clear specific bit in specified register
#
    
def clearDioBit(reg,bit):
  if bit < 0:
    return -1
  if bit > 15:
    return -1 
  t = readDio(reg)
  t = t & ~(1<<bit)
  writeDio(reg,t)  
  return 0

#
# Flip value of specific bit in specified register
#
    
def flipDioBit(reg,bit):
  if bit < 0:
    return -1
  if bit > 15:
    return -1 
  t = readDio(reg)
  t = t ^ (1<<bit)
  writeDio(reg,t) 
  return 0

#
# Get value of specific bit in specified register
#
    
def getDioBit(reg,bit):
  if bit < 0:
    return -1
  if bit > 15:
    return -1 
  if readDio(reg) & (1<<bit):
    return 1
  return 0  

#
# Print out contents of all the MCP23S17 registers (16 bit)
#
    
def dumpDio():
    print "reg val"
    print "--------"
    for r in range(0,16):
      print "", format(r+r, '02X'), format(readDio(r+r),'04X')



