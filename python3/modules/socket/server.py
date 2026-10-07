import socket
import os
from datetime import datetime

# 0x01      MESSAGE
# 0x02      PICTURE SEND
# 0x10      VALIDATE_DATA_WITH_SOURCE

# STATUS CODES
# 200 : c8 : OK
# 201 : c9 : ERROR
# 202 : ca
# 203 : cb
# 204 : cc
# 205 : cd
# 206 : ce
# 207 : cf

STATUS_CODE_DICT = {
    b"\xc8": b"OK",
    b"\xc9": b"ERROR"
}

#
# ┌──────────┬──────────────┬──────────────────────┐
# │ TYPE     │ LENGTH       │ PAYLOAD              │
# │ 1 bajt   │ 4 bajty      │ LENGTH bajtów        │
# └──────────┴──────────────┴──────────────────────┘
#

#
# 1. odbiera 1 bajt TYPE
# 2. sprawdza TYPE
# 3. odbiera 4 bajty LENGTH
# 4. sprawdza LENGTH
# 5. odbiera dokładnie LENGTH bajtów
# 6. sprawdza, czy odebrał kompletny payload
# 7. interpretuje payload zależnie od TYPE
#

# AF_INET for ipv4 / SOCK_STREAM for TCP protocol

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5555))
server.listen()


def receive_exactly(CONNECTION, LENGTH: int, address_client):
    try:
        frame = CONNECTION.recv(LENGTH)
        while len(frame) < LENGTH:
            more = CONNECTION.recv(LENGTH - len(frame))
            if more == b"":
                print(f"{address_client} lost connection")
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
        print(f"{address_client} exceed 30s idle state while in operation mode")
        CONNECTION.close()
        return b""
        # should add loggin instead of priting

def send_exactly(CONNECTION, PAYLOAD: bytes, MSG_LENGTH: int) -> bool:
    sent = CONNECTION.send(PAYLOAD)
    while sent < MSG_LENGTH:
        sent += CONNECTION.send(PAYLOAD[len(sent) :])
    return sent >= MSG_LENGTH

def send_status_code(CONNECTION, STATUS_CODE):
    frame = (
        STATUS_CODE
        + len(STATUS_CODE_DICT[STATUS_CODE]).to_bytes(4, "little")
        + STATUS_CODE_DICT[STATUS_CODE]
    )

    sent = CONNECTION.send(frame)
    while sent < len(frame):
        sent += CONNECTION.send(frame[len(sent) :])
    return sent >= len(frame)


while True:
    connection, address_client = server.accept()
    connection.settimeout(30)
    # where connection = local address / address_client = remote address
    print(f"connected: {address_client}")

    while True:
        frame = receive_exactly(connection, 5, address_client)

        if frame == b"":
            print("client lost connection")
            break

        match frame[0]:
            case 0x01:
                LENGTH = int.from_bytes(frame[1:5], "little")
                frame = receive_exactly(connection, LENGTH, address_client)
                if frame != b"":
                    STATUS_CODE = b"\x00"
                    try:
                        with open("message_file.txt", "a") as file:
                            date = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            msg = f"{date}: {frame.decode('utf-8')} \n"
                            file.write(msg)

                            STATUS_CODE = b"\xc8"

                    except:
                        # any kind of error
                        STATUS_CODE = b"\xc9"
                    finally:
                        if send_status_code(connection, STATUS_CODE) == True:
                            print(f"{address_client} received status code")
                        else:
                            print(f"{address_client} didnt receive status code")

                else:
                    print("client lost connection")
                    break

            case 0x02:
                LENGTH = int.from_bytes(frame[1:5], "little")
                frame = receive_exactly(connection, LENGTH, address_client)
                if frame != b"":
                    path_for_pics = (
                        "/home/vscode/lab/python3/modules/socket/dest_pictures/"
                    )

                    # need to make different system for naming
                    with open(f"{path_for_pics}cat_pic.webp", "wb") as file:
                        file.write(frame)
                else:
                    print("client lost connection")
                    break
            case _:
                print(f"Protocol unknown from {address_client}")
                connection.close()
