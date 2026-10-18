import json
import socket
import ssl
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


SERVER_PORT = 5555
CONNECT_TIMEOUT = 10

AUTHENTICATE = b"\x03"
AUTH_OK = b"\xdc"
AUTH_ERROR = b"\xdd"
ERROR = b"\xc9"


class PhotoSyncApp(App):
    def build(self):
        self.title = "Photo Sync"
        self.client_socket = None
        self.connected = False
        self.busy = False

        root = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(12),
        )

        root.add_widget(
            Label(
                text="[b]Photo Sync[/b]",
                markup=True,
                font_size="28sp",
                size_hint_y=None,
                height=dp(52),
            )
        )

        root.add_widget(
            Label(
                text="Phone to server backup",
                size_hint_y=None,
                height=dp(28),
            )
        )

        self.host_input = TextInput(
            hint_text="Server IP address",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
        )
        root.add_widget(self.host_input)

        self.port_input = TextInput(
            hint_text="Port",
            text=str(SERVER_PORT),
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
        )
        root.add_widget(self.port_input)

        self.login_input = TextInput(
            hint_text="Login",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
        )
        root.add_widget(self.login_input)

        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(50),
        )
        root.add_widget(self.password_input)

        self.status_label = Label(
            text="Not connected",
            size_hint_y=None,
            height=dp(35),
        )
        root.add_widget(self.status_label)

        self.connect_button = Button(
            text="Connect and log in",
            size_hint_y=None,
            height=dp(54),
        )
        self.connect_button.bind(on_release=self.connect_and_login)
        root.add_widget(self.connect_button)

        self.sync_button = Button(
            text="Sync photos",
            size_hint_y=None,
            height=dp(54),
            disabled=True,
        )
        self.sync_button.bind(on_release=self.start_sync)
        root.add_widget(self.sync_button)

        root.add_widget(Widget())

        self.message_label = Label(
            text="Enter your server details",
            size_hint_y=None,
            height=dp(45),
        )
        root.add_widget(self.message_label)

        return root

    def connect_and_login(self, instance):
        if self.busy:
            return

        host = self.host_input.text.strip()
        login = self.login_input.text.strip()
        password = self.password_input.text
        port_text = self.port_input.text.strip()

        if not host or not login or not password or not port_text:
            self.message_label.text = "Complete all fields first"
            return

        try:
            port = int(port_text)
            if not 1 <= port <= 65535:
                raise ValueError
        except ValueError:
            self.message_label.text = "Invalid port number"
            return

        self.busy = True
        self.connect_button.disabled = True
        self.status_label.text = "Connecting..."
        self.message_label.text = "Establishing secure connection"

        threading.Thread(
            target=self._connect_worker,
            args=(host, port, login, password),
            daemon=True,
        ).start()

    def _connect_worker(self, host, port, login, password):
        client = None

        try:
            raw_socket = socket.create_connection(
                (host, port),
                timeout=CONNECT_TIMEOUT,
            )

            # TODO: Replace this with a trusted CA certificate context.
            # Do not use an unverified TLS context in production.
            tls_context = ssl.create_default_context()

            client = tls_context.wrap_socket(
                raw_socket,
                server_hostname=host,
            )
            client.settimeout(CONNECT_TIMEOUT)

            auth_payload = json.dumps(
                {
                    "login": login,
                    # The existing server expects the plain-text password
                    # under the legacy field name "password_hash".
                    "password_hash": password,
                }
            ).encode("utf-8")

            # Frame: 1-byte type + 4-byte little-endian payload length
            # + payload.
            frame = (
                AUTHENTICATE
                + len(auth_payload).to_bytes(4, "little")
                + auth_payload
            )
            client.sendall(frame)

            response = self._receive_exactly(client, 1)

            if response == AUTH_OK:
                self.client_socket = client
                client = None
                Clock.schedule_once(
                    lambda dt: self._login_result(True, "Login successful"),
                    0,
                )
            elif response == AUTH_ERROR:
                Clock.schedule_once(
                    lambda dt: self._login_result(
                        False, "Invalid login or password"
                    ),
                    0,
                )
            elif response == ERROR:
                Clock.schedule_once(
                    lambda dt: self._login_result(
                        False, "Server returned an error"
                    ),
                    0,
                )
            else:
                Clock.schedule_once(
                    lambda dt: self._login_result(
                        False,
                        f"Unexpected server response: {response!r}",
                    ),
                    0,
                )

        except (OSError, ssl.SSLError, ValueError) as exc:
            message = str(exc)
            Clock.schedule_once(
                lambda dt, msg=message: self._login_result(
                    False, f"Connection failed: {msg}"
                ),
                0,
            )
        finally:
            if client is not None:
                try:
                    client.close()
                except OSError:
                    pass

    @staticmethod
    def _receive_exactly(sock, size):
        data = bytearray()

        while len(data) < size:
            chunk = sock.recv(size - len(data))
            if not chunk:
                raise ConnectionError("Server closed the connection")
            data.extend(chunk)

        return bytes(data)

    def _login_result(self, success, message):
        self.busy = False
        self.connect_button.disabled = False
        self.message_label.text = message

        if success:
            self.connected = True
            self.status_label.text = "Connected and authenticated"
            self.sync_button.disabled = False
            self.connect_button.text = "Connected"
            self.connect_button.disabled = True
        else:
            self.connected = False
            self.status_label.text = "Not connected"
            self.sync_button.disabled = True

    def start_sync(self, instance):
        if not self.connected:
            self.message_label.text = "Connect to the server first"
            return

        self.message_label.text = (
            "Login works. Photo transfer is the next implementation step."
        )

    def on_stop(self):
        if self.client_socket is not None:
            try:
                self.client_socket.close()
            except OSError:
                pass


if __name__ == "__main__":
    PhotoSyncApp().run()

