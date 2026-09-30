string = """ some random string """
print(len(string))
print(string)
print("index 0:", string[0])
print("index 1:", string[1])
print("index last:", string[-1])

index = 0
for i in string:
    print("index:", index, "value:", i)
    index += 1
