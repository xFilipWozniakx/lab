import json
import socket
import os
import subprocess
import hashlib
import ssl
import tempfile

from datetime import datetime
from pathlib import Path

# ----------------------------- local_DB ---------------------------------
db = subprocess.Popen(
    ["python3", "local_db.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
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


def add_logs(msg, *args) -> None:
    da = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    msg = f"{da}: {msg} {' '.join(args)}\n"
    with open(my_server.logs_write_to, "a") as write_logs:
        write_logs.write(msg)


def setup_logging(PATH_LOGS) -> str:
    logs = Path(os.path.join(PATH_LOGS, "logs.txt"))
    return str(logs)


def from_bytes_x(nbytes, unit="B"):
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    return nbytes / units[unit]


def setup_path(env_var: str = "p_sync_path") -> tuple[str, str, int]:

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
    return (
        os.path.abspath(path_files),
        os.path.abspath(path_logs),
        int(os.getenv("mfs", 20000000)),
    )


def monitor_pics(PATH: Path, monitorable_objects: dict):
    # Scan recursively so files selected from different phone folders can keep
    # their relative paths instead of colliding when their basenames are equal.
    for i in PATH.rglob("*"):
        if i.is_file():
            name = i.relative_to(PATH).as_posix()
            path_file = str(i.absolute())
            stat_file = i.stat(follow_symlinks=False)
            size = stat_file.st_size
            m_time = stat_file.st_mtime

            # Hash in chunks to avoid reading an entire large file into memory.
            hash_object = hashlib.sha256()
            with open(i, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    hash_object.update(chunk)

            monitorable_objects[name] = {
                "abs_path": path_file,
                "size": size,
                "m_time": m_time,
                "sha256": hash_object.hexdigest(),
            }

    return monitorable_objects


path_files, path_logs, max_file_length = setup_path()
logs_write_to = setup_logging(path_logs)


class Server:
    def __init__(self, path_files, path_logs, max_file_length):
        self.files_path: str = path_files
        self.logs_path: str = path_logs
        self.logs_write_to: str = logs_write_to
        self.max_file_length = max_file_length


my_server = Server(path_files, path_logs, max_file_length)
monitorable_objects = monitor_pics(Path(my_server.files_path), monitorable_objects)

add_logs(f"Server instance started")
add_logs(f"Number of files in monitored area:  {len(monitorable_objects)}")


def refresh_monitor():
    # Refresh the index before each comparison so newly uploaded files are not
    # requested again during the next synchronization.
    monitorable_objects.clear()
    monitor_pics(Path(my_server.files_path), monitorable_objects)


def get_safe_destination(relative_name: str) -> Path:
    # Reject absolute paths and traversal components supplied by a remote client.
    relative_path = Path(relative_name)
    if (
        relative_path.is_absolute()
        or not relative_path.parts
        or any(part in (".", "..") for part in relative_path.parts)
    ):
        raise ValueError("Invalid relative file path")
    root = Path(my_server.files_path).resolve()
    destination = (root / relative_path).resolve()
    if destination != root and root not in destination.parents:
        raise ValueError("File path escapes the storage directory")
    return destination


def receive_file_to_disk(connection, size: int, destination: Path) -> bool:
    # Stream incoming bytes to disk instead of buffering the complete photo in RAM.
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb", dir=destination.parent, delete=False
        ) as output:
            temporary_path = Path(output.name)
            remaining = size
            while remaining:
                chunk = receive_exactly(
                    connection.client,
                    min(64 * 1024, remaining),
                    connection.client_address,
                )
                if not chunk:
                    return False
                output.write(chunk)
                remaining -= len(chunk)
        # Replace only the target path after the full transfer has completed.
        os.replace(temporary_path, destination)
        return True
    except OSError as exc:
        print(f"Could not save received file: {exc}")
        return False
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink(missing_ok=True)


# status codes
STATUS_CODE_SEND = {
    "OK": b"\xc8",
    "ERROR": b"\xc9",
    "AUTH_OK": b"\xdc",
    "AUTH_ERROR": b"\xdd",
    "SIZE_ERROR": b"\xde",
    "SIZE_ACK": b"\xdf",
    "SUCCES_RECEIVED": b"\xe0",
}

STATUS_CODE_RECEIVE = {
    b"\xc8": "OK",
    b"\xc9": "ERROR",
    b"\xdc": "AUTH_OK",
    b"\xdd": "AUTH_ERROR",
    b"\xde": "SIZE_ERROR",
    b"\xdf": "SIZE_ACK",
    b"\xe0": "SUCCES_RECEIVED",
}

TYPE_PROT = {
    0x02: b"\x02",
}


class Client:
    def __init__(
        self,
        client,
        client_address,
        authenticated=False,
        login_client="",
        password_client="",
        auth_tries=0,
    ):
        self.client = client
        self.client_address = client_address
        self.authenticated = authenticated
        self.login_client = login_client
        self.password_client = password_client
        self.auth_tries = auth_tries


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    "./photo_sync/certs/server.crt", "./photo_sync/certs/server.key"
)
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


def status_code_send(CONNECTION, STATUS_CODE) -> bool:
    STATUS = STATUS_CODE_SEND[STATUS_CODE]
    if send_exactly(CONNECTION, STATUS, 1) == True:
        return True
    else:
        print("status code not send")
        return False


def status_code_receive(CONNECTION, CONNECTION_ADDR):
    status = receive_exactly(CONNECTION, 1, CONNECTION_ADDR)
    if status != b"":
        return f"{STATUS_CODE_RECEIVE[status]}"
    else:
        return f"Status code not received"


def request_files_from_client(CONNECTION, TO_REQUEST, CLIENT_ADDRESS):
    PAYLOAD = json.dumps(TO_REQUEST).encode("utf-8")
    if send_exactly(CONNECTION, PAYLOAD, len(PAYLOAD)) == False:
        print(status_code_receive(CONNECTION, CLIENT_ADDRESS))
    else:
        print(status_code_receive(CONNECTION, CLIENT_ADDRESS))


def create_payload(TYPE, DATA) -> bytes:
    if TYPE == 0x02:
        DATA = DATA.encode("utf-8")
        LENGTH = len(DATA).to_bytes(4, "little")

    return TYPE_PROT[0x02] + LENGTH + DATA


# DAEMON:
while True:
    raw_client, client_address = server.accept()
    try:
        secure_client = context.wrap_socket(raw_client, server_side=True)
        connection = Client(secure_client, client_address)
        print(f"TLS established: {secure_client.version()}")
        connection.client.settimeout(30)

    except ssl.SSLError as exc:
        print(f"TLS handshake failed for {client_address}: {exc}")
        raw_client.close()
        continue

    # Keep transfer state local to this client; never reuse another client's filename or size.
    LENGTH_NAME = b""
    length_name_int = 0
    NAME = b""
    relative_name = ""
    LENGTH_FILE = 0

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

                frame = receive_exactly(connection.client, 4, connection.client_address)
                if frame == b"":
                    print("client lost connection or sent malufactured bytes")
                else:
                    LENGTH = int.from_bytes(frame, "little")
                    frame = receive_exactly(
                        connection.client, LENGTH, connection.client_address
                    )

                if frame != b"":
                    try:
                        with open("message_file.txt", "a") as file:
                            date_time = (
                                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            )
                            msg = f"{date_time}: {frame.decode('utf-8')} \n"
                            file.write(msg)
                            status_code_send(connection.client, "OK")
                    except:
                        status_code_send(connection.client, "ERROR")
                else:
                    status_code_send(connection.client, "ERROR")
                    break

            case 0x02:
                if not connection.authenticated:
                    connection.client.close()
                    break

                frame = receive_exactly(connection.client, 4, connection.client_address)
                if not frame:
                    status_code_send(connection.client, "ERROR")
                    break
                LENGTH = int.from_bytes(frame, "little")
                PAYLOAD = receive_exactly(
                    connection.client, LENGTH, connection.client_address
                )
                if not PAYLOAD:
                    status_code_send(connection.client, "ERROR")
                    break

                try:
                    remote_list = json.loads(PAYLOAD.decode("utf-8"))
                    if not isinstance(remote_list, dict):
                        raise ValueError("Photo list must be a JSON object")
                except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                    print(f"Invalid photo list from {connection.client_address}: {exc}")
                    status_code_send(connection.client, "ERROR")
                    break

                status_code_send(connection.client, "OK")
                refresh_monitor()
                to_request = {}
                # Compare relative paths and hashes to find missing or changed files.
                for name, metadata in remote_list.items():
                    current = monitorable_objects.get(name)
                    if current is None or current["sha256"] != metadata.get("sha256"):
                        to_request[name] = metadata

                to_request_payload = create_payload(0x02, json.dumps(to_request))
                if not send_exactly(
                    connection.client, to_request_payload, len(to_request_payload)
                ):
                    print("Could not send requested-file list")
                    break
                print(status_code_receive(connection.client, connection.client_address))

            case 0x03:
                if connection.auth_tries >= 2:
                    connection.client.close()
                    break
                if connection.authenticated:
                    status_code_send(connection.client, "AUTH_OK")
                    continue

                length_bytes = receive_exactly(
                    connection.client, 4, connection.client_address
                )
                if not length_bytes:
                    break
                payload_length = int.from_bytes(length_bytes, "little")
                payload = receive_exactly(
                    connection.client, payload_length, connection.client_address
                )
                if not payload:
                    print("Malformed or incomplete authentication payload")
                    status_code_send(connection.client, "AUTH_ERROR")
                    connection.auth_tries += 1
                    continue

                try:
                    json_object = json.loads(payload.decode("utf-8"))
                    login = json_object["login"]
                    password = json_object["password_hash"]
                    if not isinstance(login, str) or not isinstance(password, str):
                        raise ValueError("Login and password hash must be strings")
                except (
                    UnicodeDecodeError,
                    json.JSONDecodeError,
                    KeyError,
                    ValueError,
                ) as exc:
                    print(
                        f"Invalid authentication payload from {connection.client_address}: {exc}"
                    )
                    status_code_send(connection.client, "AUTH_ERROR")
                    connection.auth_tries += 1
                    continue

                # Do not print authentication data because it contains credentials.
                auth_data = f"AUTH|{login}|{password}\n"
                db.stdin.write(auth_data)
                db.stdin.flush()
                auth_status = db.stdout.buffer.read(1)

                if auth_status == b"\xdc":
                    status_code_send(connection.client, "AUTH_OK")
                    connection.authenticated = True
                elif auth_status == b"\xdd":
                    status_code_send(connection.client, "AUTH_ERROR")
                    add_logs(f"Authentication failed for {connection.client_address}")
                    connection.auth_tries += 1
                else:
                    print("Unrecognized status code received from local_db")
                    status_code_send(connection.client, "ERROR")

            case 0x04:
                if not connection.authenticated:
                    connection.client.close()
                    break

                # The client sends a two-byte little-endian filename length.
                LENGTH_NAME = receive_exactly(
                    connection.client, 2, connection.client_address
                )
                if not LENGTH_NAME:
                    print("Client disconnected while sending filename length")
                    break
                length_name_int = int.from_bytes(LENGTH_NAME, "little")
                if length_name_int == 0 or length_name_int > 4096:
                    status_code_send(connection.client, "ERROR")
                    break
                status_code_send(connection.client, "OK")

            case 0x05:
                if not connection.authenticated:
                    connection.client.close()
                    break
                NAME = receive_exactly(
                    connection.client, length_name_int, connection.client_address
                )
                if not NAME:
                    print("Client disconnected while sending filename")
                    break
                try:
                    # Validate the path now, before accepting any file payload.
                    relative_name = NAME.decode("utf-8")
                    get_safe_destination(relative_name)
                except (UnicodeDecodeError, ValueError) as exc:
                    print(f"Rejected filename from {connection.client_address}: {exc}")
                    status_code_send(connection.client, "ERROR")
                    break
                status_code_send(connection.client, "OK")

            case 0x06:
                if not connection.authenticated:
                    connection.client.close()
                    break

                LENGTH_FILE_BYTES = receive_exactly(
                    connection.client, 4, connection.client_address
                )
                if not LENGTH_FILE_BYTES:
                    print("Client disconnected while sending file size")
                    break
                LENGTH_FILE = int.from_bytes(LENGTH_FILE_BYTES, "little")
                print(f"FILE: {relative_name} has length: {LENGTH_FILE} bytes")
                print(f"Server max_file_size: {my_server.max_file_length}")

                if LENGTH_FILE == 0:
                    status_code_send(connection.client, "SIZE_ERROR")
                    status_code_receive(connection.client, connection.client_address)
                    add_logs(f"{relative_name} was empty; empty files are not saved")
                elif LENGTH_FILE > my_server.max_file_length:
                    status_code_send(connection.client, "SIZE_ERROR")
                    print(
                        f"Size error acknowledged: {status_code_receive(connection.client, connection.client_address)}"
                    )
                    add_logs(f"{relative_name} exceeded the allowed file size")
                else:
                    status_code_send(connection.client, "OK")

            case 0x07:
                if not connection.authenticated:
                    connection.client.close()
                    break

                try:
                    destination = get_safe_destination(relative_name)
                except ValueError as exc:
                    print(f"Rejected destination path: {exc}")
                    status_code_send(connection.client, "ERROR")
                    break

                print(f"Receiving file: {relative_name} -> {destination}")
                if receive_file_to_disk(connection, LENGTH_FILE, destination):
                    # Update the index immediately so this file is not requested again.
                    refresh_monitor()
                    add_logs(f"Received {relative_name} ({LENGTH_FILE} bytes)")
                    status_code_send(connection.client, "SUCCES_RECEIVED")
                else:
                    add_logs(f"Transfer failed for {relative_name}")
                    status_code_send(connection.client, "ERROR")

    # Close the TLS connection before accepting the next client.
    try:
        connection.client.close()
    except OSError:
        pass
