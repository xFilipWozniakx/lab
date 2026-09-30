thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

thisdict_2 = {
    "brand": "Ford",
    "electric": False,
    "year": 1964,
    "colors": ["red", "white", "blue"],
}

# print(len(thisdict_2))
# print(thisdict_2["electric"])
# print(thisdict_2["colors"][1])
# print(thisdict_2.get("brand"))
#
# update items:

thisdict_2["electric"] = True
thisdict_2.update({"year": 2022})
thisdict_2.update({"VIN": "random_string_blabla"})

# or
thisdict_2["wheels"] = "winter"

# pop to remove key value pair
thisdict_2.pop("wheels")
# or popitem to remove last k:v pair

# loop
# for x in thisdict_2:
#     print(x)
#
# for x in thisdict_2.values():
#     print(x)

####
# for x in thisdict_2:
#     print(f"{x} v: {thisdict_2[x]}")
####

# for x in thisdict_2.values() / thisdict_2.keys():
#   print(x)

#
# for x, y in thisdict_2.items():
#     print(x, y)

# copy
new_dict_2 = thisdict_2.copy()
# or
new_dict = dict(thisdict_2)

# nested dicts:
myfamily = {
    "child1": {"name": "Emil", "year": "2004"},
    "child2": {"name": "Aron", "year": "2004"},
    "child3": {"name": "Malolat", "year": "1995"},
}
# or
child1 = {"name": "Emil", "year": "2005"}
child2 = {"name": "Michal", "year": "2005"}
child3 = {"name": "Darek", "year": "2005"}

my_family = {"child1": child1, "child2": child2, "child3": child3}
print(myfamily["child1"]["name"])

for x, obj in my_family.items():
    print(x)
    for y in obj:
        print(y + ":", obj[y])
