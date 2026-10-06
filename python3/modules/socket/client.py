# int.to_bytes(length, byteorder, *, signed=False)

import socket

# TYPES:
type_1 = bytes([1])  # MESSAGE


msg = input("Type in message for python3_socket_server:\n")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

msg_b = msg.encode("utf-8")
type_1 += len(msg_b).to_bytes(4, "little")
type_1 += msg_b

client.send(type_1)
client.send(b"")
