from time import sleep
"""
Generators allow you to iterate over data without storing the entire dataset in memory.
Instead of using return, generators use the yield keyword.
"""

def my_generator():
    yield 1 
    yield 2 
    yield 3 

for value in my_generator():
    print(value)

# Unlike return, which terminates the function, yield pauses it and can be called multiple times.

def count_up_to(n):
    count = 1 
    while count <= n:
        yield count 
        count += 1 

for num in count_up_to(5):
    sleep(2)
    print(num)

# Generators are memory-efficient because they generate values on-the-fly instead of storing everything in memory.

def large_sequence(n):
    for i in range(n):
        yield i

gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen))

# When there are no more values to yield, the generator raises a StopIteration exception

"""

# List comprehension - creates a list
list_comp = [x * x for x in range(5)]
print(list_comp)

# Generator expression - creates a generator
gen_exp = (x * x for x in range(5))
print(gen_exp)
print(list(gen_exp))

"""

# Calculate sum of squares without creating a list
total = sum(x * x for x in range(10))
print(total)

def fibonacci():
    a, b = 0,1
    while True:
        yield a 
        a, b = b, a + b
gen = fibonacci()
for _ in range(100):
    print(next(gen))

def echo_generator():
    while True:
        received = yield
        print("Received:", received)

gen = echo_generator()
next(gen)
gen.send("Hello")
gen.send("World")

def my_gen():
  try:
    yield 1
    yield 2
    yield 3
  finally:
    print("Generator closed")

gen = my_gen()
print(next(gen))
gen.close()
