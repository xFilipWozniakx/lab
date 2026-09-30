"""
Definition and Usage
The join() method takes all items in an iterable and joins them into one string.

A string must be specified as the separator.

Syntax
string.join(iterable)
Parameter Values
Parameter	Description
iterable	Required. Any iterable object where all the returned values are strings
"""

string = "Lorem ipsum dolor sit amet."
string_2 = "Fusce Diam Nam Sit Eros"
lorem = (string, string_2)

# print(string.find("ipsum"))

print(" ".join(lorem))

spaces = "              "
print("number of spaces in spaces:" + str(len(spaces)))
