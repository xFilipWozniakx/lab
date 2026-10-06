# int.to_bytes(length, byteorder, *, signed=False)

import socket

# TYPES:
type_1 = bytes([1])  # MESSAGE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))


def send_msg(TYPE, client):
    type_1 = TYPE

    msg = input("Type in message for python3_socket_server:\n")
    msg_b = msg.encode("utf-8")

    # TYPE + LENGHT
    type_leng = type_1 + len(msg_b).to_bytes(4, "little")

    # TYPE + LENGHT + PAYLOAD
    type_leng_pay = type_leng + msg_b
    leng_msg = len(type_leng_pay)

    send_exactly(client, type_leng_pay, leng_msg)


def send_exactly(CONNECTION, PAYLOAD, MSG_LENGHT):
    send = CONNECTION.send(PAYLOAD)
    while send < MSG_LENGHT:
        send += CONNECTION.send(PAYLOAD[len(send) :])
    print("MSG send succefully")


# CHOICE MENU:
while True:
    print("Choices: (1 message) ")
    choice = int(input("What are you going to do: "))

    while choice == 1:
        send_msg(type_1, client)

        print("1 = yes, 2 = no ")
        inner_choice = int(input("Communication over?"))
        if inner_choice == 1:
            break
        elif inner_choice == 2:
            pass
