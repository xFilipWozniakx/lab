# var created in outer function is available to inner function aswell
def myfunc():
  x = 300
  def myinnerfunc():
    print(x)
  myinnerfunc()

myfunc()

# which ever var created at global scope is available inside entire program / script 
my_var = 100

# can be overwriten by GLOBAL keyword
def change_var():
    global my_var 
    my_var = 200

change_var()
print(my_var)   # 200


# non local var 
# makes var belong to outer function
def fun():
    x = ''
    def inner_fun():
        nonlocal x 
        x = "some value"
    inner_fun()
    return x
print(fun())

x = 300
def myfunc():
    # if placed global x var would become global scope variable return will not achive that
    x = 200
  return x 
print(myfunc())
print(x)


