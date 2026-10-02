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


