#!/usr/bin/env python
import os
import pygame, sys
import datetime
import time
from pygame.locals import *
import pygame.camera
import shutil
import numpy
import subprocess, glob
import RPi.GPIO as GPIO
import signal
from decimal import *
getcontext().prec = 8

#ONLY WORKS WITH PYTHON 2.7, start with SUDO IDLE if you wish to use the GPIO.

# if using the RPi camera set use_Pi_Cam = 1 , if set to 0 the program will use a USB camera.
use_Pi_Cam = 1

#==================================================================================================
# DISPLAY SETTINGS

# Display - Set this dependent on your display. 0 = LCD 840x480, 1 = PAL Composite (640x480),
# 2 = other, set by parameters below
# if using 1 for PAL composite then adjust /boot/config.txt to suit
# if using 0 then change /boot/config.txt for hmdi group = 2 and hdmi mode = 14 
Display = 0

# Image_window - sets image window size, either 0 = 320x240, 1 = 352x288,2 = 640x480, 3 = 800x600
# Any for HDMI but recommend 0 for Composite (PAL)
Image_window = 3

# max_res - camera max available resolution, depends on your webcam
# 0 = 320x240, 1 = 352x288, 2 = 640x480, 3 = 800x600, 4 = 960x720, 5 = 1280x960, 6 = 1920x1440, 7 = 2592x1944
# Logitech C270 won't work past max_res = 4, Philip 900 won't work above above max_res = 2, pi camera = 7
max_res = 7

# bits - bits to display in pygame
bits = 16

#switch on GPIO pin sw to GND ? If so set to 1, it will shutdown Pi when pressed
switch = 0
sw = 26 #GPIO pin 26

# saving directory for pictures (temporary files are in /run/shm/)
savdir = "./captured/" 

#==================================================================================================
# SET DEFAULT CONFIG
#==================================================================================================

# Window - Window size in pixels. 
vWindow = 70
hWindow = 40
# minwin - set minimum window size 
minwin = 20
# maxwin - set maximum window size
maxwin = 190
# offset3/4 - offsets from centre of screen
offset3 = 0
offset4 = 0
# Triggers - Photo taken when this number of changed pixels exceeded, in %
Triggers = 50
# Threshold - Threshold, Pixel difference values less than this won't be detected
Threshold = 30
# thres - on = 1,off = 0. Displays detected changed pixels
thres = 0
# Zoom - set to give Zoomed image, higher magnification
Zoom = 0
# Capture - set to 1 to capture images
Capture = 1
# shots on trigger
shots = 2
# movement detection area ,0 = FULL, 1 = using cropped area
det_area = 1
# save 2 preshots, before trigger, 1 = YES 
preshot = 1
# auto exposure correction ,0 = OFF,1 = restart raspistill, 2 = auto correction using Average metering,
# 3 = auto correction using Spot metering (using cropped area)
auto_c = 2
# timelapse, 1 = ON
timelapse = 0
# timelapse period in seconds
timeperiod = 300
# full size timelapse shots, RPi camera only
fullsize = 0


# RPi camera presets
#===================================================================================
rpico = 50     # -co   set brightness
rpibr = 50     # -br   set contrast
rpiexno = 1    # -ex   0=off,1=auto,2=night,3=backlight,4=spotlight.... (see below)
rpiISO = 0     # -ISO  0 = auto or set 100,200,...or 800
rpiev = 0      # -ev   set ev correction, used in auto exposure mode
rpisa =  0     # -sa   set saturation
rpiss = 100000 # -ss   100000 = 100mS, used in exposure off mode
rpist = 1      # -st   1 = -st ON (will override -awb setting), 0 = -st OFF
rpiawbno = 1   # -awb  0=off,1=auto,2=sun,3=cloud,4=shade,5=tungsten,6=flourescent.... (see below)
rpiawbr = 1.0  # -awbg red gain, only used if rpiawbno = 0
rpiawbb = 1.3  # -awbg blue gain, only used if rpiawbno = 0
rpimmno = 3    # -mm   0 = average, 1 = spot, 2 = backlit, 3 = matrix
rpiq = 100     # -q    jpg quality
rpibm = 1      # -bm   burst mode (speeds up picture capture but may upset auto exposure
#===================================================================================

rpiawbs = ['off', 'auto', 'sun', 'cloud', 'shade', 'tungsten', 'fluorescent', 'incandescent', 'flash', 'horizon']
rpimms = ['average', 'spot', 'backlit', 'matrix']
rpimodes = ['off', 'auto', 'night', 'backlight', 'spotlight', 'sports', 'snow', 'verylong', 'fireworks']
rpimodesa = [' off', 'auto', 'night', 'backl', 'spotl', 'sport', 'snow', 'vlong', 'fwork']
rpiawbsa = [' off', 'auto', ' sun', 'cloud', 'shade', 'tungn', 'fcent', 'incan', 'flash', 'horzn']
rpimmsa = ['avrge', 'spot', 'backl', 'matrx']
auto_ca = ['off','RST','AVE','SPOT']
det_areaa =['FULL','SPOT']
rpiwidth = [320,352,640,800,960,1280,1920,2592]
rpiheight = [240,288,480,600,720,960,1440,1944]
rpiscalex = [1,1.1,1.818,1.25,1.2,1.333,1.5,1.35]
rpiscaley = [1,1.2,1.666,1.25,1.2,1.333,1.5,1.35]
rpit = 0       # -t leave as 0

if rpist == 1:
   rpiawbno = 1

vtime = 0
htime = 0
sf = 4
rpiex = rpimodes[rpiexno]
rpimm = rpimms[rpimmno]
rpiawb = rpiawbs[rpiawbno]

if switch == 1:
   GPIO.setwarnings(False)
   GPIO.setmode (GPIO.BOARD)
   GPIO.setup(sw,GPIO.IN,pull_up_down = GPIO.PUD_UP)

pygame.init()
scalex = 1
scaley = 1
z = 0
change = 1
ar5 = []
omg = []
sar6 = 0
sar7 = 0

oldttot = 0
restart = 0
rgb = ['X','R','G','B','W']
fontObj = pygame.font.Font(None,16)
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
greyColor = pygame.Color(128,128,128)
dgryColor = pygame.Color(64,64,64)
lgryColor = pygame.Color(192,192,192)
blackColor = pygame.Color(0,0,0)
whiteColor = pygame.Color(255,255,255)
purpleColor = pygame.Color(255,0,255)
yellowColor = pygame.Color(255,255,0)

if Image_window > Zoom:
   Zoom = Image_window


if Display == 0:
   width = 640
   b1x = width
   b1y = -32
   b2x = width
   b2y = 128
   b3x = width
   b3y = 288
   Image_window = 2
   height = 480
   hplus = 0
   Zoom = 2
   
if Display == 1:
   width = 352
   height = 288
   b1x = width
   b1y = -32
   b2x = width
   b2y = 128
   b3x = width
   b3y = 288
   Image_window = 1
   modewidth = 640
   Zoom = 1
   hplus = 192
   
if Display > 1:
   width = rpiwidth[Image_window]
   height = rpiheight[Image_window]
   b1x = width
   b1y = -32
   b2x = width
   b2y = 128
   b3x = width
   b3y = 288
   hplus = 0

min_res = Image_window

while z <= Zoom:
   scalex = scalex * rpiscalex[z]
   scaley = scaley * rpiscaley[z]
   z +=1

offset5 = 0
offset6 = 0
w = rpiwidth[Zoom]
h = rpiheight[Zoom]
if width <= 352:
   modewidth = 640
else:
   modewidth = width + 128      
windowSurfaceObj = pygame.display.set_mode((modewidth,height + hplus),1,bits)
pygame.display.set_caption('Movement')

   
if use_Pi_Cam == 0:
   pygame.camera.init()
   if Zoom == 0:
      cam = pygame.camera.Camera("/dev/video0",(320,240))
   if Zoom == 1 and max_res >= 1:
      cam = pygame.camera.Camera("/dev/video0",(352,288))
   if Zoom == 2 and max_res >= 2:
      cam = pygame.camera.Camera("/dev/video0",(640,480))
   if Zoom == 3 and max_res >= 3:
      cam = pygame.camera.Camera("/dev/video0",(800,600))
   if Zoom == 4 and max_res >= 4:
      cam = pygame.camera.Camera("/dev/video0",(960,720))
   if Zoom == 5 and max_res >= 5:
      cam = pygame.camera.Camera("/dev/video0",(1280,960))
   if Zoom == 6 and max_res >= 6:
      cam = pygame.camera.Camera("/dev/video0",(1920,1440))
   if Zoom == 7 and max_res >= 7:
      cam = pygame.camera.Camera("/dev/video0",(2592,1944))
   cam.start()
   cam.set_controls(0,0,rpibr)

if use_Pi_Cam == 1:
   if os.path.exists('/run/shm/test.jpg') == True:
      os.rename('/run/shm/test.jpg','/run/shm/oldtest.jpg')

   rpistr = "raspistill -o /run/shm/test.jpg -co " + str(rpico) + " -br " + str(rpibr)
   if rpiex != 'off':
      rpistr = rpistr + " -t " + str(rpit) + " -tl 0 -st -ex " + rpiex
   else:
      rpistr = rpistr + " -t " + str(rpit) + " -tl 0 -st -ss " + str(rpiss)
   if rpibm == 1:
      rpistr = rpistr + " -bm "
   if rpiISO > 0:
      rpistr = rpistr + " -ISO " + str(rpiISO)
   if rpiev != 0:
      rpistr = rpistr + " -ev " + str(rpiev)
   if rpist == 1:
      rpistr = rpistr + " -st "
   else:
      rpistr = rpistr + " -awb " + rpiawb
      if rpiawb == 'off':
         rpistr = rpistr + " -awbg " + str(rpiawbr) + "," + str(rpiawbb)
     
    
   off5 = (Decimal(0.5) - (Decimal(width)/Decimal(2))/Decimal(w)) + (Decimal(offset5)/Decimal(w))
   off6 = (Decimal(0.5) - (Decimal(height)/Decimal(2))/Decimal(h)) + (Decimal(offset6)/Decimal(h))
   widx = Decimal(width)/Decimal(w)
   heiy = Decimal(height)/Decimal(h)
   rpistr = rpistr + " -mm " + rpimm + " -q " + str(rpiq) + " -n -sa " + str(rpisa) + " -w " + str(width) + " -h " + str(height) + " -roi " +  str(off5) + "," + str(off6) + ","+str(widx) + "," + str(heiy)
   #print rpistr
   p=subprocess.Popen(rpistr,shell=True, preexec_fn=os.setsid)

def button2 (bx1,by1,bx2,by2,height,bColor):
   greyColor = pygame.Color(128,128,128)
   dgryColor = pygame.Color(64,64,64)
   blackColor = pygame.Color(0,0,0)
   whiteColor = pygame.Color(255,255,255)
   redColor = pygame.Color(255,0,0)
   colors = [greyColor,dgryColor,redColor]
   Color = colors[bColor]
   pygame.draw.rect(windowSurfaceObj,Color,Rect(bx1,height+by1,bx2,by2))
   pygame.draw.line(windowSurfaceObj,whiteColor,(bx1,height+by1),(bx1+bx2-1,height+by1))
   pygame.draw.line(windowSurfaceObj,whiteColor,(bx1+1,height+by1+1),(bx1+bx2-2,height+by1+1))
   return()

button2 (b3x+1,b3y+97,63,31,0,0)
if use_Pi_Cam  == 1:
   
   button2 (b3x+1,b3y+33,63,31,0,0)
   button2 (b3x+1,b3y+65,63,31,0,0)
   button2 (b1x+65,b1y+97,63,31,0,0)
   button2 (b1x+65,b1y+129,63,31,0,0)
   button2 (b1x+65,b1y+161,63,31,0,0)
   button2 (b2x+65,b2y+33,63,31,0,0)
button2 (b2x+65,b2y+65,63,31,0,0)
button2 (b3x+1,b3y+129,31,31,0,0)
button2 (b3x+33,b3y+129,31,31,0,0)

cy = 33
while cy <= 161:
   button2 (b1x+1,b1y+cy,63,31,0,0)
   cy +=32
button2 (b1x+65,b1y+33,63,31,0,0)
button2 (b1x+65,b1y+65,63,31,0,0)
button2 (b2x+1,b2y+33,63,31,0,0)
if use_Pi_Cam == 1:
   cy = 65
   while cy <= 161:
      button2 (b2x+1,b2y+cy,63,31,0,0)
      cy +=32


def keys2(msg,fsize,fcolor,fx,fy,upd):
   greenColor = pygame.Color(0,255,0)
   greyColor = pygame.Color(128,128,128)
   dgryColor = pygame.Color(64,64,64)
   yellowColor = pygame.Color(255,255,0)
   redColor = pygame.Color(255,0,0)
   blueColor = pygame.Color(0,0,255)
   whiteColor = pygame.Color(255,255,255)
   blackColor = pygame.Color(0,0,0)
   purpleColor = pygame.Color(255,0,255)
   colors = [dgryColor,greenColor,yellowColor,redColor,greenColor,blueColor,whiteColor,greyColor,blackColor,purpleColor]
   color = colors[fcolor]
   fontObj = pygame.font.Font('freesansbold.ttf',fsize)
   msgSurfaceObj = fontObj.render(msg, False,color)
   msgRectobj = msgSurfaceObj.get_rect()
   msgRectobj.topleft =(fx,fy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
   windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
   if upd ==1:
      pygame.display.update(pygame.Rect(fx,fy,64,32))
   return()

Trigger =  str(Triggers)+" %"
keys2 (str(Threshold),14,3,(b1x+31)-(len(str(Threshold))*4),b1y+111,0)
keys2 (str(Trigger),14,3,(b1x+31)-(len(str(Trigger))*4),b1y+143,0)
keys2 (str(Zoom),14,3,b1x+27,b1y+175,0)
keys2 (str(rpibr),14,3,b2x+24,b2y + 47,0)
keys2 (str(shots),14,3,(b3x+31)-(len(str(shots))*4),b3y+111,0)
if use_Pi_Cam == 1:
   keys2 (str(rpico),14,3,b2x+24,b2y + 79,0)
   if rpiex == 'off':
      keys2 (str(int(rpiss/1000)),13,3,(b2x+33)-(len(str(rpiss/1000))*4),b2y + 112,0)
   else:
      keys2 (str(int(rpiev)),13,3,(b2x+33)-(len(str(rpiev))*4),b2y + 112,0)
   keys2 ((rpimodesa[rpiexno]),14,3,b2x+17,b2y + 143,0)
   if rpist == 0:
      keys2 ((rpiawbsa[rpiawbno]),14,3,b3x+15,b3y + 48,0)
   else:
      keys2 ((rpiawbsa[rpiawbno]),14,0,b3x+15,b3y + 48,0)
   keys2 ((rpimmsa[rpimmno]),14,3,b3x+14,b3y + 80,0)
   keys2 (str(rpiISO),14,3,b2x+19,b2y + 175,0)
   if rpiISO == 0:
      pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+19,b2y + 175, 26, 16))
      keys2 ('auto',14,3,b2x+17,b2y + 175,0)
   keys2 ("Contrast",12,6,b2x+5,b2y + 66,0)
   keys2 ("-       +",18,6,b2x+8,b2y + 74,0)
   if rpiex == 'off':
      keys2 ("Exp Time",12,6,b2x+4,b2y + 100,0)
   else:
      keys2 ("       eV",12,6,b2x+4,b2y + 100,0)
   keys2 ("-       +",18,6,b2x+8,b2y + 106,0)
   keys2 ("ISO",12,6,b2x+20,b2y + 163,0)
   keys2 ("-       +",18,6,b2x+8,b2y + 170,0)
   keys2 ("Exp Mode",12,6,b2x+3,b2y + 129,0)
   keys2 ("<           >",16,6,b2x+3,b2y + 138,0)
   keys2 ("  Non",14,rpist,b1x+73,b1y+163,0)
   keys2 ("Pi Lens",14,rpist,b1x+72,b1y+175,0)
   keys2 ("Burst",14,rpibm,b2x+78,b2y+34,0)
   keys2 (" Mode",14,rpibm,b2x+74,b2y+47,0)
   keys2 ("   awb",14,6,b3x+6,b3y+34,0)
   keys2 ("<           >",16,6,b3x+3,b3y + 44,0)
   keys2 ("Metering",14,6,b3x+4,b3y+66,0)
   keys2 ("<           >",16,6,b3x+3,b3y + 76,0)
keys2 ("Det Area",12,6,b2x+70,b2y+67,0)
keys2 ("<           >",16,6,b2x+66,b2y + 77,0)
if det_area == 0:
   keys2 (det_areaa[det_area],12,3,b2x+80,b2y+81,0)
else:
   keys2 (det_areaa[det_area],12,1,b2x+80,b2y+81,1)
keys2 ("Dis",14,thres,b3x+36,b3y+130,0)
keys2 ("play",14,thres,b3x+35,b3y+142,0)
keys2 (" Shots ",14,6,b3x+10,b3y+98,0)
keys2 ("-       +",18,6,b3x+8,b3y+110,0)
   
keys2 (str(hWindow),14,3,(b1x+31)-(len(str(hWindow))*4),b1y+79,0)
keys2 (str(vWindow),14,3,(b1x+31)-(len(str(vWindow))*4),b1y+47,0)
keys2 ("Cap",14,Capture,b3x+3,b3y+130,0)
keys2 ("ture",14,Capture,b3x+4,b3y+143,0)
keys2 ("V-Win",14,6,b1x+12,b1y+33,0)
keys2 ("-       +",18,6,b1x+10,b1y+42,0)
keys2 ("H-Win",14,6,b1x+12,b1y+65,0)
keys2 ("-       +",18,6,b1x+10,b1y+74,0)
keys2 ("Threshold",12,6,b1x+1,b1y+98,0)
keys2 ("-       +",18,6,b1x+8,b1y+106,0)
keys2 ("Trigger",13,6,b1x+6,b1y+130,0)
keys2 ("-       +",18,6,b1x+8,b1y+138,0)
keys2 ("Zoom",14,6,b1x+14,b1y+162,0)
keys2 ("-       +",18,6,b1x+8,b1y+170,0)
keys2 ("Brightness",12,6,b2x+1,b2y+34,0)
keys2 ("-       +",18,6,b2x+8,b2y+ 42,0)
keys2 ("  Time",14,timelapse,b1x+70,b1y+35,0)
keys2 ("  lapse",14,timelapse,b1x+70,b1y+47,0)
keys2 (" Period",14,6,b1x+70,b1y+67,0)
keys2 (" -       +",18,6,b1x+68,b1y+78,0)
if use_Pi_Cam == 1:
   keys2 ("   Full",14,fullsize,b1x+70,b1y+99,0)
   keys2 ("   Res",14,fullsize,b1x+70,b1y+111,0)
   keys2 (" Auto Exp",12,6,b1x+68,b1y+131,0)
   keys2 ("<        >",18,6,b1x+68,b1y+142,0)
   if auto_c < 3:
      keys2 (auto_ca[auto_c],12,3,(b1x+96)-(len(auto_ca[auto_c])*4),b1y+146,0)
   else:
      keys2 (auto_ca[auto_c],12,2,(b1x+96)-(len(auto_ca[auto_c])*4),b1y+146,0)

keys2 (str(timeperiod),14,3,(b1x+95)-(len(str(timeperiod))*4),b1y+80,0)
pygame.display.update() 

oldvWindow  = vWindow
oldhWindow = hWindow
oldTriggers = Triggers
oldThreshold = Threshold
oldthres = thres
oldZoom = Zoom
oldrpibr = rpibr
oldrpico = rpico
oldrpiss = rpiss
oldrpiexno = rpiexno
oldrpiISO = rpiISO
oldrpiev = rpiev
oldCapture = Capture
oldshots = shots
oldrpiawbno = rpiawbno
oldrpimmno = rpimmno
oldtimelapse = timelapse
oldtimeperiod = timeperiod
oldfullsize = fullsize
oldauto_c = auto_c
oldrpist = rpist
oldrpibm = rpibm
olddet_area = det_area

pct = 1
pcu = 1
xycle = 0
count = 1
filno = 0
time_start = time.time()
trigmask = 0

greenColor = pygame.Color(0,255,0)
greyColor = pygame.Color(128,128,128)
dgryColor = pygame.Color(64,64,64)
yellowColor = pygame.Color(255,255,0)
redColor = pygame.Color(255,0,0)
blueColor = pygame.Color(0,0,255)
whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)
purpleColor = pygame.Color(255,0,255)

while True:
 
   sar5 = 0

# take picture

   if use_Pi_Cam == 0:
      image = cam.get_image()
      if Zoom == 0:
         offset5 = offset3
         offset6 = offset4
         if offset5 > 0 and offset5 >= (w/2)-(width/2):
            offset5 = (w/2)-(width/2)
         if offset5 < 0 and offset5 <= 0-((w/2)-(width/2)):
            offset5 = 0-((w/2)-(width/2))
         if offset6 > 0 and offset6 >= (h/2)-(height/2):
            offset6 = (h/2)-(height/2)
         if offset6 < 0 and offset6 <= 0-((h/2)-(height/2)):
            offset6 = 0-((h/2)-(height/2))
      if Zoom > 0 and Zoom != Image_window:
         strim1 = pygame.image.tostring(image,"RGB",1)
         x = ((h/2)-(height/2)) - offset6
         strt = w * 3 * x
         strim = ""
         c = 0
         stas = (((w/2) - (width/2)) + offset5) * 3
         while c < height:
            ima = strim1[strt:strt+(w*3)]
            imd = ima[stas : stas + (width*3)]
            strim = strim + imd
            strt +=(w*3)
            c +=1
         image = pygame.image.fromstring(strim,(width,height),"RGB",1)
      if preshot == 1:
         pygame.image.save(image,'/run/shm/test.jpg')

      
      catSurfaceObj = image
      windowSurfaceObj.blit(catSurfaceObj,(0,0))
      strim = pygame.image.tostring(image,"RGB",1)
          
   if use_Pi_Cam == 1:

      while os.path.exists('/run/shm/test.jpg') == False:
          time.sleep(.005)
      imagefile = ('/run/shm/test.jpg')

      try:
         image = pygame.image.load(imagefile)
      except pygame.error:
         imagefile = ('/run/shm/oldtest.jpg')
         image = pygame.image.load(imagefile)

      catSurfaceObj = image
      windowSurfaceObj.blit(catSurfaceObj,(0,0))
      strim = pygame.image.tostring(image,"RGB",1)


   # define time format and colors
   now = datetime.datetime.now()
   msg = now.strftime("%Y %m %d %H:%M:%S")
   fsize = 16 #font size
   textcolor = 5 # 0 to 9
   backcolor = 0 # 0 to 9, -1 for no background
   fx = 0  # x position of text
   fy = 460 # y postion of text

# put text on image and save
   colors = [dgryColor,yellowColor,redColor,greenColor,blueColor,whiteColor,greyColor,blackColor,purpleColor,lgryColor]
   tcolor = colors[textcolor]
   lt = (len(msg) * (fsize/2)) #+ fsize
   if backcolor > -1:
      bcolor = colors[backcolor]
      pygame.draw.rect(windowSurfaceObj,bcolor,Rect(fx,fy, lt, fsize))
   fontObj = pygame.font.Font('freesansbold.ttf',fsize)
   msgSurfaceObj = fontObj.render(msg, False,tcolor)
   msgRectobj = msgSurfaceObj.get_rect()
   msgRectobj.topleft =(fx,fy)
   windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
   pygame.display.update(pygame.Rect(fx,fy,lt,fsize))

# Crop picture
   if auto_c == 3 or det_area == 1:
      cropped = pygame.Surface((hWindow,vWindow))
      cropped.blit(image,(0,0),((((width/2) - (hWindow/2))+offset3),(((height/2)-(vWindow/2)) + offset4),hWindow,vWindow))
      imb = pygame.image.tostring(cropped,"RGB",1)

   if auto_c < 3 or det_area == 0:
      imagem = pygame.transform.scale(image,[width/sf,height/sf])
      imc = pygame.image.tostring(imagem,"RGB",1)
      

   
# initialise arrays
   mx = []
   my = []
   if filno == 1 or (len(mx) != len(omg)):
      if det_area == 1:
         ar5 = [0] * vWindow*hWindow*3
      else:
         ar5 = [0] * (width/sf) * (height/sf) * 3
   if auto_c == 3 or det_area == 1:
      mx = [ord(i) for i in imb]
   if auto_c < 3 or det_area == 0:
      my = [ord(i) for i in imc]
      
   if len(mx) == len(omg) and det_area == 1:
      ar5 = (abs(abs(numpy.array(mx)) - abs(numpy.array(omg))) - Threshold)
      ar5 = numpy.clip(ar5,0,1)
      sar5 = sum(ar5)

   if len(my) == len(omg) and det_area == 0:
      ar5 = (abs(abs(numpy.array(my)) - abs(numpy.array(omg))) - Threshold)
      ar5 = numpy.clip(ar5,0,1)
      sar5 = sum(ar5)

   if det_area == 1:   
      omg = mx[:]
   else:
      omg = my[:]
         
 
   pic =""   
   counter = 0
   if thres == 1:
      if det_area == 1:
         while counter < hWindow*vWindow*3 :
            if ar5[counter] == 0:
               pic = pic + imb[counter:counter+3]
            else:
               pic = pic + chr(255)+chr(0)+chr(0)
            counter +=3
      if det_area == 0:
         while counter < (h/sf)*(w/sf)*3 :
            if ar5[counter] == 0:
               pic = pic + imc[counter:counter+3]
            else:
               pic = pic + chr(255)+chr(0)+chr(0)
            counter +=3

   try:
      lapsed = 0
      time_now = time.time()
      if time_now < time_start:
         time_start = time.time()
         time_now = time.time()
      time_diff = time_now - time_start
      if timelapse == 1 and (time_diff > timeperiod):
         lapsed = 1
      trig =(hWindow*vWindow*3)/(100/Triggers)
      trig2 = int(Decimal(Decimal(sar5)/(vWindow*hWindow*3))*100)
      if trig2 > 0 and Capture == 1:
         trigmask = 10
      trigmask -=1
      
      if (sar5 > trig and trig2 < 95 and Capture == 1 and ((len(mx) == len(omg) and det_area==1) or (len(my) == len(omg) and det_area==0)) or (lapsed == 1 and timelapse == 1 and ((len(mx) == len(omg) and det_area==1) or (len(my) == len(omg) and det_area==0)))):
         time_start = time.time()
         if lapsed == 0:
            keys2 (str(Trigger),14,1,(b1x+31)-(len(str(Trigger))*4),b1y+143,1)
         else:
            keys2 (str(timeperiod),14,1,(b1x+95)-(len(str(timeperiod))*4),b1y+80,1)
         keys2 (str(filno),14,0,(b1x+31)-(len(str(filno))*4),b3y+165,0)
         filno = filno + 1
         keys2 (str(filno),14,1,(b1x+31)-(len(str(filno))*4),b3y+165,0)
         now = datetime.datetime.now()
         timestamp = now.strftime("%y%m%d%H%M%S")
         fname = savdir + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
         if use_Pi_Cam == 1:
            if preshot == 1 and lapsed == 0:            
               if os.path.exists('/run/shm/oldtest2.jpg') == True: 
                  fname = savdir + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
                  shutil.copy('/run/shm/oldtest2.jpg',fname)
                  os.remove('/run/shm/oldtest2.jpg')
               if os.path.exists('/run/shm/oldtest.jpg') == True:
                  filno = filno + 1
                  fname = savdir + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
                  shutil.copy('/run/shm/oldtest.jpg',fname)
               filno = filno + 1
               fname = savdir + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
               
            if lapsed == 0 or (lapsed == 1 and fullsize == 0):
               shutil.copy('/run/shm/test.jpg',fname)
               os.rename('/run/shm/test.jpg','/run/shm/oldtest.jpg')

            if lapsed == 1 and fullsize == 1:
               os.killpg(p.pid, signal.SIGTERM)
               rpistr = "raspistill -o " + fname + " -co " + str(rpico) + " -br " + str(rpibr)
               if rpiex != 'off':
                  rpistr = rpistr + " -t 800 -st -ex " + rpiex
               else:
                  rpistr = rpistr + " -t 10 -st -ss " + str(rpiss)
               if rpiISO > 0:
                  rpistr = rpistr + " -ISO " + str(rpiISO)
               if rpiev != 0:
                  rpistr = rpistr + " -ev " + str(rpiev)
               if rpist == 1:
                  rpistr = rpistr + " -st "
               else:
                  rpistr = rpistr + " -awb " + rpiawb
               if rpiawb == 'off':
                  rpistr = rpistr + " -awbg " + str(rpiawbr) + "," + str(rpiawbb)
               rpistr = rpistr + " -n -sa " + str(rpisa) +  " -mm " + rpimm + " -q  " + str(rpiq)
               path = rpistr + ' -w 2592 -h 1944'
               #print path
               os.system (path)
               restart = 1    
            
         else:
            pygame.image.save(image,fname)
            if preshot == 1 and lapsed == 0:            
               if os.path.exists('/run/shm/oldtest2.jpg') == True: 
                  fname = savdir + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
                  shutil.copy('/run/shm/oldtest2.jpg',fname)
                  os.remove('/run/shm/oldtest2.jpg')
               if os.path.exists('/run/shm/oldtest.jpg') == True:
                  filno = filno + 1
                  fname = savdir + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
                  shutil.copy('/run/shm/oldtest.jpg',fname)
               filno = filno + 1
               fname = savdir + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
               shutil.copy('/run/shm/test.jpg',fname)
               os.rename('/run/shm/test.jpg','/run/shm/oldtest.jpg')
               
         time.sleep(0.1)
         if lapsed == 0:
            keys2 (str(Trigger),14,3,(b1x+31)-(len(str(Trigger))*4),b1y+143,1)
         else:
            keys2 (str(timeperiod),14,3,(b1x+95)-(len(str(timeperiod))*4),b1y+80,1)

         shot = 1
 
         while shot < shots  and lapsed == 0:
            filno = filno + 1
            if use_Pi_Cam == 1:
               while os.path.exists('/run/shm/test.jpg') == False:
                  time.sleep(.001)
               imagefile = ('/run/shm/test.jpg')

               try:
                  image = pygame.image.load(imagefile)
               except pygame.error:
                  imagefile = ('/run/shm/oldtest.jpg')
                  image = pygame.image.load(imagefile)
            else:
               image = cam.get_image()
               if Zoom == 0:
                  offset5 = offset3
                  offset6 = offset4
                  if offset5 > 0 and offset5 >= (w/2)-(width/2):
                     offset5 = (w/2)-(width/2)
                  if offset5 < 0 and offset5 <= 0-((w/2)-(width/2)):
                     offset5 = 0-((w/2)-(width/2))
                  if offset6 > 0 and offset6 >= (h/2)-(height/2):
                     offset6 = (h/2)-(height/2)
                  if offset6 < 0 and offset6 <= 0-((h/2)-(height/2)):
                     offset6 = 0-((h/2)-(height/2))
               if Zoom > 0 and Zoom != Image_window:
                  strim1 = pygame.image.tostring(image,"RGB",1)
                  x = ((h/2)-(height/2)) - offset6
                  strt = w * 3 * x
                  strim = ""
                  c = 0
                  stas = (((w/2) - (width/2)) + offset5) * 3
                  while c < height:
                     ima = strim1[strt:strt+(w*3)]
                     imd = ima[stas : stas + (width*3)]
                     strim = strim + imd
                     strt +=(w*3)
                     c +=1
                  image = pygame.image.fromstring(strim,(width,height),"RGB",1)
               if preshot == 1:
                  pygame.image.save(image,'/run/shm/test.jpg')
            now = datetime.datetime.now()
            timestamp = now.strftime("%y%m%d%H%M%S")
            fname = savdir  + "pic_" + str(timestamp)+ "_" + str(filno) + '.jpg'
            if use_Pi_Cam == 1:
               shutil.copy('/run/shm/test.jpg',fname)
            else:
               pygame.image.save(image,fname)
            if use_Pi_Cam == 1 or preshot == 1:
               os.rename('/run/shm/test.jpg','/run/shm/oldtest.jpg')
            shot +=1
            
         pygame.draw.rect(windowSurfaceObj,blackColor,Rect(b3x+6,b3y + 162, 50, 25))
         keys2 (str(filno),14,1,(b3x+31)-(len(str(filno))*4),b3y+165,1)

      if preshot == 1:
         if os.path.exists('/run/shm/oldtest.jpg') == True:
            os.rename('/run/shm/oldtest.jpg','/run/shm/oldtest2.jpg')
      if use_Pi_Cam == 1 or preshot == 1:
         os.rename('/run/shm/test.jpg','/run/shm/oldtest.jpg')

   except OSError:
      pass
# auto correction
   tol = 32
   ave = 128
   if ((det_area==1 and len(mx) == len(omg)) or (det_area==0 and (len(my) == len(omg)))) and auto_c > 0 and trig2 < 1 and trigmask < 1 and use_Pi_Cam == 1:
      if xycle == 0:
         sar6 = numpy.average(my)
         xycle = 1
      else:
         if auto_c < 3:
            sar7 = numpy.average(my)
            smax = numpy.amax(my)
            smin = numpy.amin(my)
         else:
            sar7 = numpy.average(mx)
            smax = numpy.amax(mx)
            smin = numpy.amin(mx)
         if ((sar7 > ave + tol) and rpiexno == 1 and auto_c  > 1) or ((sar7 > sar6 + tol) and rpiexno == 1 and auto_c == 1):
            if rpiev > -9 and auto_c > 1:
               rpiev = rpiev - 1
            restart = 2
            change = 1
         if ((sar7 < ave - tol) and rpiexno == 1 and auto_c > 1) or ((sar7 < sar6 - tol) and rpiexno == 1 and auto_c == 1):
            if rpiev < 9 and auto_c > 1:
               rpiev = rpiev + 1
            if rpiev == 9:
               rpiev = 0
               rpiexno = 0
               rpiex = rpimodes[rpiexno]
               rpiISO = 400
               pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+2,b2y + 99, 60, 15))
               if rpiex == 'off':
                  keys2 ("Exp Time",12,6,b2x+4,b2y + 100,0)
               else:
                  keys2 ("       eV",12,6,b2x+4,b2y + 100,0)
            restart = 2
            change = 1
         if ((sar7 > ave + tol) and rpiexno == 0 and auto_c > 1) or ((sar7 > sar6 + tol) and rpiexno == 0 and auto_c == 1):
            if rpiss > 5000 and auto_c > 1:
               rpiss = rpiss - int((sar7-128))*1000
               if rpiss <= 1000:
                  rpiss = 1000
               if rpiss < 80000:
                  rpiISO = rpiISO - 100
                  if rpiISO < 300:
                     rpiISO = 0
                     rpiev = 0
                     rpiexno = 1
                     rpiex = rpimodes[rpiexno]
                     pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+2,b2y + 99, 60, 15))
                     if rpiex == 'off':
                        keys2 ("Exp Time",12,6,b2x+4,b2y + 100,0)
                     else:
                        keys2 ("       eV",12,6,b2x+4,b2y + 100,0)
                     
            restart = 2
            change = 1
         if ((sar7 < ave - tol) and rpiexno == 0 and auto_c > 1) or ((sar7 < sar6 - tol) and rpiexno == 0 and auto_c == 1):
            if rpiss < 6000000 and auto_c > 1:
               rpiss = rpiss + int((128-sar7))*1000
               if rpiss > 100000 and rpiISO < 800:
                  rpiISO = rpiISO +100
                  
            restart = 2
            change = 1
         if smax - smin > 245 and restart != 2 and auto_c > 1:
            if rpico > -90:
               rpico = rpico - 10
               restart = 2
               change = 1
         if smax - smin < 180 and restart != 2 and auto_c > 1:
            if rpico < 90:
               rpico = rpico + 10
               restart = 2
               change = 1
            
         if rpiISO == 800 and rpiss > 1000000 and auto_c > 1:
            rpibr = 60 + (rpiss-1000000)/100000
               
   if thres == 1 and det_area == 1:
      #keys2 (str(trig2)+"%",16,3,width + 65,height + 5,1)
      imagep = pygame.image.fromstring(pic,(hWindow,vWindow),"RGB",1)
      catSurfaceObj = imagep
      windowSurfaceObj.blit(catSurfaceObj,((width/2)-(hWindow /2)+offset3,(height/2)-(vWindow /2)+offset4))
   if thres == 1 and det_area == 0:
      #keys2 (str(trig2)+"%",16,3,width + 65,height + 5,1)
      imagep = pygame.image.fromstring(pic,((w/sf),(h/sf)),"RGB",1)
      imagem = pygame.transform.scale(imagep,[width,height])
      catSurfaceObj = imagem
      windowSurfaceObj.blit(catSurfaceObj,(0,0))
   
# shutdown button pressed (if enabled)
   if switch == 1 and GPIO.input(sw) == 0:
      os.killpg(p.pid, signal.SIGTERM)
      path = 'sudo shutdown -h now '
      os.system (path)
       
# Display
   
   if change == 1:

      if oldCapture != Capture:
         keys2 ("Cap",14,Capture,b3x+3,b3y+130,0)
         keys2 ("ture",14,Capture,b3x+4,b3y+143,0)
      if oldrpibm != rpibm:
         keys2 ("Burst",14,rpibm,b2x+78,b2y+34,0)
         keys2 (" Mode",14,rpibm,b2x+74,b2y+47,0)
      if oldrpist != rpist:
         keys2 ("  Non",14,rpist,b1x+73,b1y+163,0)
         keys2 ("Pi Lens",14,rpist,b1x+72,b1y+175,0)
         if rpist == 0:
            keys2 ((rpiawbsa[rpiawbno]),14,3,b3x+15,b3y + 48,0)
         else:
            rpiawbno = 1
            keys2 ((rpiawbsa[rpiawbno]),14,0,b3x+15,b3y + 48,0)
      if oldfullsize != fullsize:
         keys2 ("   Full",14,fullsize,b1x+70,b1y+99,0)
         keys2 ("   Res",14,fullsize,b1x+70,b1y+111,0)
      if oldtimelapse != timelapse:
         keys2 ("  Time",14,timelapse,b1x+70,b1y+35,0)
         keys2 ("  lapse",14,timelapse,b1x+70,b1y+47,0)
      if oldthres != thres :
         keys2 ("Dis",14,thres,b3x+36,b3y+130,0)
         keys2 ("play",14,thres,b3x+35,b3y+142,0)
      if oldThreshold != Threshold:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b1x+20,b1y+111, 26, 16))
         keys2 (str(Threshold),14,3,(b1x+31)-(len(str(Threshold))*4),b1y+111,0)
      if oldtimeperiod != timeperiod:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b1x+80,b1y+80, 33, 16))
         keys2 (str(timeperiod),14,3,(b1x+95)-(len(str(timeperiod))*4),b1y+80,0)
      if oldauto_c != auto_c:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b1x+80,b1y+142, 33, 16))
         if auto_c < 3:
            keys2 (auto_ca[auto_c],12,3,(b1x+96)-(len(auto_ca[auto_c])*4),b1y+146,1)
         else:
            keys2 (auto_ca[auto_c],12,2,(b1x+96)-(len(auto_ca[auto_c])*4),b1y+146,0)
      if olddet_area != det_area:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+78,b2y+78, 33, 16))
         if det_area == 0:
            keys2 (det_areaa[det_area],12,3,b2x+80,b2y+81,1)
         else:
            keys2 (det_areaa[det_area],12,1,b2x+80,b2y+81,1)
      if oldTriggers != Triggers:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b1x+15,b1y+143, 33, 16))
         Trigger =  str(Triggers)+" %"
         keys2 (str(Trigger),14,3,(b1x+31)-(len(str(Trigger))*4),b1y+143,0)
      if oldZoom != Zoom:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b1x+20,b1y+175, 26, 16))
         keys2 (str(Zoom),14,3,b1x+27,b1y+175,0)
      if oldhWindow  != hWindow :
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b1x+18,b1y+79, 26, 16))
         keys2 (str(hWindow),14,3,(b1x+31)-(len(str(hWindow))*4),b1y+79,0)
      if oldvWindow  != vWindow :
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b1x+18,b1y+47, 26, 16))
         keys2 (str(vWindow),14,3,(b1x+31)-(len(str(vWindow))*4),b1y+47,0)
      if oldrpibr != rpibr :
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+22,b2y + 47, 26, 16))
         keys2 (str(rpibr),14,3,(b2x+32)-(len(str(rpibr))*4),b2y+47,0)
      if oldrpico != rpico:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+19,b2y + 79, 26, 16))
         keys2 (str(rpico),14,3,(b2x+32)-(len(str(rpico))*4),b2y+79,0)
      if oldrpiss != rpiss:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+17,b2y + 111, 26, 16))
         keys2 (str(int(rpiss/1000)),13,3,(b2x+33)-(len(str(rpiss/1000))*4),b2y + 112,0)
      if oldrpiexno != rpiexno:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+14,b2y + 143, 38, 16))
         keys2 (rpimodesa[rpiexno],14,3,b2x+14,b2y + 143,0)
         if rpimodes[rpiexno] != "off":
            pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+17,b2y+ 114, 26, 14))
            keys2 (str(int(rpiev)),13,3,(b2x+33)-(len(str(rpiev))*4),b2y + 112,0)
         else:
            pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+17,b2y + 114, 26, 14))
            keys2 (str(int(rpiss/1000)),13,3,(b2x+33)-(len(str(rpiss/1000))*4),b2y + 112,0)
      if oldrpiISO != rpiISO:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+17,b2y + 175, 31, 16))
         keys2 (str(rpiISO),14,3,b2x+19,b2y + 175,0)
         if rpiISO == 0:
            pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+17,b2y + 175, 31, 16))
            keys2 ('auto',14,3,b2x+17,b2y + 175,0)
      if oldrpiev != rpiev:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+17,b2y + 113, 32, 14))
         keys2 (str(int(rpiev)),13,3,(b2x+33)-(len(str(rpiev))*4),b2y + 112,0)
      if oldshots != shots:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b3x+18,b3y+111, 32, 16))
         keys2 (str(shots),14,3,(b3x+31)-(len(str(shots))*4),b3y+111,0)
      if oldrpiawbno != rpiawbno:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b3x+15,b3y + 48, 41, 16))
         if rpist == 0:
            keys2 (rpiawbsa[rpiawbno],14,3,b3x+15,b3y + 48,0)
         else:
            keys2 (rpiawbsa[rpiawbno],14,0,b3x+15,b3y + 48,0)
      if oldrpimmno != rpimmno:
         pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b3x+14,b3y + 79, 38, 16))
         keys2 (rpimmsa[rpimmno],14,3,b3x+14,b3y + 79,0)
  
      pygame.display.update(width,0,width+64,height + hplus)

   if auto_c > 2 or det_area > 0:   
      w2 = width/2 + offset3
      h2 = height/2 + offset4
      c1 = hWindow /2
      c2 = vWindow /2
      c3 = c1 +1 
      c4 = c2 +1 
      if det_area == 1:
         pygame.draw.line(windowSurfaceObj, greenColor, (w2-c1,h2-c2),(w2+c1,h2-c2))
         pygame.draw.line(windowSurfaceObj, greenColor, (w2+c1,h2-c2),(w2+c1,h2+c2))
         pygame.draw.line(windowSurfaceObj, greenColor, (w2+c1,h2+c2),(w2-c1,h2+c2))
         pygame.draw.line(windowSurfaceObj, greenColor, (w2-c1,h2+c2),(w2-c1,h2-c2))
      if auto_c == 3:
         pygame.draw.line(windowSurfaceObj, yellowColor, (w2-c3,h2-c4),(w2+c3,h2-c4))
         pygame.draw.line(windowSurfaceObj, yellowColor, (w2+c3,h2-c4),(w2+c3,h2+c4))
         pygame.draw.line(windowSurfaceObj, yellowColor, (w2+c3,h2+c4),(w2-c3,h2+c4))
         pygame.draw.line(windowSurfaceObj, yellowColor, (w2-c3,h2+c4),(w2-c3,h2-c4))


      
   pygame.display.update(0,0,width,height)

   oldvWindow  = vWindow
   oldhWindow = hWindow
   oldTriggers = Triggers
   oldThreshold = Threshold
   oldthres = thres
   oldZoom = Zoom
   oldrpibr = rpibr
   oldrpico = rpico
   oldrpiss = rpiss
   oldrpiexno = rpiexno
   oldrpiISO = rpiISO
   oldrpiev = rpiev
   oldCapture = Capture
   oldshots = shots
   oldrpiawbno = rpiawbno
   oldrpimmno = rpimmno
   oldtimelapse = timelapse
   oldtimeperiod = timeperiod
   oldfullsize = fullsize
   oldauto_c = auto_c
   oldrpist = rpist
   oldrpibm = rpibm
   olddet_area = det_area
   change = 0

# read mouse or keyboard

   for event in pygame.event.get():
       if event.type == QUIT:
          if use_Pi_Cam == 1:
             os.killpg(p.pid, signal.SIGTERM)
          pygame.quit()
          sys.exit()
           
       elif event.type == MOUSEBUTTONUP or event.type == KEYDOWN:
          restart = 0
          change = 1
          
          z = 0
          kz = 0
          if event.type == KEYDOWN:
             kz = event.key
             
          if event.type == MOUSEBUTTONUP:
             mousex,mousey = event.pos
             if Display > 3:
                x = mousex/32
                if mousey > height:
                   y = (mousey-height)/32
                   z = (10*x)+y
                   #print z
             else:
                if mousex > width:
                   if mousey < 160:
                      x = int((mousex - width)/32)
                      y = int(mousey/32)+1
                      z = (10*x)+y
                   if mousey > 160 and mousey < 320:
                      x = int((mousex - width)/32)+6
                      y = int((mousey-160)/32)+1
                      z = (10*x)+y
                   if mousey > 320:
                      x = int((mousex - width)/32)+12
                      y = int((mousey-320)/32)+1
                      z = (10*x)+y
                   #print z
             
             if mousex < width and mousey < height :
                xycle = 0
                offset3o = offset3
                offset4o = offset4
                offset3 = 0-((width/2)- mousex)
                offset4 = 0-((height/2) - mousey)
                if ((width/2) + offset3 + (hWindow /2) ) >= width or ((width/2) + offset3 - (hWindow /2) ) <=1:
                   offset3 = offset3o 
                   offset4 = offset4o 
                if ((height/2) + offset4 + (vWindow /2) ) >= height or ((height/2) + offset4 - (vWindow /2) ) <=1:
                   offset3 = offset3o 
                   offset4 = offset4o
                   
          if z == 124 or kz == 304 or kz == 303:
             Capture = Capture + 1
             if Capture > 1:
                Capture = 0
          if z == 25 or z == 35:
             rpist = rpist + 1
             if rpist > 1:
                rpist = 0
             restart = 1

          if z == 81 or z == 91:
             rpibm = rpibm + 1
             if rpibm > 1:
                rpibm = 0
             restart = 1
             
          if z == 21 or z == 31:
             timelapse = timelapse + 1
             if timelapse > 1:
                timelapse = 0

          if z == 23 or z == 33:
             fullsize = fullsize + 1
             if fullsize > 1:
                fullsize = 0
                
          if ((z > 60 and z < 76) or z==25 or z==35 or z==121 or z==131 or z==122 or z==132 or z==135 or z==81 or z==91)  and use_Pi_Cam == 1:
             os.killpg(p.pid, signal.SIGTERM)
             
          if z == 125:
             pygame.image.save(windowSurfaceObj, savdir + 'scr_pic' + str(pct)+'.jpg')
             pct +=1
             
          if z == 135 and use_Pi_Cam == 1:
             os.killpg(p.pid, signal.SIGTERM)
             rpistr = "raspistill -o " + fname + " -co " + str(rpico) + " -br " + str(rpibr)
             if rpiex != 'off':
                rpistr = rpistr + " -t 800 -st -ex " + rpiex
             else:
                rpistr = rpistr + " -t 10 -st -ss " + str(rpiss)
             if rpiISO > 0:
                rpistr = rpistr + " -ISO " + str(rpiISO)
             if rpiev != 0:
                rpistr = rpistr + " -ev " + str(rpiev)
             if rpist == 1:
                rpistr = rpistr + " -st "
             else:
                rpistr = rpistr + " -awb " + rpiawb
             if rpiawb == 'off':
                rpistr = rpistr + " -awbg " + str(rpiawbr) + "," + str(rpiawbb)
             rpistr = rpistr + " -n -sa " + str(rpisa) +  " -mm " + rpimm + " -q  " + str(rpiq)
             path = rpistr + ' -w 2592 -h 1944'
             #print path
             os.system (path)
             restart = 1

          if z == 14:
             Triggers = Triggers +1
             if Triggers > 99:
                Triggers = 99
                
          if z == 4:
             Triggers = Triggers - 1
             if Triggers < 1:
                Triggers = 1

          if z == 32:
             timeperiod = timeperiod +1
             if timeperiod > 9999:
                timeperiod = 9999
                
          if z == 24:
             auto_c = auto_c - 1
             if auto_c < 0:
                auto_c = 3

          if z == 34:
             auto_c = auto_c +1
             if auto_c > 3:
                auto_c = 0

          if z == 82:
             det_area = det_area - 1
             if det_area < 0:
                det_area = 1

          if z == 92:
             det_area = det_area +1
             if det_area > 1:
                det_area = 0
                
          if z == 22:
             timeperiod = timeperiod - 1
             if timeperiod < 1:
                timeperiod = 1
                
          if z == 133:
             shots = shots +1
             if shots > 99:
                shots = 99
                
          if z == 123:
             shots = shots - 1
             if shots < 1:
                shots = 1
                      
          if z == 71 :
             rpibr = rpibr + 2
             if rpibr >= 100:
                rpibr = 100
             if use_Pi_Cam == 0:
                cam.set_controls(0,0,rpibr)
             restart = 1
             
          if z == 61 :
             rpibr = rpibr - 2
             if rpibr <= 0:
                rpibr = 0
             if use_Pi_Cam == 0:
                cam.set_controls(0,0,rpibr)
             restart = 1
             
          if z == 62 :
             rpico = rpico - 5
             if rpico <= -100:
                rpico = -100
             restart = 1
             
          if z == 72 :
             rpico = rpico + 5
             if rpico >= 100:
                rpico = 100
             restart = 1
             
          if z == 63 and use_Pi_Cam == 1 and rpiex == 'off':
             if rpiss < 20000:
                rpiss = rpiss - 1000
             if rpiss >= 20000 and rpiss <= 490000:
                rpiss = rpiss - 10000
             if rpiss > 490000:
                rpiss = rpiss - 100000
             if rpiss <= 1000:
                rpiss = 1000
             restart = 1
             
          if z == 73 and use_Pi_Cam == 1  and rpiex == 'off':
             if rpiss < 20000:
                rpiss = rpiss + 1000
             if rpiss >= 20000 and rpiss <= 490000:
                rpiss = rpiss + 10000
             if rpiss > 490000:
                rpiss = rpiss + 100000
             if rpiss >= 6000000:
                rpiss = 6000000
             restart = 1
             
          if z == 63 and use_Pi_Cam == 1 and rpiex != 'off':
             if rpiev >= -9:
                rpiev = rpiev - 1
             restart = 1
             
          if z == 73 and use_Pi_Cam == 1  and rpiex != 'off':
             if rpiev <= 9:
                rpiev = rpiev + 1
             restart = 1
             
          if z == 65 :
             if rpiISO > 0:
                rpiISO = rpiISO - 100
                rpiev = 0
             if rpiISO <= 0:
                rpiISO = 0
             restart = 1
             
          if z == 75 :
             rpiISO = rpiISO + 100
             rpiev = 0
             if rpiISO >= 800:
                rpiISO = 800
             restart = 1   
             
          if z == 12:
             hWindow  = hWindow  + 5
             if hWindow  > maxwin:
                hWindow  = maxwin
             if ((width/2) + offset3 + (hWindow /2) ) >= width:
                hWindow  = hWindow  - 5
             if ((width/2) + offset3 - (hWindow /2) ) <=1:
                hWindow  = hWindow  - 5
              
          if z == 2:
             hWindow  = hWindow  - 5
             if hWindow  < minwin:
                hWindow  = minwin

          if z == 11:
             vWindow  = vWindow  + 5
             if vWindow  > maxwin:
                vWindow  = maxwin
             if ((height/2) + offset4 + (vWindow /2) ) >= height:
                vWindow  = vWindow  - 5
             if ((height/2) + offset4 - (vWindow /2) ) <=1:
                vWindow  = vWindow  - 5
              
          if z == 1:
             vWindow  = vWindow  - 5
             if vWindow  < minwin:
                vWindow  = minwin
                 
          if z == 134 or kz == K_t:
             thres = thres + 1
             if thres > 1:
                thres = 0

          if z == 3:
             Threshold = Threshold -1
             if Threshold < 1:
                Threshold = 1
                
          if z == 13:
             Threshold = Threshold +1
             if Threshold > 255:
                Threshold = 255

          if z == 74 and use_Pi_Cam == 1 :
             if rpiexno < 8:
                rpiexno = rpiexno + 1
                rpiex = rpimodes[rpiexno]
                pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+2,b2y + 99, 60, 15))
                if rpiex == 'off':
                   keys2 ("Exp Time",12,6,b2x+4,b2y + 100,0)
                else:
                   keys2 ("       eV",12,6,b2x+4,b2y + 100,0)
             restart = 1
             
          if kz == K_m and use_Pi_Cam == 1 :
             rpiexno = rpiexno + 1
             if rpiexno > 8:
                rpiexno = 0
             rpiex = rpimodes[rpiexno]
             pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+2,b2y + 99, 60, 15))
             if rpiex == 'off':
                keys2 ("Exp Time",12,6,b2x+4,b2y + 100,0)
             else:
                keys2 ("       eV",12,6,b2x+4,b2y + 100,0)
             restart = 1
             
          if z == 64 and use_Pi_Cam == 1 :
             if rpiexno > 0:
                rpiexno = rpiexno - 1
                rpiex = rpimodes[rpiexno]
                pygame.draw.rect(windowSurfaceObj,greyColor,Rect(b2x+2,b2y + 99, 60, 15))
                if rpiex == 'off':
                   keys2 ("Exp Time",12,6,b2x+4,b2y + 100,0)
                else:
                   keys2 ("       eV",12,6,b2x+4,b2y + 100,0)
             restart = 1

          if z == 121 and use_Pi_Cam == 1:
             if rpist == 0:
                if rpiawbno > 0:
                   rpiawbno = rpiawbno - 1
                   rpiawb = rpiawbs[rpiawbno]
                else:
                   rpiawbno = 9
                   rpiawb = rpiawbs[rpiawbno]
             restart = 1

          if z == 131 and use_Pi_Cam == 1:
             if rpist == 0:
                if rpiawbno < 9:
                   rpiawbno = rpiawbno + 1
                   rpiawb = rpiawbs[rpiawbno]
                else:
                   rpiawbno = 0
                   rpiawb = rpiawbs[rpiawbno]
             restart = 1

          if z == 122 and use_Pi_Cam == 1 :
             if rpimmno > 0:
                rpimmno = rpimmno - 1
                rpimm = rpimms[rpimmno]
             else:
                rpimmno = 3
                rpimm = rpimms[rpimmno]
             restart = 1

          if z == 132 and use_Pi_Cam == 1 :
             if rpimmno < 3:
                rpimmno = rpimmno + 1
                rpimm = rpimms[rpimmno]
             else:
                rpimmno = 0
                rpimm = rpimms[rpimmno]
             restart = 1
             
          if z == 15 :
             if use_Pi_Cam == 1:
                os.killpg(p.pid, signal.SIGTERM)
             if Zoom < max_res:
                Zoom = Zoom + 1
                w = rpiwidth[Zoom]
                h = rpiheight[Zoom]
                scalex = rpiscalex[Zoom]
                scaley = rpiscaley[Zoom]
                offset5 = int((offset5 + offset3) * scalex)
                offset6 = int((offset6 + offset4) * scaley)
                if offset5 > 0 and offset5 >= (w/2)-(width/2):
                   offset5 = (w/2)-(width/2)
                if offset5 < 0 and offset5 <= 0-((w/2)-(width/2)):
                   offset5 = 0-((w/2)-(width/2))
                if offset6 > 0 and offset6 >= (h/2)-(height/2):
                   offset6 = (h/2)-(height/2)
                if offset6 < 0 and offset6 <= 0-((h/2)-(height/2)):
                   offset6 = 0-((h/2)-(height/2))
                offset3 = 0
                offset4 = 0
                if use_Pi_Cam == 0:
                   cam.stop()
                   pygame.camera.init()
                   if Zoom == 0:
                      cam = pygame.camera.Camera("/dev/video0",(320,240))
                   if Zoom == 1 and max_res >= 1:
                      cam = pygame.camera.Camera("/dev/video0",(352,288))
                   if Zoom == 2 and max_res >= 2:
                      cam = pygame.camera.Camera("/dev/video0",(640,480))
                   if Zoom == 3 and max_res >= 3:
                      cam = pygame.camera.Camera("/dev/video0",(800,600))
                   if Zoom == 4 and max_res >= 4:
                      cam = pygame.camera.Camera("/dev/video0",(960,720))
                   if Zoom == 5 and max_res >= 5:
                      cam = pygame.camera.Camera("/dev/video0",(1280,960))
                   if Zoom == 6 and max_res >= 6:
                      cam = pygame.camera.Camera("/dev/video0",(1920,1440))
                   if Zoom == 7 and max_res >= 7:
                      cam = pygame.camera.Camera("/dev/video0",(2592,1944))
                   cam.start()
                if Zoom == 0:
                   offset3 = offset3/2
                   offset4 = offset4/2
             restart = 1
             
          if z == 5 :
             if use_Pi_Cam == 1 :
                os.killpg(p.pid, signal.SIGTERM)
             if Zoom > min_res:
                Zoom = Zoom - 1
                w = rpiwidth[Zoom]
                h = rpiheight[Zoom]
                scalex = rpiscalex[Zoom]
                scaley = rpiscaley[Zoom]
                offset5 = int((offset5 + offset3) / scalex)
                offset6 = int((offset6 + offset4) / scaley)
                if offset5 > 0 and offset5 >= (w/2)-(width/2):
                   offset5 = (w/2)-(width/2)
                if offset5 < 0 and offset5 <= 0-((w/2)-(width/2)):
                   offset5 = 0-((w/2)-(width/2))
                if offset6 > 0 and offset6 >= (h/2)-(height/2):
                   offset6 = (h/2)-(height/2)
                if offset6 < 0 and offset6 <= 0-((h/2)-(height/2)):
                   offset6 = 0-((h/2)-(height/2))
                offset3 = 0
                offset4 = 0
                if use_Pi_Cam == 0:
                   cam.stop()
                   pygame.camera.init()
                   if Zoom == 0:
                      cam = pygame.camera.Camera("/dev/video0",(320,240))
                   if Zoom == 1 and max_res >= 1:
                      cam = pygame.camera.Camera("/dev/video0",(352,288))
                   if Zoom == 2 and max_res >= 2:
                      cam = pygame.camera.Camera("/dev/video0",(640,480))
                   if Zoom == 3 and max_res >= 3:
                      cam = pygame.camera.Camera("/dev/video0",(800,600))
                   if Zoom == 4 and max_res >= 4:
                      cam = pygame.camera.Camera("/dev/video0",(960,720))
                   if Zoom == 5 and max_res >= 5:
                      cam = pygame.camera.Camera("/dev/video0",(1280,960))
                   if Zoom == 6 and max_res >= 6:
                      cam = pygame.camera.Camera("/dev/video0",(1920,1440))
                   if Zoom == 7 and max_res >= 7:
                      cam = pygame.camera.Camera("/dev/video0",(2592,1944))
                   cam.start()
                if Zoom == 0:
                   offset3 = offset3/2
                   offset4 = offset4/2

             restart = 1
                
   if use_Pi_Cam == 1 and restart > 0:
      if restart == 2:
         os.killpg(p.pid, signal.SIGTERM)
      if os.path.exists('/run/shm/test.jpg') == True:
         os.rename('/run/shm/test.jpg','/run/shm/oldtest.jpg')
      try:
         os.remove('/run/shm/test.jpg')
      except OSError:
         pass
          
      rpistr = "raspistill -o /run/shm/test.jpg -co " + str(rpico) + " -br " + str(rpibr)
      if rpiex != 'off':
         rpistr = rpistr + " -t " + str(rpit) + " -tl 0 -st -ex " + rpiex
      else:
         rpistr = rpistr + " -t " + str(rpit) + " -tl 0 -st -ss " + str(rpiss)
      if rpibm == 1:
         rpistr = rpistr + " -bm "
      if rpiISO > 0:
         rpistr = rpistr + " -ISO " + str(rpiISO)
      if rpiev != 0:
         rpistr = rpistr + " -ev " + str(rpiev)
      if rpist == 1:
         rpistr = rpistr + " -st "
      else:
         rpistr = rpistr + " -awb " + rpiawb
         if rpiawb == 'off':
            rpistr = rpistr + " -awbg " + str(rpiawbr) + "," + str(rpiawbb)
      rpistr = rpistr + " -n -sa " + str(rpisa)
      off5 = (Decimal(0.5) - (Decimal(width)/Decimal(2))/Decimal(w)) + (Decimal(offset5)/Decimal(w))
      off6 = (Decimal(0.5) - (Decimal(height)/Decimal(2))/Decimal(h)) + (Decimal(offset6)/Decimal(h))
      widx = Decimal(width)/Decimal(w)
      heiy = Decimal(height)/Decimal(h)
      rpistr = rpistr +  " -mm " + rpimm + " -q  " + str(rpiq) + " -w " + str(width) + " -h " + str(height) + " -roi " +  str(off5) + "," + str(off6) + ","+str(widx) + "," + str(heiy)
      #print rpistr
      p=subprocess.Popen(rpistr,shell=True, preexec_fn=os.setsid)
      xycle = 0
      if restart == 2:
         wt = 3
         while wt > 0:
            wt -=1
            while os.path.exists('/run/shm/test.jpg') == False:
               time.sleep(.001)
            os.rename('/run/shm/test.jpg','/run/shm/oldtest.jpg')
         omg = []
      restart = 0
