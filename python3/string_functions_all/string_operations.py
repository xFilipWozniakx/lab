# in keyword
var = "best"
txt = "the best things in life are not for free"
if var in txt:
    print("var y")
else:
    print("var n")

# slicing
x = "Welcome"
print(x[-6:-3])
# last character excluded, while doing negative indexing excludes last as it was the first

# string modifications:
a = "Hello, world"
print(a.upper())
# or
# upper = "some string".upper()

print(a.lower())

# strip removes white spaces from the beggining and end of the string
print(a.strip())

# replace replaces char from 1st paremeter to the 2nd
print(a.replace("H", "J"))

# split splits strings parameter = delimiter returns type list
b = a.split(",")
print(type(b))

## string concatenate
a = "Hello"
b = "World"
# c = a + b
# or
c = a + " " + b
print(c)

a = "join"
b = "the"
c = "party"

print(a.replace("j", "J") + " " + b + " " + c.upper())

## f-strings format strings
age = 36
txt = f"My name is John, and im {age}"
print(txt)

# f-strings can contain of modifiers, functions or operations and variables
item = ("banana", "apple")
price_b = 35.50
price_a = 5.555

txt = f"price of {item[0]} is {price_b:.2f} $"

# example of arithmetical operation inside of placeholder
sum = f"sum price of {item[0]} and {item[1]} is: {price_b + price_a:.2f}"
print(f"{sum} \n cheap")

# if else conditionals in f-strings
x,y =2,3
print(f"price is: {50 if x > y else 100}")

name = 'filip'
# execute functions inside f-strings
print(f"my name is: {name.upper()}")
# The function does not have to be a built-in Python method

"""
f-string formatting types:
:<		Left aligns the result (within the available space)
:>		Right aligns the result (within the available space)
:^		Center aligns the result (within the available space)
:=		Places the sign to the left most position
:+		Use a plus sign to indicate if the result is positive or negative
:-		Use a minus sign for negative values only
: 		Use a space to insert an extra space before positive numbers (and a minus sign before negative numbers)
:,		Use a comma as a thousand separator
:_		Use a underscore as a thousand separator
:b		Binary format
:c		Converts the value into the corresponding Unicode character
:d		Decimal format
:e		Scientific format, with a lower case e
:E		Scientific format, with an upper case E
:f		Fix point number format
:F		Fix point number format, in uppercase format (show inf and nan as INF and NAN)
:g		General format
:G		General format (using a upper case E for scientific notations)
:o		Octal format
:x		Hex format, lower case
:X		Hex format, upper case
:n		Number format
:%		Percentage format
"""
x = 5
print(f"Present number {x} in binary format: {x:b}")

# format() function
quantity = 3
itemno = 567
price = 49
myorder = "I want {} pieces of item number {} for {:.2f} dollars."
# myorder = "I want {0} pieces of item number {1} for {2:.2f} dollars." 
# if you want to refer to the same value more than once, use the index number:
print(myorder.format(quantity, itemno, price))

"""
You can also use named indexes by entering a name inside the curly brackets {carname}, but then you must use names when you pass
the parameter values txt.format(carname = "Ford"):
"""
myorder = "I have a {carname}, it is a {model}."
print(myorder.format(carname = "Ford", model = "Mustang"))

