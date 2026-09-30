# extend list
list_main = ["some", "text", 20]
lista = ["world"]
list_main += lista
# print(list_main)

thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
# print(thislist)

# both works the same way

thislist = ["apple", "banana", "cherry"]
thistuple = ("kiwi", "orange")
thislist.extend(thistuple)
# print(thislist)

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango", "banana"]
# print(thislist[2:5])

# insert into index
# list.insert(pos,item)
# append on the end
# list.append(item)

# remove deletes first occurence
thislist.remove("banana")

# pop removes specified index from list
thislist.pop(-1)  # no banana in the list both occurences deleted
# print(thislist)  # if not specified index in pop, takes last index

del thislist[-5]  # works like pop
thislist.clear()  # clears entire list
# print(thislist)

thislist2 = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango", "banana"]

# loop throught items
for x in thislist2:
    # print(x)
    pass
# loop thourght indexes print out item
for i in range(len(thislist2)):
    # print(thislist2[i])
    pass
# loop thourght with while loop
i = 0

# while i < len(thislist2):
#     print(thislist2[i])
#     i += 1

# looping using list comprehension ( shortest syntax )
thislist = ["apple", "banana", "cherry"]
# [print(x) for x in thislist]

# list comprehension to create new list object with items that contain a
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []

# long version
# for item in fruits:
#     if "a" in item:
#         newlist.append(item)
# print(newlist)

# short version
newlist = [x for x in fruits if "a" in x]
# print(newlist)

# list comprehension syntax
# newlist = [expression for item in iterable if condition == True]
newlist_2 = [x.upper() for x in fruits if "k" in x]

# Return "orange" instead of "banana":
newlist = [x if x != "banana" else "orange" for x in fruits]

# sorting list
# bare sort sorts alfabethicaly
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
# or from lowest to highiest

thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse=True)  # reverse self explanatory
# print(thislist)


# sort list with my own function
def my_sort_func(n):
    return abs(n - 50)


thislist = [100, 50, 65, 82, 23]
thislist.sort(key=my_sort_func)
# print(thislist)


# capital letters mixed in lists can give unexpected resoults
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
# print(thislist)

# sorting lists with case-insenstive sort aids it (str.lower)
thislist.sort(key=str.lower)
# print(thislist)

# to reverse order in list use list.reverse()
thislist.reverse()
# print(thislist)

# copy a list
# You cannot copy a list simply by typing list2 = list1, because:
# list2 will only be a reference to list1,
# and changes made in list1 will automatically also be made in list2.
# so i have to do list.copy()
new_list = thislist.copy()

# another method
new_list2 = list(thislist)
print(new_list2)
