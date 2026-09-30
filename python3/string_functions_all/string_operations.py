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
