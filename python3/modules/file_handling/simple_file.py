import re

# simple script censoring lines of txt file that are found by regex search
# made only to get to know python3

# next step make it more flexible, add asking client for string to search for


def obf(tup, obf_string):
    list_of_indexes = []
    new_string = ""
    for i in range(tup[0], tup[1]):
        list_of_indexes.append(i)

    for obf_index in range(len(obf_string)):
        if obf_index in list_of_indexes:
            new_string += "_"
        else:
            new_string += obf_string[obf_index]
    return new_string


with open("alter.log", "r") as file:
    doc = file.readlines()
    for line in doc:
        indexes = re.search(":.*", line).span()
        with open("new_file.log", "a") as new_file:
            new_file.write(obf(indexes, line))
