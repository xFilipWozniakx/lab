def countdown(n):
    if n <= 0:
        print('Done!')
    else:
        print(n)
        countdown(n-1)
countdown(10)

"""
Base Case and Recursive Case
Every recursive function must have two parts:

A base case - A condition that stops the recursion
A recursive case - The function calling itself with a modified argument

Without a base case, the function would call itself forever, causing a stack overflow error.
"""

def factorial(n):
  # Base case
  if n == 0 or n == 1:
    return 1
  # Recursive case
  else:
    return n * factorial(n - 1)

print(factorial(5))

def fibonacci(n):
    if n <= 1:
        return n 
    else:
        return fibonacci(n-1) + fibonacci(n-2)
print(fibonacci(7))

list_a = [1,2,3,4,5]
# calculate the sum of all elements:

def sum_list(numbers):
    if len(numbers) == 0:
        return 0
    else:
        return numbers[0] + sum_list(numbers[1:])

print(sum_list(list_a))

# recursion have limits to check yours
# import sys
# print(sys.gerrecursionlimit())
# to change recursion limits
# sys.setrecursionlimit(2000)
# beaware this can cause crashes


