import socket
import os
from datetime import datetime

# model
# create communication channel ( socket )
# bind address + port to that socket ( bind )
# start listening ( listen )
# accept incoming connection ( accept )

# 0x01      MESSAGE
# 0x02      PICTURE SEND
# 0x10      VALIDATE_DATA_WITH_SOURCE


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


def receive_exactly(conn, n, address_client):
    data = conn.recv(n)
    while len(data) < n:
        more = conn.recv(n - len(data))
        if more == b"":
            print(f"{address_client} lost connection")
            break
        else:
            data += more
    if len(data) != n:
        # return bytes
        return b""
    else:
        # return int
        return data


while True:
    connection, address_client = server.accept()
    # where connection = local address / address_client = remote address
    print(f"connected: {address_client}")

    while True:
        data = receive_exactly(connection, 5, address_client)
        match data[0]:
            case b"":
                break

            case 0x01:
                LENGHT = int.from_bytes(data[1:5], "little")
                data = receive_exactly(connection, LENGHT, address_client)
                if data != b"":
                    with open("message_file.txt", "a") as file:
                        date = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        msg = f"{date}: {data.decode('utf-8')} \n"
                        file.write(msg)
                else:
                    print("client lost connection")
                    break

            case 0x02:
                LENGHT = int.from_bytes(data[1:5], "little")
                data = receive_exactly(connection, LENGHT, address_client)
                if data != b"":
                    path_for_pics = (
                        "/home/vscode/lab/python3/modules/socket/dest_pictures/"
                    )

                    # need to make different system for naming
                    with open(f"{path_for_pics}cat_pic.webp", "wb") as file:
                        file.write(data)
                else:
                    print("client lost connection")
                    break
