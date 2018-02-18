# rrb3test.py 


import time
import rwpilib.rrb3 as rrb



# ############ rrb4rwp TEST MAIN ######################
	
spd = 0

def main():
    global spd
    print "*** rrb3test.py TEST MAIN ***"
    rr = rrb.RRB3()
    spd = 0.9    

    def print_status():
        print("Ultrasonic Distance: %.1f in" % (rr.get_distance()/2.54))
        print "Speed: ", spd

    def key_input(event):
        global spd
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
            rr.left(1)
        elif key_press == 'd':
            rr.right(1)
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

