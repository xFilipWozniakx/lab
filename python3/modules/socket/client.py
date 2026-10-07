# int.to_bytes(length, byteorder, *, signed=False)

import socket
import os
import hashlib


# TYPES:
type_1 = b"x01"  # MESSAGE
type_2 = b"x02"  # PICTURE_UPDATE


# FILES:
item_pic = "/home/vscode/lab/python3/modules/socket/src_pictures/tumblr_9922ba4264f6b86b7c8fd06ca46c0cc1_a5b31645_540-68e4c74257652__700.webp"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))


def create_payload(PROTOCOL: bytes, item) -> bytes:
    if PROTOCOL == type_1:
        item_bytes = item.encode("utf-8")
        PAYLOAD_LENGHT = len(item_bytes).to_bytes(4, "little")
        PAYLOAD = PROTOCOL + PAYLOAD_LENGHT + item_bytes
        return PAYLOAD
    elif PROTOCOL == type_2:
        with open(item, "rb") as pic:
            PAYLOAD = pic.read()
        return PAYLOAD
    else:
        raise ValueError("Unknown protocol type")


def send_msg(TYPE: bytes, client):

    msg = input("Type in message for python3_socket_server:\n")
    msg_b = msg.encode("utf-8")

    PAYLOAD = create_payload(type_1, msg_b)
    PAYLOAD_LENGHT = len(PAYLOAD)
    send_exactly(client, PAYLOAD, PAYLOAD_LENGHT)


def send_exactly(CONNECTION, PAYLOAD: bytes, MSG_LENGHT: int) -> bool:
    send = CONNECTION.send(PAYLOAD)
    while send < MSG_LENGHT:
        send += CONNECTION.send(PAYLOAD[len(send) :])
    return send >= MSG_LENGHT


# CHOICE MENU:
while True:
    print("Choices: (1 message) (2 update_picture) ")
    choice = int(input("What are you going to do: "))

    while choice == 1:
        message = input("Insert message for server to write: \n")
        PAYLOAD = create_payload(type_1, message)
        send_exactly(client, PAYLOAD, len(PAYLOAD))

        print("1 = yes, 2 = no ")
        inner_choice = int(input("Communication over?"))
        if inner_choice == 1:
            break
        elif inner_choice == 2:
            pass

    while choice == 2:
        # mechanizm wskazywania pliku do wyslania
        item_pic = "path"
        PAYLOAD = create_payload(type_2, item_pic)

        if send_exactly(client, PAYLOAD, len(PAYLOAD)) == True:
            print("picture send successfuly")
            break
