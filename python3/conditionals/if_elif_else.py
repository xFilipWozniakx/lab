# simple
a = 20
b = 30
if a < b:
    print(f"{a} is < {b}")

is_logged_in = True
if is_logged_in:
    print(f"Status: {is_logged_in}")

# with multiple conditions in elif statement, first that matches evaluets to true
# conditions are evalueted top to bottom

# shorthand if one liner if
a = 5
b = 10
if a == b:
    print("vars are equal")

# or
print("equal") if a == b else print("not equal")

# or
bigger = a if a > b else b
print("Bigger is ", bigger)

"""
The syntax follows this pattern:
variable = value_if_true if condition else value_if_false
"""

# shorthand multiple conditions:
print("A") if a > b else print("=") if a == b else print("B")

x, y = 20, 50
max_value = x if x > y else y
print(f"Max values: {max_value}")

username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)

# if with logical operators
age = 25
is_student = False
has_discount_code = True

if (age < 18 or age > 65) and not is_student or has_discount_code:
    print("Discount applies!")
