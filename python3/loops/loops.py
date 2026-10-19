# simple while loop with break statement and else at the end
i = 0 
while i < 10:
    print(i)
    i += 1
    # will never execute
    if i == 12:
        break
else: 
    print(f"condition no logner true\n i became: {i} ")

# simple for loop
fruits = ['apple', 'banana', 'grape']
for i in fruits:
    print(i)
# break and conitune works just like it would with while loop
# for can loop thought indexes in strings 
for i in "some_string":
    print(i)

# or throught ranges:
for i in range(0, 10, 2):
    print(i)

# nested for loops: 
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for i in adj:
    for y in fruits:
        print(i,y)

# for loops cannot be empty, filled up with pass
