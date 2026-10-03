# An iterator is an object that contains a countable number of values.
# Technically, in Python, an iterator is an object which implements the iterator protocol,
# which consist of the methods __iter__() and __next__().

mytuple = ('some', 'random', 'text')
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

# srings are also iterable object

# create iterator
class MyNumbers:
    def __iter__(self):
        self.a = 1 
        return self 
    def __next__(self):
        if self.a <= 20:
            x = self.a 
            self.a += 1 
            return x
        else:
            raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))

for i in myiter:
    print(i)

