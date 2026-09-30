# a tuple
thistuple = ("apple",)
print(type(thistuple))

# a tuple
thistuple = tuple(("apple"))
print(type(thistuple))

# since tuples are immutable to change values have to use workournd, tuple -> list -> operation -> tuple

x = tuple(("apple", "strawberry"))
y = list(x)
y[1] = "kiwi"
x = tuple(y)
print(type(x))

# del keyword deletes tuple entirely

# unpacking tuple
fruits = ("apple", "banana", "cherry")
(green, yellow, red) = fruits
print(green)
print(yellow)
print(red)

# The number of variables must match the number of values in the tuple,
# if not, you must use an asterisk to collect the remaining values as a list.
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")
(green, yellow, *red) = fruits
print(green)
print(yellow)
print(red)

fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2
