import json
import socket
import os
import subprocess 
from datetime import datetime
from time import sleep
# ----------------------------- local_DB ---------------------------------
db = subprocess.Popen(
        ['python3', 'local_db.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
        )


# -------------------------------- start of TCP --------------------------------------
# 0x01      MESSAGE
# 0x02      PICTURE SEND
# 0x10      VALIDATE_DATA_WITH_SOURCE

# STATUS CODES
# 200 : c8 : OK
# 201 : c9 : ERROR
# 202 : ca
# 203 : cb

STATUS_CODE_DICT = {
    b"\xc8": b"OK",
    b"\xc9": b"ERROR"
}

class Client:
    def __init__(self,client,client_address,authenticated=False,login_client="",password_client=""):
        self.client = client
        self.client_address = client_address
        self.authenticated = authenticated
        self.login_client = login_client
        self.password_client = password_client

# ┌──────────┬──────────────┬──────────────────────┐
# │ TYPE     │ LENGTH       │ PAYLOAD              │
# │ 1 byte   │ 4 bytes      │ LENGTH bytes        │
# └──────────┴──────────────┴──────────────────────┘

# LOGGING 
# NOT DONE YET
def logging(text):
    with open("access_log.txt", "a") as logging:
        date_time = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        logging.write(date_time,text)


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


# do usuniecia
def AUTH_PROCESS(connection,LENGTH,address_client):
    frame = receive_exactly(connection,5,address_client)
    
    if frame == b'':
        print(f"{address_client} client lost connection")
        logging(f"{address_client} client lost connection")
    elif frame[0] == 0x03:
        LENGTH = int.from_bytes(frame[1:5], "little")
        frame = receive_exactly(connection, LENGTH, address_client)
        
def validate_with_database(LOGIN,PASSWORD,db) -> bool:

    db.stdin.write(f"AUTH|{LOGIN}|{PASSWORD}\n")
    db.stdin.flush()
    response = db.stdout.readline()
    if response == "AUTH_OK":
        return True
    else:
        return False

while True:
    connection, client_address = server.accept()
    connection = Client(connection,client_address)
    connection.client.settimeout(30)


    # where connection = local address / address_client = remote address
    #client_connection = f"{date_time} connected: {connection.client_address}"
    #print(f'{client_connection}')
    #logging(client_connection)

    while True:
        auth_counter = 0


        frame = receive_exactly(connection.client, 5, connection.client_address)
        if frame == b"":
            print("client lost connection")
            break

        match frame[0]:
            case 0x01:

                LENGTH = int.from_bytes(frame[1:5], "little")
                frame = receive_exactly(connection.client, LENGTH, connection.client_address)
                if frame != b"":
                    STATUS_CODE = b"\x00"
                    try:
                        with open("message_file.txt", "a") as file:
                            date_time = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            msg = f"{date_time}: {frame.decode('utf-8')} \n"
                            file.write(msg)

                            STATUS_CODE = b"\xc8"

                    except:
                        # any kind of error
                        STATUS_CODE = b"\xc9"
                    finally:
                        # will need to make some proper logging and status codes sending
                        if send_status_code(connection.client, STATUS_CODE) == True:
                            #print(f"{address_client} received status code")
                            pass
                        else:
                            pass
                            #print(f"{address_client} didnt receive status code")

                else:
                    print("client lost connection")
                    break

            case 0x02:
                LENGTH = int.from_bytes(frame[1:5], "little")
                frame = receive_exactly(connection.client, LENGTH, connection.client_address)
                if frame != b"":
                    path_for_pics = (
                        "/home/vscode/lab/python3/modules/socket/dest_pictures/"
                    )

                    # need to make different system for naming
                    # but for now doesnt matter untill i do my sync modules
                    # photos will inherit name from their original 
                    with open(f"{path_for_pics}cat_pic.webp", "wb") as file:
                        file.write(frame)

                    send_status_code(connection.client, STATUS_CODE=b'\xc8')


                else:
                    send_status_code(connection.client, STATUS_CODE=b'\xc9')
                    break
            
            case 0x03:
                if auth_counter >= 3:
                    connection.client.close()

                LENGTH = int.from_bytes(frame[1:5], "little")
                PAYLOAD = receive_exactly(connection.client, LENGTH, connection.client_address)

                PAYLOAD = PAYLOAD.decode('utf-8')
                json_object = json.loads(PAYLOAD)
                login = json_object["login"]
                password = json_object["password_hash"]

                if PAYLOAD == b'':
                    print("malformed data sent")
                else:

                    auth_data = f'AUTH|{login}|{password}\n'
                    
                    db.stdin.write(auth_data)
                    db.stdin.flush()
                    
                    auth_status = db.stdout.buffer.read(1)

                    if auth_status == b'\xc8':
                        connection.authenticated = True
                        send_status_code(connection.client,STATUS_CODE[b"\xc8"])
                    else:
                        send_status_code(connection.client,STATUS_CODE[b"\xc9"])
                        auth_counter += 1 



                    
