# rrb3.py Library for RWP

#    set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
#    set_driver_pins(self, left_pwm, left_dir, right_pwm, right_dir):
#    forward(self, seconds=0, speed=1.0):
#    stop(self):
#    reverse(self, seconds=0, speed=1.0):
#    left(self, seconds=0, speed=0.5):
#    right(self, seconds=0, speed=0.5):
#    step_forward(self, delay, num_steps):
#    step_reverse(self, delay, num_steps):
#    sw1_closed(self):
#    sw2_closed(self):
#    set_led1(self, state):
#    set_led2(self, state):
#    set_oc1(self, state):
#    set_oc2(self, state):
#    _send_trigger_pulse(self):
#    _wait_for_echo(self, value, timeout):
#    get_distance(self):
#    cleanup(self):

#    To use:  import rrb4rwp as rrb
#             rr=rrb.RRB3()
#             rr.forward(2,1.0)  # fwd for 2s at full speed
#             print("distance: %.1f cm" % rr.get_distance()) 
 

import time
import PDALib
# import myPyLib
import RPi.GPIO as GPIO

class RRB3:


    MOTOR_DELAY = 0.2

    
#    RIGHT_PWM_PIN = 14
#    RIGHT_1_PIN = 10
#    RIGHT_2_PIN = 25
#    LEFT_PWM_PIN = 24
#    LEFT_1_PIN = 17
#    LEFT_2_PIN = 4
#    SW1_PIN = 11
#    SW2_PIN = 9
#    LED1_PIN = 8
#    LED2_PIN = 7
#    OC1_PIN = 22
#    OC2_PIN = 27
#    OC2_PIN_R1 = 21
#    OC2_PIN_R2 = 27
#    TRIGGER_PIN = 18
    TRIGGER_PIN = 26
    ECHO_PIN = 23

    left_pwm = 0        # 0.0-1.0
    right_pwm = 0       # 0.0-1.0
    # pwm_scale = 0       # (not used for rwp)

    old_left_dir = -1   # 0=fwd, 1=bwd
    old_right_dir = -1  # 0=fwd, 1=bwd

    # #### RWPi Vars AND CONSTANTS

    LEFT = 0     # LEFT MOTOR
    RIGHT = 1    # RIGHT MOTOR

    # Motor Pins 
    # SRV 6		Motor 1 Speed (PWM)
    # SRV 7		Motor 2 Speed (PWM)

    RMotor = 6
    LMotor = 7

    MotorPin = [7,6]  # MotorPin[0] Left, MotorPin[1] Right

    # DIO 12 (A4)	Motor 1 Dir A (0=coast 1=F/Brake)
    # DIO 13 (A5)	Motor 1 Dir B (0=coast 1=R/Brake)

    # DIO 14 (A6)	Motor 2 Dir A (0=coast 1=F/Brake)
    # DIO 15 (A7)	Motor 2 Dir B (0=coast 1=R/Brake)

    M1DirA = 12
    M1DirB = 13
    M2DirA = 14
    M2DirB = 15
    MotorDirA = [14,12]  # 0 left 1 right
    MotorDirB = [15,13]  # 0 left 1 right

    MinPwr2Move = 100
    MaxPwr = 255

    ####  __init__  parameters are ignored

    def __init__(self, battery_voltage=9.0, motor_voltage=6.0, revision=2):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)




        PDALib.pinMode(self.RMotor,PDALib.PWM)  # init motor1 speed control pin
        PDALib.pinMode(self.LMotor,PDALib.PWM)  # init motor2 speed control pin 

        PDALib.pinMode(self.M1DirA,PDALib.OUTPUT)  #init motor1 dirA/Fwd    enable
        PDALib.pinMode(self.M1DirB,PDALib.OUTPUT)  #init motor1 dirB/Bkwd  enable
        PDALib.pinMode(self.M2DirA,PDALib.OUTPUT)  #init motor2 dirA/Fwd    enable
        PDALib.pinMode(self.M2DirB,PDALib.OUTPUT)  #init motor2 dirB/Bkwd  enable

        # init all direction pins to off
        PDALib.digitalWrite(self.M1DirA,0)  #set to off/coast
        PDALib.digitalWrite(self.M1DirB,0)  #set to off/coast
        PDALib.digitalWrite(self.M2DirA,0)  #set to off/coast
        PDALib.digitalWrite(self.M2DirB,0)  #set to off/coast



    def set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
        if self.old_left_dir != left_dir or self.old_right_dir != right_dir:
            self.set_driver_pins(0, 0, 0, 0)    # stop motors between sudden changes of direction
            time.sleep(self.MOTOR_DELAY)
        self.set_driver_pins(left_pwm, left_dir, right_pwm, right_dir)
        self.old_left_dir = left_dir
        self.old_right_dir = right_dir

    def set_driver_pins(self, left_pwm, left_dir, right_pwm, right_dir):  # 0.0 to 1.0, fwd=0 rev=1, 0.0-1.0, fwd=0 rev=1
        #self.left_pwm.ChangeDutyCycle(left_pwm * 100 * self.pwm_scale)
        PDALib.analogWrite(self.MotorPin[self.LEFT], int( left_pwm * (self.MaxPwr - self.MinPwr2Move) + self.MinPwr2Move ) ) #set motor pwr level
        #GPIO.output(self.LEFT_1_PIN, left_dir)
        #GPIO.output(self.LEFT_2_PIN, not left_dir)
        PDALib.digitalWrite(self.MotorDirA[self.LEFT],not left_dir)      # write 1=fwd 0=coast
        PDALib.digitalWrite(self.MotorDirB[self.LEFT],left_dir)          # write 1=bwd 0=coast

        #self.right_pwm.ChangeDutyCycle(right_pwm * 100 * self.pwm_scale)
        PDALib.analogWrite(self.MotorPin[self.RIGHT], int( right_pwm * (self.MaxPwr - self.MinPwr2Move) + self.MinPwr2Move ) ) #set motor pwr level
        #GPIO.output(self.RIGHT_1_PIN, right_dir)
        #GPIO.output(self.RIGHT_2_PIN, not right_dir)
        PDALib.digitalWrite(self.MotorDirA[self.RIGHT],not right_dir)      # write 1=fwd 0=coast
        PDALib.digitalWrite(self.MotorDirB[self.RIGHT],right_dir)          # write 1=bwd 0=coast


    def forward(self, seconds=0, speed=1.0):
        self.set_motors(speed, 0, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def stop(self):
        self.set_motors(0, 0, 0, 0)

    def reverse(self, seconds=0, speed=1.0):
        self.set_motors(speed, 1, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def left(self, seconds=0, speed=0.5):
        self.set_motors(speed, 0, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def right(self, seconds=0, speed=0.5):
        self.set_motors(speed, 1, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def step_forward(self, delay, num_steps):
        for i in range(0, num_steps):
            self.set_driver_pins(1, 1, 1, 0)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 0)
            time.sleep(delay)
        self.set_driver_pins(0, 0, 0, 0)

    def step_reverse(self, delay, num_steps):
        for i in range(0, num_steps):
            self.set_driver_pins(1, 0, 1, 0)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 0)
            time.sleep(delay)
        self.set_driver_pins(0, 0, 0, 0)

#    def sw1_closed(self):
#        return not GPIO.input(self.SW1_PIN)

#    def sw2_closed(self):
#        return not GPIO.input(self.SW2_PIN)

#    def set_led1(self, state):
#        GPIO.output(self.LED1_PIN, state)

#    def set_led2(self, state):
#        GPIO.output(self.LED2_PIN, state)

#    def set_oc1(self, state):
#        GPIO.output(self.OC1_PIN, state)

#    def set_oc2(self, state):
#        GPIO.output(self.OC2_PIN, state)

    def _send_trigger_pulse(self):
        GPIO.output(self.TRIGGER_PIN, True)
        time.sleep(0.0001)
        GPIO.output(self.TRIGGER_PIN, False)

    def _wait_for_echo(self, value, timeout):
        count = timeout
        while GPIO.input(self.ECHO_PIN) != value and count > 0:
            count -= 1

    def get_distance(self):
        self._send_trigger_pulse()
        self._wait_for_echo(True, 10000)
        start = time.time()
        self._wait_for_echo(False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        return distance_cm

    def cleanup(self):
        GPIO.cleanup()
        print "GPIO.cleanup() performed"



# ############ rrb4rwp TEST MAIN ######################
	
def main():
    print "rrb4rwp:main: *** rrb4rwp.py TEST MAIN ***"
    rr = RRB3()
    spd = 0.9    

    def print_status():
        print("Ultrasonic Distance: %.1f cm" % rr.get_distance())
        print "Speed: ", spd

    def key_input(event):
        spd = 1.0
        key_press = event  # ALAN  for Tkinter was = event.keysym.lower()
        print(key_press)

        if key_press == '?':
            print """
            w: forward
            s: reverse
            a: left
            d: right
            q: rotate left
            e: rotate right
            space: stop
            u: ultrasonic dist
            =: status
            
            ctrl-c: quit
        
            """
        if key_press == 'w':
            rr.forward(1,spd)
        elif key_press == 's':
            rr.reverse(1,spd)
        elif key_press == 'a':
            rr.left()
        elif key_press == 'd':
            rr.right()
        elif key_press == 'q':
            rr.left()
        elif key_press == 'e':
            rr.right()
        elif key_press == ' ':     # was 'space'
            rr.stop()
        elif key_press == '+':
            spd+=0.1
            if (spd > 1.0): spd = 1.0
        elif key_press == '-':
            spd-=0.1
            if (spd < 0.1): spd = 0.1
        elif key_press == 'u':
            print rr.get_distance()," cm"
        elif key_press == '=':
            print_status()
            

    # command = tk.Tk()
    # command.bind_all('<Key>', key_input)  # ALAN  '' changed to '<Key>'
    # command.mainloop()

    ### created for command line execution cntl-C to quit

    while True:
      event=raw_input("cmd? ") 
      key_input(event)
    rr.cleanup()

	   
	   

if __name__ == "__main__":
    main()	    

