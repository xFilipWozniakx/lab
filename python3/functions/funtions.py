# simple function
def my_function():
    print('hello from function')

my_function()

# simple function with return 
def my_function():
    return 'hello from function'

my_msg = my_function()
print(my_msg)

# shorter syntax:
print(my_function())

# function with arguments
def my_function(fname):
    return f'hello {fname}'

print(my_function("Filip"))

"""
A parameter is the variable listed inside the parentheses in the function definition.
An argument is the actual value that is sent to the function when it is called.
"""
def my_function(fname):         # ( fname = parameter)
    return f'hello {fname}'

print(my_function("Filip"))     # ( "Filip" = argument)

# function can be done with default value for parameters
def my_function(fname = 'Filip'):
    return f'hello {fname}'

print(my_function())

# keyword parameters
def my_function(fname, age):
    return f'hello {fname}, your age is {age}'

# order does not matter with keyword arguments
print(my_function(age = 30, fname = "Filip"))

# when function called with positional arguments, order matters: ( positional becomes if no keyword in parameter section)
print(my_function("Filip", 30))

# can mix positional and keyword arugments but positional must come first
def my_func(name,age,cat_name,cat_age):
    print(f"Hello {name}, your cat name is {cat_name} and his age is {cat_age}, and your age is {age}")

my_func("Filip",30,cat_age=3,cat_name="Madi")

# functions can take any data type, and those will be preserved in function

some_list=['dog','cat','turtle']
dicti = {"pet":"dog", "age":3}

def loop_thourght(data_type):
    for i in data_type:
        print(i)

loop_thourght(some_list)
loop_thourght(dicti)

def loop_dict(data_type):
    print(f"type of pet: {data_type['pet']}\n age of pet {data_type['age']}")
loop_dict(dicti)

# can perform operations on return values

def some_math(a,b):
    return a * b 
print(some_math(10,20))

# or function can return any type of data:
list_a = ['banana', 'strawberry', 'kiwi']
def return_list(lista):
    return lista

returned = return_list(list_a)
print(returned[0])
print(returned[1])
print(returned[2])

# keyword arguments only
#
def my_functi(*, name):
    print(f"hello {name}")

my_functi("Emil")

# my_functi("name = emil") would resolve in error

# Arguments before / are positional-only, and arguments after * are keyword-only:
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)



