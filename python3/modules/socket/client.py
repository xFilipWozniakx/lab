# int.to_bytes(length, byteorder, *, signed=False)

import socket
import os

# TYPES:
type_1 = bytes([1])  # MESSAGE
type_2 = bytes([2])  # PICTURE_UPDATE


# FILES:
item_pic = "/home/vscode/lab/python3/modules/socket/src_pictures/tumblr_9922ba4264f6b86b7c8fd06ca46c0cc1_a5b31645_540-68e4c74257652__700.webp"


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


def send_exactly(CONNECTION, PAYLOAD: bytes, MSG_LENGHT: int) -> bool:
    send = CONNECTION.send(PAYLOAD)
    while send < MSG_LENGHT:
        send += CONNECTION.send(PAYLOAD[len(send) :])
    return send >= MSG_LENGHT


def prot_2(pic_path):
    with open(pic_path, "rb") as pic:
        pic_bytes = pic.read()
        pic_bytes_len = len(pic_bytes).to_bytes(4, "little")
    return pic_bytes, pic_bytes_len


# CHOICE MENU:
while True:
    print("Choices: (1 message) (2 update_picture) ")
    choice = int(input("What are you going to do: "))

    while choice == 1:
        send_msg(type_1, client)

        print("1 = yes, 2 = no ")
        inner_choice = int(input("Communication over?"))
        if inner_choice == 1:
            break
        elif inner_choice == 2:
            pass

    while choice == 2:
        PIC_BYTES, PIC_BYTES_LEN = prot_2(item_pic)

        # prep payload:
        PAYLOAD = type_2 + PIC_BYTES_LEN + PIC_BYTES

        if send_exactly(client, PAYLOAD, len(PAYLOAD)) == True:
            print("picture send successfuly")
            break
        else:
            print("pic didnt send seccessfuly")
