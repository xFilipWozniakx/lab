import math

# Python has a set of built-in math functions, 
# including an extensive math module, that allows you to perform mathematical tasks on numbers.

# The min() and max() functions can be used to find the lowest or highest value in an iterable:
x = [3,2,5,10,1000,100]
print(min(x))
print(max(x))

# The abs() function returns the absolute (positive) value of the specified number:
# so how far from zero the number is 
print(abs(8*-97434))

# pow() returns value of x powered to y
print(pow(3,3))

# sqrt() returns square root of number, returns float 
square_root = math.sqrt(81)
print(square_root)

# ceil() rounds number to the closest int floor() rounds downwords to the closest int
num = 25.55
print(math.ceil(num))
print(math.floor(num))

# pi() holds pi value
pi = math.pi
print(pi)
