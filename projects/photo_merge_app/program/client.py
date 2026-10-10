import json
import sys
import os
import importlib.util
import socket
import hashlib
from pathlib import Path

# TODO :
# ADD SOME COMMENTS TO SEE PROCESS OF type_2 & type_4 
# ADD 10 PICTURES TO TEST SYNC PROCESS 



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
type_4 = b"\x04"  # TRANSFER PICS DICT  

# STATUS CODES RECEIVE:
STATUS_CODE_RECEIVE = {
    b"\xc8": "OK",
    b"\xc9": "ERROR",
    b'\xdd': "AUTH_ERROR",
    b'\xdc': "AUTH_OK"
}
STATUS_CODE_SEND = {
    "OK": b"\xc8",
    "ERROR": b"\xc9",
    "AUTH_ERROR": b'\xdd',
    "AUTH_OK": b'\xdc'
}


# creds for auth:
credentials_dict = {
        "login": "admin",
        "password_hash": '$2b$12$4e6t9p17R7.IJ5LK6fJl5.zbUtmEXrNfUZ3oIpKfftoqWZpuHtmoW'
        }


# MAKE CONNECTION TO SERVER
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

# ------------------------------------ functions -----------------------------------

def create_payload(PROTOCOL: bytes, item) -> bytes:
    if PROTOCOL == type_1:
        DATA = item.encode("utf-8")
    elif PROTOCOL == type_2:
        file_name = item['abs_path'].name.encode("utf-8")
        file_name_len = len(file_name).to_bytes(2,'little')
        with open(item["abs_path"], "rb") as pic:
            DATA = pic.read()
        return PROTOCOL + file_name_len + file_name + len(DATA).to_bytes(4,'little') + DATA
    elif PROTOCOL == type_3:
        DATA = item.encode('utf-8')
    elif PROTOCOL == type_4:
        DATA = item.encode('utf-8') 
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

def status_code_receive() -> str:
    status = receive_exactly(client,1) 
    if status != b'':
        return f"{STATUS_CODE_RECEIVE[status]}"
    else:
        return f"Status code not received"

def monitor_pics(PATH=Path("/home/vscode/lab/projects/photo_merge_app/program/test_dir/")) :
    
    while not PATH.is_dir():
        PATH = Path(input("Dir path to monitor: "))

    monitorable_objects = {}

    for i in PATH.iterdir():
        if i.is_file():

            # create object
            name = i.name
             
            path_file = i.absolute()
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

# CHOICE MENU:
while True:
    
    print("Choices: (1 message) (2 update_picture) (3 auth) ")
    choice = int(input("What are you going to do: (takes-int) "))
    
    while choice == 1:
        message = input("Insert message for server to write: \n")
        PAYLOAD = create_payload(type_1, message)
        status = send_exactly(client, PAYLOAD, len(PAYLOAD))
        if status == True:
            print(status_code_receive())
        elif status == False:
            print("Status code not received")

        print("1 = yes, 2 = no ")
        inner_choice = int(input("Communication over?"))
        if inner_choice == 1:
            break
        elif inner_choice == 2:
            pass


    while choice == 2:
        local_pic_dict = monitor_pics()
        json_list = json.dumps(local_pic_dict)
        
        # change protocol 
        PAYLOAD = create_payload(type_4,json_list)

        send_exactly(client,PAYLOAD,len(PAYLOAD))
        print(status_code_receive())
        
        # recive list of pictures to upload
        frame = receive_exactly(client,5)
        if frame == b"":
            print("server lost connection")
            break
        else:
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
            
    if choice == 3:
        
        PAYLOAD = authenticate_client(credentials_dict)
        status = send_exactly(client,PAYLOAD,len(PAYLOAD))
        if status == True:
            print(status_code_receive())
        else:
            print("AUTH_DATA NOT SENT")

    while choice == 4:
        for counter, name in enumerate(to_upload_json, start=1):
            print(f"File {counter}/{len(to_upload_json)}: {name}")

            # send files that digest is exactly the same localy and while were send to server
            if name in local_pic_dict and local_pic_dict[name]["sha256"] == to_upload_json[name]["sha256"]:
                PAYLOAD = create_payload(type_2,local_pic_dict[name])
                if send_exactly(client,PAYLOAD,len(PAYLOAD)) == True:
                    print(status_code_receive())
                else:
                    print(status_code_receive())
        
