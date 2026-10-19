# args become list and kwargs become dict 


# if you dont know how many arguments will be passed to function use * before argument name
def my_function(*args):
    n = 0
    for i in args:
        print(f'parameter {n}: {i}')
        n += 1 

my_function('Emil','Filip','Michael')

def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")

## **kwargs ( if function do not recive all nesesery kwargs will raise error)
def my_function(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function(name = "Tobias",age = 30 , city = "Bergen")

def my_function(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function("User Info", "Emil", "Tobias", age = 25, city = "Oslo")

#unpacking args 
def my_function(a,b,c):
    return a + b + c 

numbers = [1,2,3]
result = my_function(*numbers)
print(result)

def my_function(fname, lname):
  print("Hello", fname, lname)

person = {"fname": "Emil", "lname": "Refsnes"}
my_function(**person) # Same as: my_function(fname="Emil", lname="Refsnes")


