# range() function often used with for loops 
# range includes 1st index and excludes last 

for i in range(0,100,2):
    print(i)

# list to display ranges
print(list(range(5)))
print(list(range(1,10)))
print(type(list(range(1,100,5))))

# ranges can be sliced just like other data types
r = range(0,10)
print(r[2])
print(r[:3])

# does not support assigment / editing values

# but supports membership testing
print(4 in r)
print(11 in r)

print(len(r))
print(list(r))

