# rosie_distance.py   for RWPi

# Import the time module - we need this later for the sleep function
import time

# Import the RasPi Robot Board V3 module and all its functions
from rwpilib.rrb3 import *

# Create an instance of the RRB3 object
rr = RRB3()

# Import the Squid module and all its functions
from squid import *

# Create an instance of squid object, using GPIO pins 16, 20 and 21.  Choose right PINs to avoid conflict.
rgb = Squid(16, 20, 21)

# Parameters for application:
distance_danger = 25                    # Distance (cm) below which alert level becomes danger
distance_warning = 50                   # Distance (cm) below which alert level becomes warning
distance_last = distance_warning        # Last distance recorded.  Set as disance_danger value to begin with.
alert_level = 0                         # Alert level: 0 = normal, 1 = warning, 2 = danger.  Begin as normal.
rgb.set_color(BLUE)                     # Set RGB LED to blue to begin with

# Place all code in infinite loop
while True:
        
   # Get distance from instance of distance / range sensor   
   distance = rr.get_distance()

   # Print distance on screen for information
   print(distance)         

   # If last and current distances are both below danger level
   # if not already at alert_level 2,
   # set alert_level to 2, change LED colour to red and print message
   if distance < distance_danger and distance_last < distance_danger:
      if alert_level != 2:
         alert_level = 2   
         rgb.set_color(RED)
         print("ROSIE: Too close!  Too close!")
         rr.report("Too close! Too close!")

   # Else if last and current distances are both below warning level
   # if not already at alert_level 1,
   # set alert_level to 1, change LED colour to yellow and print message
   elif distance < distance_warning and distance_last < distance_warning:
      if alert_level != 1:
         alert_level = 1
         rgb.set_color(YELLOW)
         print("ROSIE: I don't like the look of that...")
         rr.report("I don't like the look of that...")

   # Else if last and current distances are both equal to or above warning level
   # if not already at alert_level 0,
   # set alert_level to 0, change LED colour to blue and print message
   elif distance >= distance_warning and distance_last >= distance_warning:
      if alert_level != 0:
         alert_level = 0
         rgb.set_color(BLUE)
         print("ROSIE: It's all good.")
         rr.report("It's all good.")

   # Set current distance to be last_distance before looping
   distance_last = distance

   # Pause for half a second before re-looping 
   time.sleep(0.5)
