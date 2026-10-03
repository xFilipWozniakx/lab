import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
# print(x)

"""
functions for reqex 
findall	Returns a list containing all matches
search	Returns a Match object if there is a match anywhere in the string
split	Returns a list where the string has been split at each match
sub	Replaces one or many matches with a string
"""


txt = "The rain in Spain\n Yesterday there were a rainy day in France\n In Spain corrida has started"
# u = re.findall(".*Spain.*", txt)
# print(u)

r"""
special characters
Metacharacters are characters with a special meaning:

[]	A set of characters	"[a-m]"	
\	Signals a special sequence (can also be used to escape special characters)	"\d"	
.	Any character (except newline character)	"he..o"	
^	Starts with	"^hello"	
$	Ends with	"planet$"	
*	Zero or more occurrences	"he.*o"	
+	One or more occurrences	"he.+o"	
?	Zero or one occurrences	"he.?o"	
{}	Exactly the specified number of occurrences	"he.{2}o"	
|	Either or	"falls|stays"	
()	Capture and group
"""
# index = 0
# for i in txt:
#     print(f"{i} index: {index}")
#     index += 1
# print(re.search(".?esterday", txt))


"""
flags
Use:
    r"string" does so that string is treat as raw_string so no escaping special characters needed
    re.search(r"hello", "Hello world", flags=re.IGNORECASE)

re.ASCII	re.A	Returns only ASCII matches	
re.DEBUG		Returns debug information	
re.DOTALL	re.S	Makes the . character match all characters (including newline character)	
re.IGNORECASE	re.I	Case-insensitive matching	
re.MULTILINE	re.M	Returns matches at the start/end of each line	
re.NOFLAG		Specifies that no flag is set for this pattern	
re.UNICODE	re.U	Returns Unicode matches. This is default from Python 3. For Python 2: use this flag to return only Unicode matches	
re.VERBOSE	re.X	Allows whitespaces and comments inside patterns. Makes the pattern more readable
"""


r"""
another way to use special characters:
\A	Returns a match if the specified characters are at the beginning of the string	"\AThe"	
\b	Returns a match where the specified characters are at the beginning or at the end of a word
(the "r" in the beginning is making sure that the string is being treated as a "raw string")	r"\bain"
r"ain\b"	
\B	Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word
(the "r" in the beginning is making sure that the string is being treated as a "raw string")	r"\Bain"
r"ain\B"	
\d	Returns a match where the string contains digits (numbers from 0-9)	"\d"	
\D	Returns a match where the string DOES NOT contain digits	"\D"	
\s	Returns a match where the string contains a white space character	"\s"	
\S	Returns a match where the string DOES NOT contain a white space character	"\S"	
\w	Returns a match where the string contains any word characters (characters from a to Z, digits from 0-9, and the underscore _ character)	"\w"	
\W	Returns a match where the string DOES NOT contain any word characters	"\W"	
\Z	Returns a match if the specified characters are at the end of the string	"Spain\Z"
"""

"""
groups
[arn]	Returns a match where one of the specified characters (a, r, or n) is present	
[a-n]	Returns a match for any lower case character, alphabetically between a and n	
[^arn]	Returns a match for any character EXCEPT a, r, and n	
[0123]	Returns a match where any of the specified digits (0, 1, 2, or 3) are present	
[0-9]	Returns a match for any digit between 0 and 9	
[0-5][0-9]	Returns a match for any two-digit numbers from 00 and 59	
[a-zA-Z]	Returns a match for any character alphabetically between a and z, lower case OR upper case	
[+]	In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string
"""

txt_2 = "The rain in Spain"
x = re.findall("ai", txt_2)
# print(x)

y = re.search("\s", txt_2)
# print("The first white-space character is located in position:", y.start())

# The search() function searches the string for a match, and returns a Match object if there is a match.
# If there is more than one match, only the first occurrence of the match will be returned:
# If no matches found value evaluets to None

# The split() function returns a list where the string has been split at each match:
z = re.split("\s", txt)
# print(z)
# print(type(z))
#
# for i in list(z):
#     print("type: ", type(i), "value: ", i)
#


# doesnt support negative index
# last argument refers to number of occurences in split
a = re.split("\s", txt, 2)
# print(a)

# sub() replaces delimiter with 2nd parameter
# with 4th parameter i can control number of occurences for sub()
b = re.sub("\s", "_", txt, 5)
# print(b)

# match object returned from re()

txt = "The rain in Spain"
x = re.search("ai", txt)
# print(x) #this will print an object


"""
methods for match object
.span() returns a tuple containing the start-, and end positions of the match.
.string returns the string passed into the function
.group() returns the part of the string where there was a match
"""

print(x.span())
print(x.string)
print(x.group())
