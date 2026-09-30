"""
==	x == y
!=	x != y
>	x > y
<	x < y
>=	x >= y
<=	x <= y

Chaining operators:
x = 5
print(1 < x < 10)
print(1 < x and x < 10)

Logical operators:
and or not

"""

a = 20
b = 30

x = True if a < 100 and b > 15 else False
x = True if a < 100 or b > 15 else False
x = True if not a < 100 and not b > 15 else False
