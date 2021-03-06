# posie-web.py      based on RosieTheRed Robot rosie-web.py
#
# Changes:
#  GPIO.cleanup() -> rr.cleanup
#  from rwpilib.rrb3
#  (assumes running from pi/RWPi/posie/posie-web/
#  added rr.report("...") to make posie talk
#  added time limits for all motor commands
#  changed static/style.css  added text-align: center, changed background to background-color: coral, 12px corners
# 
# Point browser to Posie's IP port 5000 e.g. http://RWPi:5000
#   if background color is not set - browse http://RWPi:5000/static/style.css, then go back to root page
#
import time                     # Module required for time.sleep() function

from rwpilib.rrb3 import *      # All functions of module required for RasPiRobot v3
from squid import *             # All functions of module required for RGB LED ('squid')

from threading import Thread    # Required for starting and managing threads in Python

from flask import Flask, render_template, request, url_for, redirect        # Required by Flask

# Create an instance of RasPiRobot v3 motor controller object
# More information: https://github.com/simonmonk/raspirobotboard3
rr = RRB3(9.0, 6.0)

# Create an instance of 'Squid' object, using GPIO pins 16, 20 and 21
# More information: https://github.com/simonmonk/squid
rgb = Squid(16, 20, 21)

# Create an instance of our Flask web application
app = Flask(__name__)

# New function, to be looped in an infinite background thread, that monitors distance and changes alert levels
# Also changes RGB LED colour and stops motors when too close
def check_distance():
    print("POSIE: I've started my distance sensor...\r")

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
                print("POSIE: Too close!  Too close!\r")
                rr.report("Too close! Too Close!")

        # Else if last and current distances are both below warning level
        # if not already at alert_level 1,
        # set alert_level to 1, change LED colour to yellow and print message
        elif distance < distance_warning and distance_last < distance_warning:
            if alert_level != 1:
                alert_level = 1
                rgb.set_color(YELLOW)
                print("POSIE: I don't like the look of that...\r")
                rr.report("I don't like the look of that.")

        # Else if last and current distances are both equal to or above warning level
        # if not already at alert_level 0,
        # set alert_level to 0, change LED colour to blue and print message
        elif distance >= distance_warning and distance_last >= distance_warning:
            if alert_level != 0:
                alert_level = 0
                rgb.set_color(BLUE)
                print("POSIE: It's all good.\r")
                rr.report("It's all good now.")

        # Set current distance to be last_distance before looping
        distance_last = distance 
        time.sleep(0.1)                     # Repeat loop every tenth of a second

#------------------------------------------NEW------------------------------------------
# These Flask functions are bound to HTTP routes

# This function simply returns the index.html main page to client
@app.route("/")
def index():
    return render_template("index.html")

# This function deals with HTTP posts made by the client, and controls motor accordingly
@app.route("/control", methods = ["POST"])
def control_rosie():
    control = request.form.get("control")
    if control == "Forward":
        # If too close, disable control to move forwards and log message instead
        if alert_level != 2:
            rr.forward(1.0, 0.5)
            print("POSIE: I'm moving forwards.\r")
            rr.report("I'm going forwards.")
        else:
            print("POSIE: For your safety, forward is currently disabled.\r")
            rr.report("For your safety, forward is currently disabled.")
    elif control == "Reverse":
        rr.reverse(0.5, 0.5)
        print("POSIE: I'm going backwards.\r")
        rr.report("I'm going backwards.")
    elif control == "Right":
        rr.right(0.25)
        print("POSIE: I'm turning right.\r")
        rr.report("I'm turning right.")
    elif control == "Left":
        rr.left(0.25)
        print("POSIE: I'm turning left.\r")
        rr.report("I'm turning left.")
    else:
        rr.stop()
        print("POSIE: I've stopped.\r")
        rr.report("I've stopped.")
    return redirect(url_for("index"))
#---------------------------------------------------------------------------------------

# Main program
if __name__ == "__main__":
    try:

        print("POSIE: I'm starting up...\r")
        rr.report("I'm starting up.")

        # Code to start a continuous background thread, to monitor distance and to change alert level (function: check_distance)
        t = Thread(target = check_distance)     # Declare thread for distance checking
        t.daemon = True                         # Start as a daemon
        t.start()                               # Start thread for distance checking

        # Start Flask web server, make it accessible across the network on port 5000
        app.run(host = "0.0.0.0")

    except KeyboardInterrupt:
        #GPIO.cleanup()
        rr.cleanup()
