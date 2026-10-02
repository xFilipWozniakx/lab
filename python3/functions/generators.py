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
