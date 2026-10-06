def po(var):
    print(var)
    print(type(var))


num = 5
num_b = num.to_bytes()
# print(num_b)
# succefully placed byte 5 into binary format

num_h = num_b.hex()
# po(num_h)
# succefully translated byte 5 into hex format output == str

# creates one byte with value 65 / x41 hex format
a = bytes([65])

# creates 65 x00 bytes ( zero bytes )
b = bytes(65)


str_b = a.decode("utf-8")
po(str_b)
txt = "Some string to send over socket"
into_bytes = txt.encode("utf-8")
po(into_bytes)
print(into_bytes.hex())

# but if try to translate str into hex:
# txt.hex() resolves into error, strings doesnt have attributes hex so by default hex representation

# lenght socket

print(int(1024).to_bytes(4, "little"))

print(int(0).to_bytes(1))
print(int(200000).to_bytes(3, "little").hex())
print(int(200000).to_bytes(4, "little").hex())


# przy przekladaniu bajtow na liczby trzeba pamietac o zalozeniu ze rozne liczby skladaja sie
# z roznych ilosci bajtow.
#
# 1b = max 255
# 2b = 255 * 255
# 4b = pow(4,255)
# przy zlym sposobie dekodowania wynik sie calkowicie pomiesza
