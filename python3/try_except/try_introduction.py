"""
The try block lets you test a block of code for errors.
The except block lets you handle the error.
The else block lets you execute code when there is no error.
The finally block lets you execute code, regardless of the result of the try- and except blocks.
"""
x = ""

try:
    print(x)
except NameError:
    print("Variable x is not defined")
except:
    print("An exception occured")
else:
    print("No errors")
finally: 
    print("Finnaly block always executed after try")

# The finally block, if specified, will be executed regardless if the try block raises an error or not.


try:
  f = open("demofile.txt")
  try:
    f.write("Lorum Ipsum")
  except:
    print("Something went wrong when writing to the file")
  finally:
    f.close()
except:
  print("Something went wrong when opening the file")

# As a Python developer you can choose to throw an exception if a condition occurs.
# To throw (or raise) an exception, use the raise keyword.

x = -1 
if x < 0:
    raise Exception("Sorry, no numbers bellow 0")

x = "hello"

if not type(x) is int:
  raise TypeError("Only integers are allowed")


