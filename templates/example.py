# import from subfolder ./rwpilib
import rwpilib.myPyLib as myPyLib


# other modules
import traceback
import time



# test importing from a directory of python files


# ### TEST MAIN() ######################


def main():
  print "example.py:main: Entered main()/n"
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  try:
      while True:
        print "example.py:main: press ctrl-c to quit/n"
        time.sleep(20)

    
  except SystemExit:
      print "example.py:main: Bye Bye"    

  except:
      print "Exception Raised"
      traceback.print_exc()  



if __name__ == "__main__":
    main()
