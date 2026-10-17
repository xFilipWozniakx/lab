import hashlib
import json
import os
import socket
import ssl
import struct
import threading

from pathlib import PurePosixPath

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from android import activity
from jnius import autoclass, PythonJavaClass, java_method


# Protocol message types
TYPE_MESSAGE = b"\x01"
TYPE_PHOTO_LIST = b"\x02"
TYPE_AUTH = b"\x03"
TYPE_NAME_LENGTH = b"\x04"
TYPE_NAME = b"\x05"
TYPE_FILE_SIZE = b"\x06"
TYPE_FILE_DATA = b"\x07"

# Protocol status codes
STATUS_OK = b"\xc8"
STATUS_ERROR = b"\xc9"
STATUS_AUTH_OK = b"\xdc"
STATUS_AUTH_ERROR = b"\xdd"
STATUS_SIZE_ERROR = b"\xde"
STATUS_SIZE_ACK = b"\xdf"
STATUS_SUCCESS_RECEIVED = b"\xe0"
STATUS_SIZE_DIFFERENCE = b"\xe1"

CHUNK_SIZE = 64 * 1024
SOCKET_TIMEOUT = 30


class PhotoSyncError(Exception):
    """Base exception for Photo Sync errors."""


class AuthenticationError(PhotoSyncError):
    """Raised when the server rejects the credentials."""


class ServerUnavailableError(PhotoSyncError):
    """Raised when the server cannot be reached."""


class ProtocolError(PhotoSyncError):
    """Raised when the server sends an unexpected response."""


class AndroidFolderAccess:
    """
    Provides access to Android folders selected through the Storage Access
    Framework (SAF).

    Files are represented by content URIs, not filesystem paths.
    """

    def __init__(self):
        self.tree_uri = None
        self.tree_document_id = None

    def set_tree_uri(self, uri):
        DocumentsContract = autoclass(
            "android.provider.DocumentsContract"
        )

        self.tree_uri = uri
        self.tree_document_id = DocumentsContract.getTreeDocumentId(uri)

    def _walk_tree(self, parent_document_id, relative_directory=""):
        DocumentsContract = autoclass(
            "android.provider.DocumentsContract"
        )
        Document = autoclass(
            "android.provider.DocumentsContract$Document"
        )
        Uri = autoclass("android.net.Uri")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")

        resolver = PythonActivity.mActivity.getContentResolver()

        children_uri = (
            DocumentsContract.buildChildDocumentsUriUsingTree(
                self.tree_uri,
                parent_document_id,
            )
        )

        projection = [
            Document.COLUMN_DOCUMENT_ID,
            Document.COLUMN_DISPLAY_NAME,
            Document.COLUMN_MIME_TYPE,
            Document.COLUMN_SIZE,
        ]

        cursor = resolver.query(
            children_uri,
            projection,
            None,
            None,
            None,
        )

        files = {}

        if cursor is None:
            return files

        try:
            id_index = cursor.getColumnIndex(
                Document.COLUMN_DOCUMENT_ID
            )
            name_index = cursor.getColumnIndex(
                Document.COLUMN_DISPLAY_NAME
            )
            mime_index = cursor.getColumnIndex(
                Document.COLUMN_MIME_TYPE
            )

            while cursor.moveToNext():
                document_id = cursor.getString(id_index)
                display_name = cursor.getString(name_index)
                mime_type = cursor.getString(mime_index)

                if not display_name:
                    continue

                relative_path = str(
                    PurePosixPath(relative_directory) / display_name
                )

                if mime_type == Document.MIME_TYPE_DIR:
                    # Use the actual document ID returned by Android.
                    # Document IDs must not be constructed from paths.
                    files.update(
                        self._walk_tree(
                            document_id,
                            relative_path,
                        )
                    )
                else:
                    document_uri = (
                        DocumentsContract
                        .buildDocumentUriUsingTree(
                            self.tree_uri,
                            document_id,
                        )
                    )

                    files[relative_path] = str(document_uri)

        finally:
            cursor.close()

        return files

    def list_files(self):
        if self.tree_uri is None or self.tree_document_id is None:
            raise PhotoSyncError(
                "Select a folder before starting synchronization."
            )

        return self._walk_tree(self.tree_document_id)

    def read_file(self, content_uri):
        Uri = autoclass("android.net.Uri")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")

        resolver = PythonActivity.mActivity.getContentResolver()
        stream = resolver.openInputStream(Uri.parse(content_uri))

        if stream is None:
            raise PhotoSyncError(
                "Android could not open the selected file."
            )

        output = bytearray()
        buffer = bytearray(CHUNK_SIZE)

        try:
            ByteArray = autoclass("[B")
            java_buffer = ByteArray(CHUNK_SIZE)

            while True:
                count = stream.read(java_buffer)

                if count == -1:
                    break

                for index in range(count):
                    output.append(java_buffer[index] & 0xFF)

        finally:
            stream.close()

        return bytes(output)


class FolderPickerResult(PythonJavaClass):
    """
    Receives the result of Android's folder picker.
    """

    __javainterfaces__ = [
        "org/kivy/android/PythonActivity$ActivityResultListener"
    ]
    __javacontext__ = "app"

    def __init__(self, app):
        super().__init__()
        self.app = app

    @java_method("(IILandroid/content/Intent;)V")
    def onActivityResult(self, request_code, result_code, intent):
        if request_code != self.app.folder_request_code:
            return False

        RESULT_OK = -1

        if result_code != RESULT_OK or intent is None:
            Clock.schedule_once(
                lambda dt: self.app.set_status(
                    "Folder selection cancelled."
                ),
                0,
            )
            return True

        uri = intent.getData()

        if uri is None:
            Clock.schedule_once(
                lambda dt: self.app.set_status(
                    "Android did not return a folder URI."
                ),
                0,
            )
            return True

        try:
            self.app.folder_access.set_tree_uri(uri)

            # Persist permission so the app can access the selected folder
            # after the picker closes.
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )
            Intent = autoclass("android.content.Intent")

            resolver = (
                PythonActivity.mActivity.getContentResolver()
            )

            flags = intent.getFlags()
            permission_flags = (
                flags
                & Intent.FLAG_GRANT_READ_URI_PERMISSION
                & Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            )

            resolver.takePersistableUriPermission(
                uri,
                permission_flags,
            )

            self.app.selected_folder = str(uri)

            Clock.schedule_once(
                lambda dt: self.app.set_status(
                    "Folder selected successfully."
                ),
                0,
            )

        except Exception as exc:
            Clock.schedule_once(
                lambda dt: self.app.set_status(
                    f"Folder error: {exc}"
                ),
                0,
            )

        return True


class PhotoSyncClient:
    """
    TCP/TLS client.

    This class assumes every protocol message uses:
        1 byte  - message type
        4 bytes - payload length, little-endian
        N bytes - payload

    Confirm this framing against the current server before deployment.
    """

    def __init__(self, host, port, timeout=SOCKET_TIMEOUT):
        self.host = host.strip()
        self.port = int(port)
        self.timeout = timeout
        self.sock = None

    def connect(self):
        if not self.host:
            raise PhotoSyncError("Enter the server address.")

        try:
            raw_socket = socket.create_connection(
                (self.host, self.port),
                timeout=self.timeout,
            )
            raw_socket.settimeout(self.timeout)

        except socket.gaierror as exc:
            raise ServerUnavailableError(
                "The server address could not be resolved. "
                "Check the hostname or DNS settings."
            ) from exc

        except ConnectionRefusedError as exc:
            raise ServerUnavailableError(
                "The server refused the connection. "
                "Check that the server is running and the port is correct."
            ) from exc

        except socket.timeout as exc:
            raise ServerUnavailableError(
                "Connection timed out. The server may be unreachable."
            ) from exc

        except OSError as exc:
            raise ServerUnavailableError(
                f"Could not connect to the server: {exc}"
            ) from exc

        try:
            # Temporary testing configuration only.
            # Replace with certificate verification before production use.
            tls_context = ssl._create_unverified_context()

            self.sock = tls_context.wrap_socket(
                raw_socket,
                server_hostname=self.host,
            )

        except ssl.SSLError as exc:
            raw_socket.close()
            raise PhotoSyncError(
                "TLS handshake failed. Check the server certificate, "
                "TLS configuration, and whether this port forwards raw TLS."
            ) from exc

        except OSError as exc:
            raw_socket.close()
            raise ServerUnavailableError(
                f"Connection failed during TLS setup: {exc}"
            ) from exc

    def close(self):
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            try:
                self.sock.close()
            except OSError:
                pass

            self.sock = None

    def send_exactly(self, data):
        if self.sock is None:
            raise ServerUnavailableError(
                "There is no active server connection."
            )

        try:
            self.sock.sendall(data)
        except (socket.timeout, TimeoutError) as exc:
            raise ServerUnavailableError(
                "The server timed out while receiving data."
            ) from exc
        except (BrokenPipeError, ConnectionResetError, OSError) as exc:
            raise ServerUnavailableError(
                "The connection was lost while sending data."
            ) from exc

    def receive_exactly(self, size):
        if self.sock is None:
            raise ServerUnavailableError(
                "There is no active server connection."
            )

        if size < 0:
            raise ProtocolError("Invalid response length from the server.")

        result = bytearray()

        while len(result) < size:
            try:
                chunk = self.sock.recv(size - len(result))

            except socket.timeout as exc:
                raise ServerUnavailableError(
                    "The server did not respond in time."
                ) from exc

            except OSError as exc:
                raise ServerUnavailableError(
                    "The connection was interrupted while receiving data."
                ) from exc

            if not chunk:
                raise ServerUnavailableError(
                    "The server closed the connection unexpectedly."
                )

            result.extend(chunk)

        return bytes(result)

    def send_packet(self, message_type, payload=b""):
        header = message_type + struct.pack("<I", len(payload))
        self.send_exactly(header + payload)

    def receive_packet(self):
        message_type = self.receive_exactly(1)
        payload_length = struct.unpack(
            "<I",
            self.receive_exactly(4),
        )[0]

        if payload_length > 100 * 1024 * 1024:
            raise ProtocolError(
                "The server sent an unexpectedly large message."
            )

        payload = self.receive_exactly(payload_length)
        return message_type, payload

    def authenticate(self, login, password):
        if not login or not password:
            raise AuthenticationError(
                "Enter both username and password."
            )

        credentials = {
            "login": login,
            "password": password,
        }

        payload = json.dumps(credentials).encode("utf-8")
        self.send_packet(TYPE_AUTH, payload)

        response_type, response_payload = self.receive_packet()

        if response_type == STATUS_AUTH_ERROR:
            raise AuthenticationError(
                "Incorrect username or password."
            )

        if response_type != STATUS_AUTH_OK:
            details = response_payload.decode(
                "utf-8",
                errors="replace",
            )

            raise ProtocolError(
                "Unexpected authentication response from the server"
                + (f": {details}" if details else ".")
            )

    def send_file(self, filename, data):
        """
        Send one file.

        The field encoding below follows the framed-message assumption.
        Verify each stage against the server's receive logic.
        """
        filename_bytes = filename.encode("utf-8")

        if len(filename_bytes) > 65535:
            raise PhotoSyncError(
                f"Filename is too long: {filename}"
            )

        self.send_packet(
            TYPE_NAME_LENGTH,
            struct.pack("<H", len(filename_bytes)),
        )

        response_type, response_payload = self.receive_packet()
        if response_type == STATUS_ERROR:
            raise ProtocolError(
                "The server rejected the filename length."
            )

        self.send_packet(TYPE_NAME, filename_bytes)

        response_type, response_payload = self.receive_packet()
        if response_type == STATUS_ERROR:
            raise ProtocolError(
                "The server rejected the filename."
            )

        self.send_packet(
            TYPE_FILE_SIZE,
            struct.pack("<I", len(data)),
        )

        response_type, response_payload = self.receive_packet()

        if response_type == STATUS_SIZE_ERROR:
            raise PhotoSyncError(
                f"The server rejected the file size: {filename}"
            )

        if response_type not in (
            STATUS_SIZE_ACK,
            STATUS_SIZE_DIFFERENCE,
        ):
            raise ProtocolError(
                "Unexpected response after sending file size."
            )

        for offset in range(0, len(data), CHUNK_SIZE):
            chunk = data[offset:offset + CHUNK_SIZE]
            self.send_packet(TYPE_FILE_DATA, chunk)

        response_type, response_payload = self.receive_packet()

        if response_type != STATUS_SUCCESS_RECEIVED:
            raise ProtocolError(
                f"The server did not confirm receipt of {filename}."
            )

    def send_photo_list(self, photo_list):
        payload = json.dumps(photo_list).encode("utf-8")
        self.send_packet(TYPE_PHOTO_LIST, payload)

        response_type, response_payload = self.receive_packet()

        if response_type == STATUS_ERROR:
            raise ProtocolError(
                "The server rejected the photo list."
            )

        return response_type, response_payload


KV = """
<PhotoSyncLayout>:
    orientation: "vertical"
    padding: "16dp"
    spacing: "10dp"

    Label:
        text: "Photo Sync"
        font_size: "24sp"
        size_hint_y: None
        height: "44dp"

    TextInput:
        id: host
        hint_text: "Server hostname or IP address"
        text: "127.0.0.1"
        multiline: False
        size_hint_y: None
        height: "48dp"

    TextInput:
        id: port
        hint_text: "Server port"
        text: "5555"
        input_filter: "int"
        multiline: False
        size_hint_y: None
        height: "48dp"

    TextInput:
        id: login
        hint_text: "Username"
        multiline: False
        size_hint_y: None
        height: "48dp"

    TextInput:
        id: password
        hint_text: "Password"
        password: True
        multiline: False
        size_hint_y: None
        height: "48dp"

    Button:
        text: "Select folder"
        size_hint_y: None
        height: "48dp"
        on_release: app.choose_folder()

    Label:
        text: app.folder_status
        size_hint_y: None
        height: "44dp"
        text_size: self.width, None

    Button:
        text: "Start sync"
        size_hint_y: None
        height: "48dp"
        on_release: app.start_sync()

    Label:
        text: app.status
        text_size: self.width, None
        halign: "left"
        valign: "top"
"""


class PhotoSyncLayout(BoxLayout):
    pass


class PhotoSyncApp(App):
    status = StringProperty("Ready.")
    folder_status = StringProperty("No folder selected.")

    folder_request_code = 9021

    def build(self):
        self.title = "Photo Sync"
        self.folder_access = AndroidFolderAccess()
        self.selected_folder = None
        self._sync_running = False

        self.picker_listener = FolderPickerResult(self)

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        PythonActivity.mActivity.addActivityResultListener(
            self.picker_listener
        )

        return Builder.load_string(KV)

    def set_status(self, message):
        self.status = str(message)

    def choose_folder(self):
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")

            intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)

            intent.addFlags(
                Intent.FLAG_GRANT_READ_URI_PERMISSION
                | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
            )

            PythonActivity.mActivity.startActivityForResult(
                intent,
                self.folder_request_code,
            )

            self.set_status("Choose a folder in the Android picker.")

        except Exception as exc:
            self.set_status(f"Could not open folder picker: {exc}")

    def start_sync(self):
        if self._sync_running:
            self.set_status("Synchronization is already running.")
            return

        if not self.selected_folder:
            self.set_status("Select a folder first.")
            return

        host = self.root.ids.host.text.strip()
        port_text = self.root.ids.port.text.strip()
        login = self.root.ids.login.text.strip()
        password = self.root.ids.password.text

        try:
            port = int(port_text)
            if not 1 <= port <= 65535:
                raise ValueError
        except ValueError:
            self.set_status("Enter a valid port between 1 and 65535.")
            return

        self._sync_running = True
        self.set_status("Connecting to server...")

        threading.Thread(
            target=self._sync_worker,
            args=(host, port, login, password),
            daemon=True,
        ).start()

    def _sync_worker(self, host, port, login, password):
        client = PhotoSyncClient(host, port)

        try:
            client.connect()
            self._set_status_threadsafe("Connected. Authenticating...")

            client.authenticate(login, password)

            self._set_status_threadsafe(
                "Authentication successful. Scanning folder..."
            )

            files = self.folder_access.list_files()

            photo_list = []

            for relative_name, content_uri in files.items():
                photo_list.append({
                    "name": relative_name,
                    "uri": content_uri,
                })

            # The current protocol must define which side initiates
            # transfers and what response the server returns here.
            client.send_photo_list(photo_list)

            self._set_status_threadsafe(
                f"Found {len(files)} files. "
                "Photo list sent; transfer negotiation must match the server."
            )

        except AuthenticationError as exc:
            self._set_status_threadsafe(str(exc))

        except ServerUnavailableError as exc:
            self._set_status_threadsafe(
                f"Connection error: {exc}"
            )

        except ssl.SSLError as exc:
            self._set_status_threadsafe(
                f"TLS error: {exc}"
            )

        except ProtocolError as exc:
            self._set_status_threadsafe(
                f"Protocol error: {exc}"
            )

        except PhotoSyncError as exc:
            self._set_status_threadsafe(str(exc))

        except Exception as exc:
            self._set_status_threadsafe(
                f"Unexpected error: {type(exc).__name__}: {exc}"
            )

        finally:
            client.close()
            self._sync_running = False

    def _set_status_threadsafe(self, message):
        Clock.schedule_once(
            lambda dt: self.set_status(message),
            0,
        )

    def on_stop(self):
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            PythonActivity.mActivity.removeActivityResultListener(
                self.picker_listener
            )
        except Exception:
            pass


if __name__ == "__main__":
    PhotoSyncApp().run()
