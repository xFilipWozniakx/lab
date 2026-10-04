import re

# simple script censoring lines of txt file that are found by regex search
# made only to get to know python3

# next step make it more flexible, add asking client for string to search for

# open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
# methods of file objects: [
# read = read entire file as one string,
# readline() = reads single line with \n at the oend of line,
# write(string) = self explanatory + returns number of characters written  ( values have to be converted to str before writing )
# seek(offset in bytes, whence = 0 beggining of the line, 1 current pos, 2 from the end of file)
# tell() = returns int giving the file object's current position
# ]

"""
modes:
'r'
open for reading (default)
'w'
open for writing, truncating the file first
'x'
open for exclusive creation, failing if the file already exists
'a'
open for writing, appending to the end of file if it exists
'b'
binary mode
't'
text mode (default)
'+'
open for updating (reading and writing)
"""


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


test = 0
if test == 1:
    with open("alter.log", "r") as file:
        doc = file.readlines()
        for line in doc:
            indexes = re.search(":.*", line).span()
            with open("new_file.log", "a") as new_file:
                new_file.write(obf(indexes, line))
else:
    pass

# lets find out seek and tell
with open("test_file.txt", "a+b") as b_file:
    b_file.write(b"0123456789abcd")
    b_file.seek(-4, 2)
    print(b_file.tell())
    print(b_file.read(1))
