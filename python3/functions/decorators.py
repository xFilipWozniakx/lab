def changecase(func):
    def myinner():
        return func().upper()
    return myinner

@changecase
def myfunction():
    return "Hello Sally"

print(myfunction())

# decorators with arguments
def changecase(func):
    def myinner(x):
        return func(x).upper()
    return myinner

@changecase
def myfunction(nam):
    return "Hello " + nam

print(myfunction("Filip"))

# secure decorators with *args **kwargs arguments
def changecaseargs(func):
    def myinner(*args, **kwargs):
        return func(*args,**kwargs).upper()
    return myinner

@changecaseargs
def myfunct(fname,lname,age,height):
            return f"Hello {fname} {lname}, you r {age} years old, and {height} cm high"

print(myfunct('Filip','Wu',age=30,height=1.75))

# decorator factory that takes an argument and traforms the casing based on the argument value
def changecase(n):
  def changecase(func):
    def myinner():
      if n == 1:
        a = func().lower()
      else:
        a = func().upper()
      return a
    return myinner
  return changecase

@changecase(2)
def myfunction():
  return "Hello Linus"

print(myfunction())



# multiple decorators ( Decorators are called in reverse order, from the closest to the furthest from the function)
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

def addgreeting(func):
  def myinner():
    return "Hello " + func() + " Have a good day!"
  return myinner

@changecase
@addgreeting
def myfunction():
  return "Tobias"

print(myfunction())



