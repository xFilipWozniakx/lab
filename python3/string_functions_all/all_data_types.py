x = str("hello world")
y = int(10)
z = float(2.12)
a = complex(1j)
b = list(("apple", "bannana", "cherry"))
c = tuple(("apple", "bannana", "cherry"))
d = range(1, 10, 2)
e = dict(name="john", age=35)
f = set(("apple", "bannana", "cherry"))
g = bool(5)
h = bytes(5)
i = bytearray(5)
j = memoryview(bytes(5))

all_variables = (x, y, z, a, b, c, d, e, f, g, h, i, j)


for i in all_variables:
    print("type of i:", type(i), "value of i:", i)
