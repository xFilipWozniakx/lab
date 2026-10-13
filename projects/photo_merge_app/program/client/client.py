import json
import sys
import os
import importlib.util
import socket
import hashlib
import ssl 

from datetime import datetime 
from pathlib import Path




# TODO:
#

# PROTOCOLS:
type_1 = b"\x01"  # MESSAGE
type_2 = b"\x02"  # PICTURE_UPDATE
type_3 = b"\x03"  # AUTHENTICATE
type_4 = b"\x04"  # TRANSFER PICS: STAGE 1 
type_5 = b"\x05"  # TRANSFER PICS: STAGE 2
type_6 = b"\x06"  # TRANSFER PICS: STAGE 3
type_7 = b"\x07"  # TRANSFER PICS: STAGE 4


# FIX STATUS CODES BEFORE RUNNING 
# STATUS CODES RECEIVE:
STATUS_CODE_RECEIVE = {
    b"\xc8": "OK",
    b"\xc9": "ERROR",
    b'\xdc': "AUTH_OK",
    b'\xdd': "AUTH_ERROR",
    b'\xde': "SIZE_ERROR",
    b'\xdf': 'SIZE_ACK',
    b'\xe0': "STATUS_CODE_RECEIVED",
}
STATUS_CODE_SEND = {
    "OK": b"\xc8",
    "ERROR": b"\xc9",
    "AUTH_ERROR": b'\xdd',
    "SIZE_ERROR": b'\xde',
    "AUTH_OK": b'\xdf',
    "SIZE_ACK": b'\xe0' ,
    "STATUS_CODE_RECEIVED": b'\xe1',
}


# creds for auth:
credentials_dict = {
        "login": "admin",
        "password_hash": '$2b$12$4e6t9p17R7.IJ5LK6fJl5.zbUtmEXrNfUZ3oIpKfftoqWZpuHtmoW'
        }

class Client:
    def __init__(self,logs_path):
        self.logs = logs_path



# -------------- logs ------------

def add_logs(msg,*args) -> str:
    da =datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    msg = f'{da}: {msg} {" ".join(args)}\n'
    return msg

def setup_logging(PATH_LOGS) -> str: 
    logs = Path(os.path.join(PATH_LOGS, "logs.txt"))
    try:
        logs = open(logs, 'x')
        logs.close()
    except OSError:
        print(f"Cannot create log_file at {PATH_LOGS}")
    return str(logs)

# ------------------------------------ functions -----------------------------------

def create_payload(PROTOCOL: bytes, item) -> bytes:
    if PROTOCOL == type_1:
        DATA = item.encode("utf-8")
    elif PROTOCOL == type_2:
        DATA = item.encode('utf-8') 
    elif PROTOCOL == type_3:
        DATA = item.encode('utf-8')
    elif PROTOCOL == type_4:
        # STAGE 1:
        file_name = item['abs_path'].split("/")[-1].encode('utf-8')
        file_name_len = len(file_name).to_bytes(2,'little')
        return type_4 + file_name_len
    elif PROTOCOL == type_5:
        # STAGE 2:
        file_name = item['abs_path'].split("/")[-1].encode('utf-8')
        return type_5 + file_name
    elif PROTOCOL == type_6:
        photo = Path(item['abs_path'])
        size = photo.stat().st_size
        return size.to_bytes(4,'little')
    elif PROTOCOL == type_7:
        CHUNK_SIZE = 64 * 1024
        with open(item, "rb") as pic:
            while chunk := pic.read(CHUNK_SIZE):
                if send_exactly(client,chunk,len(chunk).to_bytes(4,'little')) == False:
                    add_logs(f"connection killed under sending {item[name]}")
        add_logs(status_code_receive(client), f" {item[name]}")
    else:
        raise ValueError("Unknown protocol type")
    
    return PROTOCOL + len(DATA).to_bytes(4, "little") + DATA

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
    if len(PAYLOAD) != MSG_LENGTH:
        return False

    try:
        CONNECTION.sendall(PAYLOAD)
        return True
    except OSError:
        return False

def authenticate_client(credential_dict):
    # add password hashing before sending 
    creds_json = json.dumps(credential_dict)
    return create_payload(type_3,creds_json)

def status_code_send(CONNECTION,STATUS_CODE) -> bool:
    STATUS = STATUS_CODE_SEND[STATUS_CODE]
    if send_exactly(CONNECTION, STATUS, 1) == True:
        return True
    else:
        print('status code not send')
        return False

def status_code_receive(CONNECTION) -> str:
    status = receive_exactly(CONNECTION,1) 
    if status != b'':
        return f"{STATUS_CODE_RECEIVE[status]}"
    else:
        return f"Status code not received"

def monitor_pics(pa: Path):
    monitorable_objects = {}
    for i in pa.iterdir():
        if i.is_file():

            # create object
            name =  i.name
            path_file = str(pa.joinpath(i.name)) 
            stat_file = i.stat(follow_symlinks=False)
            size = stat_file.st_size
            m_time = stat_file.st_mtime
            
            with open(path_file,"rb") as f:
                hash_object = hashlib.sha256(f.read())     # cut in parts for better performance
            digest = hash_object.hexdigest()

            monitorable_objects[name] = {
                "abs_path": path_file,
                "size": size,
                "m_time": m_time,
                "sha256": digest
            }

        else:
            print(f'{i} not directory, not included into monitoring')
    return monitorable_objects

## MAKE CONNECTION TO SERVER
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = "127.0.0.1"
context = ssl.create_default_context(cafile="../server/photo_sync/certs/example.crt")

with socket.create_connection(((hostname,5555))) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as client:
        print(client.version())

# CHOICE MENU:
        while True:
            print("Choices: (1 message) (2 update_picture) (3 auth) ")
            choice = int(input("What are you going to do: (takes-int) "))
            
            while choice == 1:
                message = input("Insert message for server to write: \n")
                PAYLOAD = create_payload(type_1, message)
                status = send_exactly(client, PAYLOAD, len(PAYLOAD))
                if status == True:
                    print(status_code_receive(client))
                elif status == False:
                    print("Status code not received")

                print("1 = yes, 2 = no ")
                inner_choice = int(input("Communication over?"))
                if inner_choice == 1:
                    break
                elif inner_choice == 2:
                    pass


            while choice == 2:
                local_pic_dict = monitor_pics(Path('/home/vscode/lab/projects/photo_merge_app/program/photos/photos')
        )
                print("local_pic_dict recived in choice = 2 ")
                json_list = json.dumps(local_pic_dict)
                print("local_pic_dict dumped")
                # change protocol 
                PAYLOAD = create_payload(type_2,json_list)
                print("local_pic encapsulated in payload")
                send_exactly(client,PAYLOAD,len(PAYLOAD))
                print(status_code_receive(client))
                
                # recive list of pictures to upload
                frame = receive_exactly(client,5)
                if frame == b"":
                    print("server lost connection")
                    break
                elif frame[0] == 0x02:
                    LENGTH = int.from_bytes(frame[1:5], "little")
                    frame = receive_exactly(client, LENGTH)
                    # mix in status code
                    global to_upload_json 
                    to_upload = frame.decode("utf-8")
                    to_upload_json = json.loads(to_upload)
                    print(to_upload)
                    print(type(to_upload))
                    status_code_send(client,"OK")
                    choice= 4
                else:
                    print("wrong procotol in-sent")
                                
            if choice == 3:
                
                PAYLOAD = authenticate_client(credentials_dict)
                status = send_exactly(client,PAYLOAD,len(PAYLOAD))
                if status == True:
                    print(status_code_receive(client))
                else:
                    print("AUTH_DATA NOT SENT")

            while choice == 4:
                for counter, name in enumerate(to_upload_json, start=1):
                    print(f"File {counter}/{len(to_upload_json)}: {name}")

                    # send files that digest is exactly the same localy and while were send to server
                    if name in local_pic_dict and local_pic_dict[name]["sha256"] == to_upload_json[name]["sha256"]:
                        LEN_NAME  = create_payload(type_4,to_upload_json[name])
                        if send_exactly(client,LEN_NAME,3) == True:
                            print(status_code_receive(client))
                            NAME = create_payload(type_5, to_upload_json[name])
                            if send_exactly(client,NAME,int(LEN_NAME)) == True:
                                print(status_code_receive(client))
                                FILE_LEN = create_payload(type_6,to_upload_json[name])
                                if send_exactly(client,FILE_LEN,4) == True:
                                    if status_code_receive(client) == "SIZE_ERROR":
                                        add_logs(f"file: {to_upload_json[name]} exceeded server max size restriction")
                                        status_code_send(client,"SIZE_ACK")
                                        print("SIZE ERROR ACKNOWLEDGED")
                                else:
                                    create_payload(type_7,to_upload_json[name].abs_path)


                choice = 0 








