# different ways to create bytes:

ascii_1 = b"1"
print(ascii_1.hex())
# byte ~60 /
# \x31 3x16 + 1

int_1 = 1
int_1_b = int_1.to_bytes(1, "little")
print(int_1_b.hex())
# byte 1 / \x01
#

lista_1_bajta = []
dict_byte = {}
for i in range(255):
    # lista_1_bajta.append(i.to_bytes(1, "little").hex())
    dict_byte[f"index:{i}"] = i.to_bytes(1, "little").hex()


# print(lista_1_bajta)
for i, y in dict_byte.items():
    print(f"{i} : {y}")

print(b"\xaa")
