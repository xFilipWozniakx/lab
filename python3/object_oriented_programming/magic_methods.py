# Date of creation: 10/04/26-23:11 UTF

# magic methods :
"""
__init__()> Person(...)>Runs when a new object is created
__str__()>  print(obj), str(obj)>   Controls the readable text shown for an object
__repr__()> repr(obj)>  Controls the developer-facing representation
__eq__()>   obj1 == obj2>   Controls what "equal" means for the class
__add__()>  obj1 + obj2>Controls what the + operator does
__len__()>  len(obj)>   Returns the "length" of an object
__lt__()>   obj1 < obj2>Controls how objects are ordered when compared or sorted
__contains__()> item in obj>Controls what the in operator checks
__call__()> obj(...)>   Lets an object be called like a function
"""

# init runs at initialization of object, str describes what will be show at priting object lets examine rest of magic methods:

# While __str__() controls the readable, user-facing text shown when you print an object,
# __repr__() controls a more technical representation, meant for developers.

# This class has no __str__() method, so Python falls back to __repr__() when the object is printed.
# When a class defines both __str__() and __repr__(), print() uses __str__(),
# while the built-in repr() function always uses __repr__():


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Just testing"

    def __repr__(self):
        return f"Person('{self.name}'), ({self.age})"


p1 = Person("Per", 25)
print(p1)
print(repr(p1))

# Note: __str__() gives a short, readable text. __repr__() gives a more technical result,
# that looks like the code needed to recreate the object.

"""
The __eq__() Method
Most data types (string, number, list, etc) compare by content when you use == to compare them.
For objects, this is not the case. The == operator checks if the two variables point to the exact same object in memory - not if their content matches.
The __eq__() method allows you to change this behavior.
"""


# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#
# p1 = Person("Linus", 30)
# p2 = Person("Linus", 30)
#
# print(p1 == p2)
#
# Without __eq__(), two objects with identical values are still not considered equal:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eg__(self, other):
        return self.name == other.name and self.age == other.age

    def __add__(self, other):
        return self.age + other.age

    def __lt__(self, other):
        return self.age < other.age

    def __str__(self):
        return f"{self.name} and {self.age}"


p1 = Person("Linus", 30)
p2 = Person("Linus", 31)

print(p1 == p2)

# Magic methods can control what happens when you use an operator, like +, on your own objects.
# This is called operator overloading.
# Without python would rise TypeError since it would not know,
# how to add 2 objects.

print(p1 + p2)

# The __lt__() method ("less than") controls what the < operator does for your own objects.
# And sorts object with functions like sort()

p3 = Person("linus", 32)
p4 = Person("linus", 33)

x = sorted([p1, p2, p3, p4])
print(x[0])


print(f"__lt__:  {p1 < p2}")


class Company:
    def __init__(self, employees):
        self.employees = employees

    def __len__(self):
        return len(self.employees)

    def __contains__(self, name):
        return name in self.employees


c1 = Company(["Emil", "Tobias", "Linus"])

# The __len__() method controls what the built-in len() function returns for your object.
print(len(c1))

# The __contains__() method controls what in operator checks
print("Emil" in c1)


# The __call__() method lets an object be called like a function, using object() syntax.
# Unlike a regular function, it remembers its own state between calls,
# so the count keeps going up each time it is called.


class ClickCounter:
    def __init__(self):
        self.clicks = 0

    def __call__(self):
        self.clicks += 1
        return self.clicks


button_clicks = ClickCounter()

print(button_clicks())
print(button_clicks())
print(button_clicks())
