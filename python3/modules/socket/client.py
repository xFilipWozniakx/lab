import sys
import os
import importlib.util
import socket
import hashlib

spec = importlib.util.spec_from_file_location(
    "explorer", "/home/vscode/lab/python3/modules/os/explorer.py"
)
if spec is None:
    raise ImportError("Could not create spec for explorer")

explorer = importlib.util.module_from_spec(spec)
sys.modules["explorer"] = explorer
spec.loader.exec_module(explorer)


# TYPES:
type_1 = b"\x01"  # MESSAGE
type_2 = b"\x02"  # PICTURE_UPDATE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))


def create_payload(PROTOCOL: bytes, item) -> bytes:
    if PROTOCOL == type_1:
        DATA = item.encode("utf-8")
    elif PROTOCOL == type_2:
        with open(item, "rb") as pic:
            DATA = pic.read()
    else:
        raise ValueError("Unknown protocol type")

    return PROTOCOL + len(DATA).to_bytes(4, "little") + DATA


def send_msg(TYPE: bytes, client):

    msg = input("Type in message for python3_socket_server:\n")

    PAYLOAD = create_payload(type_1, msg)
    PAYLOAD_LENGTH = len(PAYLOAD)
    send_exactly(client, PAYLOAD, PAYLOAD_LENGTH)


def send_exactly(CONNECTION, PAYLOAD: bytes, MSG_LENGTH: int) -> bool:
    sent = CONNECTION.send(PAYLOAD)
    while sent < MSG_LENGTH:
        sent += CONNECTION.send(PAYLOAD[len(sent) :])
    return sent >= MSG_LENGTH


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
        # point to file that will be send to the server
        item_pic = explorer.explorer()
        PAYLOAD = create_payload(type_2, item_pic)

        if send_exactly(client, PAYLOAD, len(PAYLOAD)) == True:
            print("picture send successfuly")
            break
