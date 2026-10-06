import socket
import os
from datetime import datetime

# model
# create communication channel ( socket )
# bind address + port to that socket ( bind )
# start listening ( listen )
# accept incoming connection ( accept )

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
        return b""
    else:
        return data


while True:
    connection, address_client = server.accept()
    # where connection = local address / address_client = remote address
    print(f"connected: {address_client}")

    while True:
        data = receive_exactly(connection, 5, address_client)
        if data == b"":
            break
        else:
            TYPE = data[0]
            LENGHT = int.from_bytes(data[1:5], "little")
            if TYPE == 1:
                data = receive_exactly(connection, LENGHT, address_client)
                if data != b"":
                    with open("message_file.txt", "a") as file:
                        date = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        msg = f"{date}: {data.decode('utf-8')} \n"
                        file.write(msg)
                else:
                    print("client lost connection")
                    break

#         data = connection.recv(5)
#         while len(data) < 5:
#             new = connection.recv(5 - len(data))
#             data += new
#             if new == b"":
#                 print("client connection lost")
#
#         TYPE = data[0]
#         LENGHT = int.from_bytes(data[1:5], "little")
#
#         PAYLOAD = connection.recv(LENGHT)
#         while len(PAYLOAD) < LENGHT:
#             PAYLOAD_CONTINUE = connection.recv(LENGHT - len(PAYLOAD))
#             if PAYLOAD_CONTINUE == b"":
#                 print("client connection lost")
#                 break
#             else:
#                 PAYLOAD += PAYLOAD_CONTINUE
#
