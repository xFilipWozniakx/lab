# sets are unchangable but can add or remove items from it.
# and they dont have indexes.

thisset = {"apple", "banana", "cherry", "apple"}
# print(thisset)

thisset = {"apple", "banana", "cherry", False, True}
# print(thisset)
my_list = ["some", "string"]
thisset.update(my_list)
# print(thisset)

# remove() will raise error if item does not exists / discard() will not

# join sets
"""
The union() and update() methods joins all items from both sets.
The intersection() method keeps ONLY the duplicates.
The difference() method keeps the items from the first set that are not in the other set(s).
The symmetric_difference() method keeps all items EXCEPT the duplicates.
"""
thisset = {"apple", "banana", "cherry", False, True}
thatset = {"strawberry", "kiwi", "peach"}

# new_set = thisset.union(thatset)
# or shorter syntax
new_set = thisset | thatset

# adding multiple sets:
# myset = set1.union(set2, set3, set4)
# new_set = thisset | thatset | some_set | what_ever_set

# union allows to join togheter different data types list, tuples.
# Note: The | operator only allows you to join sets with sets,
# and not with other data types like you can with the  union() method.

# The | operator only allows you to join sets with sets,
# and not with other data types like you can with the  union() method.
#
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set1.update(set2)
print(set1)
