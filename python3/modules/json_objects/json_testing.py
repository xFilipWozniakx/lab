import json

# json object is just like py dict, so it is parsed into one

x = '{ "fname": "John", "lname": "doe", "age": 30, "city": "New York" }'

# parse object x
y = json.loads(x)


# print(y["age"])
# print(type(y["age"]))
# print(type(y))
# 

"""
You can convert Python objects of the following types, into JSON strings:

dict
list
tuple
string
int
float
True
False
None

"""
# 
# print(json.dumps({"name": "John", "age": 30}))
# print(json.dumps(["apple", "bananas"]))
# print(json.dumps(("apple", "bananas")))
# print(json.dumps("hello"))
# print(json.dumps(42))
# print(json.dumps(31.76))
# print(json.dumps(True))
# print(json.dumps(False))
# print(json.dumps(None))
#
x = {

  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

#print(json.dumps(x))

# to make it readable
#print(json.dumps(x, indent = 4))
# and can change delimiter with keyword argument
#print(json.dumps(x, indent = 4, separators=(". ", " = ")))

print(json.dumps(x, indent=4, sort_keys=True))







