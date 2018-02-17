# rrb3test.py 


import time
import rrb3



# ############ rrb4rwp TEST MAIN ######################
	
def main():
    print "*** rrb3test.py TEST MAIN ***"
    rr = rrb3.RRB3()
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
            x: exit
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
        elif key_press == 'x':
            rr.cleanup()
            quit()
            



    while True:
      event=raw_input("cmd? ") 
      key_input(event)
    rr.cleanup()

	   
	   

if __name__ == "__main__":
    main()	    

