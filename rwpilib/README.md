File:  rwpilib/readme.txt
The file rwpilib/__init__.py is what makes this folder importable as a module.

--- This folder "rwpilib" contains Rug Warrior Pi library modules 
    which can be imported by a robot.py in the folder above this lib:

# File: robot.py
# import from subfolder ./rwpilib
import rwpilib.myPyLib as myPyLib
import rwpilib.file2 as file2
...

main():
  print "robot.py:main: Entered main()"
  myPyLib.set_cntl_c_handler()  # Set CNTL-C handler 
  file2.somefunc()


--- libs in this folder can reference each other 

rwpilib/file1.py contains func1:

# File:  rwpilib/file1.py
def func1():
  print "rwpilib/file1.py:func1: Entered func1()/n"
  
rwpilib/file2.py uses func1 by:

# File: rwpilib/file2.py
import file1

def somefunc():
    print "rwpilib/file2.py:somefunc: Entered somefunc()/n"
    file1.func1()
  
  