def check_case(value):
    match value:
        case b"":
            return "empty byte string"
        case b"x05":
            return "got what was expected"
        case "string":
            return "string value"
        case _:
            return "false read"


num = str(5)
fifth_byte = int.to_bytes(5)
bytes_representation_of_ascii_5 = num.encode("utf-8")
print(fifth_byte)

print(check_case(b""))
print(check_case(num))
print(check_case("string"))
