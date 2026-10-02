x = lambda a : a + 10
print(x(5))

y = lambda a, b : a * b 
print(y(5,10))

def myfunc(n):
    return lambda a : a * n 

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))

# lambda functions are commonly used with built-ins like map() filter() and sorted()

# map() applies a function to every item in an iterable
numbers = [1,2,3,4,5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

# filter() creates list of items for which a function returned true

numbers = [1,2,3,4,5,6,7,8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1], reverse = True)
print(sorted_students)

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

