import json
import socket
import os
import subprocess 
from datetime import datetime
from time import sleep
from pathlib import Path
import hashlib

from python3.modules.socket.client import send_status_code
# ----------------------------- local_DB ---------------------------------
db = subprocess.Popen(
        ['python3', 'local_db.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
        )


# -------------------------------- start of TCP --------------------------------------

monitorable_objects = {}

# TODO LIST:
# - name assignment for files saved to server [client send it from his own file name / change name a bit ( security ) / save it somewhere ]
# - could add some more options on db managment 
# - add logging to the app 
# - insted of TCP change to TLS

# ┌──────────┬──────────────┬──────────────────────┐
# │ TYPE     │ LENGTH       │ PAYLOAD              │
# │ 1 byte   │ 4 bytes      │ LENGTH bytes         │
# └──────────┴──────────────┴──────────────────────┘

# 0x01      MESSAGE
# 0x02      PICTURE SEND
# 0x03      AUTH

# STATUS CODES ( bland not taken yet )
# 200 : c8 : OK
# 201 : c9 : ERROR
# 202 : ca
# 203 : cb
# 204 : cc
# 205 : cd
# 206 : ce
# 207 : cf
# 208 : d0
# 209 : d1
# 210 : d2
# 211 : d3
# 212 : d4
# 213 : d5
# 214 : d6
# 215 : d7
# 216 : d8
# 217 : d9
# 218 : da
# 219 : db
# 220 : dc : AUTH OK
# 221 : dd : AUTH ERROR
# 222 : de
# 223 : df
# 224 : e0
# 225 : e1
# 226 : e2
# 227 : e3
# 228 : e4
# 229 : e5

# path to save files to, from env variables or ask user for that
def setup_path(env_var: str = "p_sync_path" ) -> str :
    path = os.getenv(env_var, "./photo_sync/files" )
    try:
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
    except OSError :
        print("cannot create dir for pictures")
        raise

    return path

def monitor_pics(PATH: Path, monitorable_objects: dict) :

    for i in PATH.iterdir():
        if i.is_file():

            # create object
            name = i.name
            path_file = str(i.absolute())
            stat_file = i.stat(follow_symlinks=False)
            size = stat_file.st_size
            m_time = stat_file.st_mtime
            
            with open(i,"rb") as f:
                hash_object = hashlib.sha256(f.read())     # cut in parts for better performance
            digest = hash_object.hexdigest()

            monitorable_objects[name] = {
                "abs_path": path_file,
                "size": size,
                "m_time": m_time,
                "sha256": digest,
            }

        else:
            print(f'{i} not directory, not included into monitoring')

    return monitorable_objects


class Server:
    def __init__(self):
        self.files_path = setup_path()

my_server = Server()
monitorable_objects = monitor_pics(Path(my_server.files_path),monitorable_objects)


STATUS_CODE_DICT ={
    'OK': b"\xc8",
    'ERROR': b'\xc9',
    'AUTH_ERROR': b'\xdd',
    'AUTH_OK': b'\xdc'
}

class Client:
    def __init__(self,client,client_address,authenticated=False,login_client="",password_client="",auth_tries=0):
        self.client = client
        self.client_address = client_address
        self.authenticated = authenticated
        self.login_client = login_client
        self.password_client = password_client
        self.auth_tries= auth_tries



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
            return b""
        else:
            return frame

    except socket.timeout:
        print(f"{address_client} exceed 30s idle state while in operation mode")
        CONNECTION.close()
        return b""
        # should add loggin instead of priting

def send_exactly(CONNECTION, PAYLOAD: bytes, MSG_LENGTH: int) -> bool:
    if len(PAYLOAD) != MSG_LENGTH:
        return False

    try:
        CONNECTION.sendall(PAYLOAD)
        return True
    except OSError:
        return False

def status_code_send(CONNECTION,STATUS_CODE) -> bool:
    STATUS = STATUS_CODE_DICT[STATUS_CODE]
    if send_exactly(CONNECTION, STATUS, 1) == True:
        return True
    else:
        print('status code not send')
        return False

def status_code_receive():
    pass

# DAEMON OPTIONS:
while True:
    connection, client_address = server.accept()
    connection = Client(connection,client_address)
    connection.client.settimeout(30)

    while True:

        frame = receive_exactly(connection.client, 5, connection.client_address)
        if frame == b"":
            print("client lost connection")
            break

        match frame[0]:
            case 0x01:
                if connection.authenticated != True:
                    connection.client.close()

                LENGTH = int.from_bytes(frame[1:5], "little")
                frame = receive_exactly(connection.client, LENGTH, connection.client_address)
                
                if frame != b"":
                    try:
                        with open("message_file.txt", "a") as file:
                            date_time = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            msg = f"{date_time}: {frame.decode('utf-8')} \n"
                            file.write(msg)
                            status_code_send(connection.client,"OK")
                    except:
                        status_code_send(connection.client,"ERROR")
                else:
                    status_code_send(connection.client,"ERROR")
                    break

            case 0x02:

                if connection.authenticated != True:
                    connection.client.close()
                LENGTH = int.from_bytes(frame[1:5], "little")
                PAYLOAD = receive_exactly(connection.client, LENGTH, connection.client_address)
                if PAYLOAD == b'':
                    send_status_code(connection.client,"ERROR")
                else:
                    send_status_code(connection.client,"OK")

                PAYLOAD_STRING = PAYLOAD.decode('utf-8')
                remote_list = json.loads(PAYLOAD_STRING)
                
                to_request = {}
                
                for name in remote_list:
                    if name not in monitorable_objects:
                        to_request[name] = remote_list[name]
                    elif name in monitorable_objects.keys() and monitorable_objects[name]["sha256"] != remote_list[name]["sha256"]:
                        to_request[name] = remote_list[name]
                    else: 
                        pass



                           
            case 0x03:
                if connection.auth_tries >= 2:
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
                        status_code_send(connection.client,"AUTH_OK")
                        connection.authenticated = True
                    else:
                        status_code_send(connection.client,"AUTH_ERROR")
                        print(f"{connection.client_address} failed AUTH") # LOGGING 
                        connection.auth_tries += 1 


