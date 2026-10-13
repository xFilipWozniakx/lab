import json
import socket
import os
import subprocess 
import hashlib
import ssl 

from datetime import datetime
from time import sleep
from pathlib import Path

# ----------------------------- local_DB ---------------------------------
db = subprocess.Popen(
        ['python3', 'local_db.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )


# -------------------------------- start of TCP --------------------------------------

monitorable_objects = {}

def infos():
# TODO LIST:


# - max picture size ~ 20 000 000 bytes
# - could add some more options on db managment 
# - some kind of admin interface to talk to 
# - multi users ? hmm 
# - dig into android apps to translate client to
# - 

#                    type_3 & type_2 & type_1 
# ┌──────────┬──────────────┬──────────────────────┐
# │ TYPE     │ LENGTH       │ PAYLOAD              │
# │ 1 byte   │ 4 bytes      │ LENGTH bytes         │
# └──────────┴──────────────┴──────────────────────┘


#                                  type_4
# ┌──────────┬──────────────┬──────────────┬──────────────────┬──────────────────┐
# │ TYPE     │ NAME LENGTH  │ NAME PAYLOAD │ PAYLOAD LENGTH   │      PAYLOAD     │
# │ 1 byte   │ 2 bytes      │ NAME (bytes) │      4 BYTES     │    FILE PAYLOAD  │
# └──────────┴──────────────┴──────────────┴──────────────────┴──────────────────┘

# 0x01      MESSAGE
# 0x02      PICTURE SEND
# 0x03      AUTH
# 0x04      PICUTRES REQUEST


    pass

def add_logs(msg,*args) -> str:
    da =datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    msg = f'{da}: {msg} {" ".join(args)}\n'
    return msg

def setup_logging(PATH_LOGS) -> str: 
    logs = Path(os.path.join(PATH_LOGS, "logs.txt"))
    try:
        with open(logs, 'a') as logs:
            logs.write(add_logs("Server start-up"))
    except OSError:
        print(f"Cannot create log_file at {PATH_LOGS}")
    return str(logs)

def from_bytes_x(nbytes, unit='B'):
    units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
    return nbytes / units[unit]

def setup_path(env_var: str = "p_sync_path") -> tuple[str,str,int]:

# max_file_size = ~20MB
# chage with mlf 

# path to save files to
# to change its path set environment variable accordinly 
# p_sync_path="/my/excelent/path"

    path = os.getenv(env_var, "./photo_sync")
    path_logs = os.path.join(path, "logs")
    path_files = os.path.join(path, "files")
    path_certs = os.path.join(path, "certs")

    try:
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        if not os.path.isdir(path_files):
            os.makedirs(path_files, exist_ok=True)
        if not os.path.isdir(path_logs):
            os.makedirs(path_logs, exist_ok=True)
        if not os.path.isdir(path_certs):
            os.makedirs(path_certs, exist_ok=True)

    except OSError:
        print("cannot server dirs")
        raise
    return os.path.abspath(path_files), os.path.abspath(path_logs), int(os.getenv("mfs", 20000000))

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

path_files, path_logs, max_file_length = setup_path()

class Server:
    def __init__(self,path_files, path_logs,max_file_length):
        self.files_path: str = path_files
        self.logs_path: str = path_logs
        self.logs_write_to: str = setup_logging(self.logs_path)
        self.max_file_length = max_file_length

my_server = Server(path_files, path_logs, max_file_length)
monitorable_objects = monitor_pics(Path(my_server.files_path),monitorable_objects)

add_logs(f"Number of files in monitored area:  {len(monitorable_objects)}")

# status codes
STATUS_CODE_SEND ={
    'OK': b"\xc8",
    'ERROR': b'\xc9',
    'AUTH_OK': b'\xdc',
    'AUTH_ERROR': b'\xdd',
    'SIZE_ERROR': b'\xde',
    'SIZE_ACK': b'\xdf',
    "SUCCES_RECEIVED": b'\xe0',
}

STATUS_CODE_RECEIVE = {
    b"\xc8": "OK",
    b"\xc9": "ERROR",
    b'\xdc': "AUTH_OK",
    b'\xdd': "AUTH_ERROR",
    b'\xde': "SIZE_ERROR",
    b'\xdf': 'SIZE_ACK',
    b'\xe0': "SUCCES_RECEIVED",
}

TYPE_PROT = {
    0x02: b"\x02",
}

class Client:
    def __init__(self,client,client_address,authenticated=False,login_client="",password_client="",auth_tries=0):
        self.client = client
        self.client_address = client_address
        self.authenticated = authenticated
        self.login_client = login_client
        self.password_client = password_client
        self.auth_tries= auth_tries

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("./photo_sync/certs/example.crt", "./photo_sync/certs/example.key")
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
    STATUS = STATUS_CODE_SEND[STATUS_CODE]
    if send_exactly(CONNECTION, STATUS, 1) == True:
        return True
    else:
        print('status code not send')
        return False

def status_code_receive(CONNECTION,CONNECTION_ADDR):
    status = receive_exactly(CONNECTION,1,CONNECTION_ADDR) 
    if status != b'':
        return f"{STATUS_CODE_RECEIVE[status]}"
    else:
        return f"Status code not received"

def request_files_from_client(CONNECTION,TO_REQUEST,CLIENT_ADDRESS):
    PAYLOAD =json.dumps(TO_REQUEST).encode('utf-8')
    if send_exactly(CONNECTION,PAYLOAD,len(PAYLOAD)) == False:
        print(status_code_receive(CONNECTION,CLIENT_ADDRESS))
    else:
        print(status_code_receive(CONNECTION,CLIENT_ADDRESS))

def create_payload(TYPE,DATA) -> bytes:
    if TYPE == 0x02:
        DATA = DATA.encode('utf-8')
        LENGTH = len(DATA).to_bytes(4,'little')
    
    return TYPE_PROT[0x02] + LENGTH + DATA 
        
# DAEMON:
while True:
    raw_client, client_address = server.accept()
    try:
        secure_client = context.wrap_socket(raw_client, server_side=True)
        connection = Client(secure_client,client_address)
        print(f"TLS established: {secure_client.version()}")
        connection.client.settimeout(30)

    except ssl.SSLError as exc:
        print(f"TLS handshake failed for {client_address}: {exc}")
        raw_client.close()
        continue

    while True:
        
        frame = receive_exactly(connection.client, 1, connection.client_address)
        if frame == b"":
            print("client lost connection")
            break

        match frame[0]:
            case 0x01:
                if connection.authenticated != True:
                    connection.client.close()
                    continue
                
                frame = receive_exactly(connection.client,4, connection.client_address)
                if frame == b'':
                    print("client lost connection or sent malufactured bytes")
                else:    
                    LENGTH = int.from_bytes(frame, "little")
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
                    continue

                frame = receive_exactly(connection.client,4, connection.client_address)
                if frame == b'':
                    status_code_send(connection.client,"ERROR")
                    print("client lost connection or sent malufactured bytes")
                else:    
                    LENGTH = int.from_bytes(frame, "little")
                    PAYLOAD = receive_exactly(connection.client, LENGTH, connection.client_address)
                    status_code_send(connection.client,"OK")

                    PAYLOAD_STRING = PAYLOAD.decode('utf-8')
                    remote_list = json.loads(PAYLOAD_STRING)
                    print("remote list loaded")
                
                to_request = {}
                # create list of missing photos
                for name in remote_list:
                    if name not in monitorable_objects:
                        to_request[name] = remote_list[name]
                    elif name in monitorable_objects.keys() and monitorable_objects[name]["sha256"] != remote_list[name]["sha256"]:
                        to_request[name] = remote_list[name]
                    else: 
                        pass
                print("to_request dict created")

                to_request_payload = create_payload(0x02,json.dumps(to_request))

                print("to request json dumped and utf-8 encoded")

                if send_exactly(connection.client,to_request_payload,len(to_request_payload)) == False:
                    print("to_request_payload didnt reach destination")
                else:
                    print(status_code_receive(connection.client,connection.client_address))

            case 0x03:
                if connection.auth_tries >= 2:
                    connection.client.close()
                    continue

                elif connection.authenticated == True:
                    print("Already authenticated")
                    status_code_send(connection.client,"AUTH_OK")
                    continue 

                frame = receive_exactly(connection.client,4, connection.client_address)
                if frame == b'':
                    print("client lost connection or sent malufactured bytes")
                else:    
                    LENGTH = int.from_bytes(frame, "little")
                    frame = receive_exactly(connection.client, LENGTH, connection.client_address)
                    PAYLOAD = frame.decode('utf-8')
                    json_object = json.loads(PAYLOAD)
                    login = json_object["login"]
                    password = json_object["password_hash"]

                if PAYLOAD == b'':
                    print("malformed data sent")
                else:

                    auth_data = f'AUTH|{login}|{password}\n'

                    db.stdin.write(auth_data)
                    db.stdin.flush()
                    
                    # auth_status 
                    output_db =  db.stdout.read()
                    print(output_db)

                    



#                     if auth_status == b'\xc8':
#                         status_code_send(connection.client,"AUTH_OK")
#                         connection.authenticated = True
#                     else:
#                         status_code_send(connection.client,"AUTH_ERROR")
#                         print(f"{connection.client_address} failed AUTH") # LOGGING 
#                         connection.auth_tries += 1 
            case 0x04:
                if connection.authenticated != True:
                    connection.client.close()
                    continue
                
                # receive length of name ( OPERATION | LEN_NAME 2b | NAME  | PAYLOAD_LEN 4b | PAYLOAD )
                LENGTH_NAME = receive_exactly(connection.client,2, connection.client_address)
                if LENGTH_NAME == b'':
                    print("client lost connection or sent malufactured bytes")
                else:
                    status_code_send(connection.client,"OK")
    
            case 0x05:
                if connection.authenticated != True:
                    connection.client.close()
                    continue
                LENGTH_NAME_INT = int.from_bytes(LENGTH_NAME, "little")
                NAME = receive_exactly(connection.client, LENGTH_NAME_INT, connection.client_address)
                if NAME != b'':
                    print("client lost connection or sent malufactured bytes")
                else:
                    status_code_send(connection.client,"OK")

            case 0x06:
                if connection.authenticated != True:
                    connection.client.close()
                    continue

                LENGTH_FILE_BYTES = receive_exactly(connection.client,4,connection.client_address)
                LENGTH_FILE = int.from_bytes(LENGTH_FILE_BYTES,'little')
                if LENGTH_FILE > my_server.max_file_length:
                    # CONTROLING SIZE OF FILE NEEDED 
                    if status_code_send(connection.client,"FILE_SIZE") == True:
                        status_code_receive(connection.client,connection.client_address)
                        add_logs(f"{NAME.decode("utf-8")} exceed allowed {from_bytes_x(int(my_server.max_file_length),"MB")} file size")
                        continue
            
            case 0x07:
                if connection.authenticated != True:
                    connection.client.close()
                    continue

                    FILE = receive_exactly(connection.client,LENGTH_FILE,connection.client_address)
                    if len(FILE) == LENGTH_FILE:
                        srv_path = my_server.files_path
                        save_path = os.path.join(srv_path, NAME.decode('utf-8'))
                        with open(save_path,'wb') as sync:
                            sync.write(FILE)
                        status_code_send(connection.client, "SUCCES_RECEIVED")

