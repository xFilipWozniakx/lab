# isinstance(object, type)
#
var = "string"
var_2 = 22
var_3 = list(("im", "like", "python3"))

if isinstance(var, str):
    print("true")
else:
    print("no")

if isinstance(var_2, (int, str, list)):
    print("yes")
else:
    print("no")

if isinstance(var_3, (int, str, list)):
    print("yes")
else:
    print("no")


class MyObj:
    name = "John"


y = MyObj()

if isinstance(y, MyObj):
    print("yes")
else:
    print("no")


# The issubclass() function, to check if an object is a subclass of another object.
#
