import json
import sys
import os
import importlib.util
import socket
import hashlib


# import self made explorer() 
spec = importlib.util.spec_from_file_location(
    "explorer", "/home/vscode/lab/python3/modules/os/explorer.py"
)
if spec is None:
    raise ImportError("Could not create spec for explorer")
explorer = importlib.util.module_from_spec(spec)
sys.modules["explorer"] = explorer
spec.loader.exec_module(explorer)


# PROTOCOLS:
type_1 = b"\x01"  # MESSAGE
type_2 = b"\x02"  # PICTURE_UPDATE
type_3 = b"\x03"  # AUTHENTICATE


# STATUS CODES:
STATUS_CODE_DICT = {
    b"\xc8": b"OK",
    b"\xc9": b"ERROR"
}

# creds:
credentials_dict = {
        "login": "random_login",
        "password": "random_password"
        }

# MAKE CONNECTION TO SERVER
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))


def create_payload(PROTOCOL: bytes, item) -> bytes:
    if PROTOCOL == type_1:
        DATA = item.encode("utf-8")
    elif PROTOCOL == type_2:
        with open(item, "rb") as pic:
            DATA = pic.read()
    elif PROTOCOL == type_3:
        DATA = item.encode('utf-8')
    else:
        raise ValueError("Unknown protocol type")

    return PROTOCOL + len(DATA).to_bytes(4, "little") + DATA


# SERVER STATUS CODES PARSER:
def receive_exactly(CONNECTION, LENGTH: int) -> bytes:
    try:
        frame = CONNECTION.recv(LENGTH)
        while len(frame) < LENGTH:
            more = CONNECTION.recv(LENGTH - len(frame))
            if more == b"":
                break
            else:
                frame += more
        if len(frame) != LENGTH:
            # return bytes
            return b""
        else:
            # return bytes
            return frame

    except socket.timeout:
        CONNECTION.close()
        return b""
        # should add loggin instead of priting

def send_exactly(CONNECTION, PAYLOAD: bytes, MSG_LENGTH: int) -> bool:
    sent = CONNECTION.send(PAYLOAD)
    while sent < MSG_LENGTH:
        sent += CONNECTION.send(PAYLOAD[len(sent) :])
    return sent >= MSG_LENGTH

def send_status_code(CONNECTION, STATUS_CODE) -> bool:
    frame = (
        STATUS_CODE
        + len(STATUS_CODE_DICT[STATUS_CODE]).to_bytes(4, "little")
        + STATUS_CODE_DICT[STATUS_CODE]
    )

    sent = CONNECTION.send(frame)
    while sent < len(frame):
        sent += CONNECTION.send(frame[len(sent) :])
    return sent >= len(frame)

def AUTHENTICATE_CLIENT(credential_dict):
    credentials_object = json.dumps(credentials_dict)
    DATA = create_payload(type_3,credentials_object)
    print(DATA)

    status = send_exactly(client,DATA,len(DATA))
    

    if status == True:
        header = receive_exactly(client, 5)
        if header == b"":
            print("server lost connection")
        else:
            STATUS_CODE = header[0]
            LENGTH = int.from_bytes(header[1:5], "little")
            payload = receive_exactly(client, LENGTH)
            print(payload.decode("utf-8"))
    else:
        print("did not receive status code from server")



# CHOICE MENU:
while True:

    
    print("Choices: (1 message) (2 update_picture) (3 auth)")
    choice = int(input("What are you going to do: (takes-int) "))

    
    while choice == 1:
        message = input("Insert message for server to write: \n")
        PAYLOAD = create_payload(type_1, message)
        status = send_exactly(client, PAYLOAD, len(PAYLOAD))
        if status == True:

            header = receive_exactly(client, 5)
            if header == b"":
                print("server lost connection at status code recieving")
            else:
                STATUS_CODE = header[0]
                LENGTH = int.from_bytes(header[1:5], "little")
                payload = receive_exactly(client, LENGTH)
                print(payload.decode("utf-8"))
        else:
            print("no status code for you")

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
            header = receive_exactly(client, 5)
            if header == b"":
                print("server lost connection")
            else:
                STATUS_CODE = header[0]
                LENGTH = int.from_bytes(header[1:5], "little")
                payload = receive_exactly(client, LENGTH)
                print(payload.decode("utf-8"))
        else:
            print("did not receive status code from server")
            break
    if choice == 3:
        AUTHENTICATE_CLIENT(credentials_dict)


    
