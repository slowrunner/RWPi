# RWPi
RugWarriorPro Robot re-envisioned on Raspberry Pi in python

The Rug Warrior Pro robot was an outgrowth of an MIT (Massachusetts Institute of Technology) robotics design course. 
It came as brains, brawn (mechanical items), or brains and brawn together. 

The kit was easy to build in a weekend and provided a powerful platform for learning and 
playing with robotics and artificial reasoning. 


Credit Joseph Jones, Alice and Klaus Peters, Fred Martin, Randy Sargent, Anita Flynn, and Bruce Seiger 
with bringing this compact, powerful, well designed, and well documented robot and kit to life.

The kit is no longer sold, and the once amazing 2 MHz 68HC11 processor with 32K of RAM is relegated to history as well.

I built my RWP in 1998 and decided in 2015 to replace the "brains" with a Raspberry Pi. 

Turning a single board computer into a robot requires some interface circuitry - motor drivers, analog-to-digital conversion, 
current limited digital I/O expansion with interrupt capture.  The original Rug Warrior provided sensors, ADC, Digital I/O,
motor drivers, battery backed up memory, and much more in a very compact package.

I chose the micronauts.com Pi Alpha Droid card as the best card to mate with the Raspberry Pi over the original Rug Warrior Brawns, 
to become my new "Rug Warrior Pi".

The RWP had all of MIT and smart PHDs designing and writing example software.  My bot only has me.

My bot consists of:
* 7" round, fully skirted platform
* Two driven wheels with encoders
* 6 directions of skirt bump detection
* twin servo tilt-pan sensor platform
    * UltraSonic Distance sensor
    * Infrared Distance sensor
    * PiCam
* Voltage and Current sensors
* Single point on/off switch
* 5000mAH 7.2v LiMH rechargable power with 5v unregulated tap for servo
* USB Microphone
* Small separately powered audio amp and speaker 


This repository contains my musings in Python to create various robot behaviors.

