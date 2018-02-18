# posie_wheels_with_distance.py
# based on https://www.rosietheredrobot.com/2017/09/achoo-crash-choo-episode-ii.html
# Changes:
#   import rwpilib.rrb3
#   GPIO.cleanup() -> rr.cleanup()
#   rr.report() added after print(ROSIE: ...) statements

import sys, tty, termios        # Modules required for user input using keyboard
import time	                	# Module required for time.sleep() function

from rrb3 import *              # All functions of module required for RasPiRobot v3
from squid import *             # All functions of module required for RGB LED ('squid')

from threading import Thread    # Required for starting and managing threads in Python

# Create an instance of RasPiRobot v3 motor controller object
# More information: https://github.com/simonmonk/raspirobotboard3
rr = RRB3(9.0, 6.0)

# Create an instance of 'Squid' object, using GPIO pins 16, 20 and 21
# More information: https://github.com/simonmonk/squid
rgb = Squid(16, 20, 21)            

# ---These functions allow the program to read your keyboard (from 08_manual_robot_continuous.py)---
# More information: https://github.com/teknoteacher/raspirobot3/blob/master/08_manual_robot_continuous.py
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return ord(c3) - 65  #  0=Up, 1=Down, 2=Right, 3=Left arrows
# --------------------------------------------------------------------------------------------------

# New function, to be looped in an infinite background thread, that monitors distance and changes alert levels
# Also changes RGB LED colour and stops motors when too close
def check_distance():
    print("ROSIE: I've started my distance sensor...\r")
    rr.report("I've started my distance sensor")

    # Parameters for application:
    distance_danger = 25                    # Distance (cm) below which alert level becomes danger
    distance_warning = 50                   # Distance (cm) below which alert level becomes warning
    distance_last = distance_warning        # Set last_distance as disance_danger value to begin with.

    # A global variable, which can be accessed from outside this function
    global alert_level                      # Alert level: 0 = normal, 1 = warning, 2 = danger.  Begin as normal.
    alert_level = 0                         # Set initially to 0 (normal)

    rgb.set_color(BLUE)                     # Set RGB LED to blue to begin with
    
    while True:
        # Get distance from instance of distance / range sensor
        distance = rr.get_distance()       

        # If last and current distances are both below danger level
        # if not already at alert_level 2,
        # set alert_level to 2, change LED colour to red and print message
        # also temporarily stop motors
        if distance < distance_danger and distance_last < distance_danger:
            if alert_level != 2:
                alert_level = 2	
                rgb.set_color(RED)
                rr.stop()               # Stop Rosie's motors
                print("ROSIE: Too close!  Too close!\r")
                rr.report("Too close! Too close!")

        # Else if last and current distances are both below warning level
        # if not already at alert_level 1,
        # set alert_level to 1, change LED colour to yellow and print message
        elif distance < distance_warning and distance_last < distance_warning:
            if alert_level != 1:
                alert_level = 1
                rgb.set_color(YELLOW)
                print("ROSIE: I don't like the look of that...\r")
                rr.report("I don't like the look of that")

        # Else if last and current distances are both equal to or above warning level
        # if not already at alert_level 0,
        # set alert_level to 0, change LED colour to blue and print message
        elif distance >= distance_warning and distance_last >= distance_warning:
            if alert_level != 0:
                alert_level = 0
                rgb.set_color(BLUE)
                print("ROSIE: It's all good.\r")
                rr.report("It's all good.")

        # Set current distance to be last_distance before looping
        distance_last = distance 
        time.sleep(0.1)                     # Repeat loop every tenth of a second

# Main program.  The 'readkey()' function is blocking, therefore will initiate non-blocking background thread for distance sensor.
if __name__ == "__main__":
    try:
        
        print("ROSIE: I'm starting up...\r")
        rr.report("I'm starting up")

        # Code to start a continuous background thread, to monitor distance and to change alert level (function: check_distance)
        t = Thread(target = check_distance)     # Declare thread for distance checking
        t.daemon = True                         # Start as a daemon
        t.start()                               # Start thread for distance checking
        
        print("ROSIE: Startup complete.  Controls enabled.\r")
        print("-------------------------------------------\r")
        print("Use the arrow keys to move ROSIE\r")
        print("Press CTRL-c to quit the program\r")
        print("-------------------------------------------\r")
        
        # ---This section controls the motors (more or less from 08_manual_robot_continuous.py, with few additions)---
        # More information: https://github.com/teknoteacher/raspirobot3/blob/master/08_manual_robot_continuous.py

        # Keyboard values for up, down, right and left
        UP = 0
        DOWN = 1
        RIGHT = 2
        LEFT = 3

        while True:
            keyp = readkey()
            if keyp == UP:
                # If too close, disable control to move forwards and log message instead
                if alert_level != 2:
                    rr.forward(0, 0.5)
                    print("ROSIE: I'm moving forwards.\r")
                    rr.report("I'm moving forward")
                else:
                    print("ROSIE: For your safety, forward is currently disabled.\r")
                    rr.report("For my safety, forward is currently disabled.")
            elif keyp == DOWN:
                rr.reverse(0, 0.5)
                print("ROSIE: I'm going backwards.\r")
                rr.report("I'm going backwards.")
            elif keyp == RIGHT:
                rr.right(0.5)
                print("ROSIE: I'm turning right.\r")
                rr.report("I'm turning right.")
            elif keyp == LEFT:
                rr.left(0.5)
                print("ROSIE: I'm turning left.\r")
                rr.report("I'm turning left.") 
            elif keyp == ' ':
                rr.stop()
                print("ROSIE: I've stopped.\r")
                rr.report("I've stopped.")
            elif ord(keyp) == 3:
                print("ROSIE: keyp == 3 detected")
                break
        # ------------------------------------------------------------------------------------------------------------

    except KeyboardInterrupt:
        #GPIO.cleanup()
        rr.cleanup()
