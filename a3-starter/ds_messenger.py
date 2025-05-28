# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321

import time
from socket import socket, AF_INET, SOCK_STREAM
from collections import namedtuple

from ds_protocol import (
    make_authenticate_request,
    make_directmessage_request,
    make_fetch_request,
    parse_response,
)
from notebook import Notebook

# Simple container for a single DM
DirectMessage = namedtuple('DirectMessage', ['sender', 'recipient', 'message', 'timestamp'])

class DirectMessenger:
    """
    Handles a persistent connection to the DSP server, and
    locally persists contacts & messages via Notebook.
    """

    def __init__(
        self,
        server_host: str = 'localhost',
        server_port: int = 3001,
        username: str = None,
        password: str = None,
        notebook_file: str = None
    ):
        # 1) Open socket + file‐wrappers
        self.server = (server_host, server_port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(self.server)
        self._send_file = self.sock.makefile('w')
        self._recv_file = self.sock.makefile('r')

        # 2) Persistence layer
        #    default notebook filename: "<username>_notebook.json"
        nb_filename = notebook_file or f"{username}_notebook.json"
        self.notebook = Notebook(nb_filename)

        # 3) Authenticate once and store token
        auth_req = make_authenticate_request(username, password)
        self._send(auth_req)
        resp = parse_response(self._recv())
        if resp.status != 'ok':
            raise RuntimeError(f"Authentication failed: {resp.message}")
        self.token = resp.token

    def _send(self, msg_str: str) -> None:
        """Write a line (JSON) to the server and flush."""
        self._send_file.write(msg_str + '\r\n')
        self._send_file.flush()

    def _recv(self) -> str:
        """Read a line (JSON) back from the server."""
        return self._recv_file.readline()

    def send(self, message: str, recipient: str) -> bool:
        """
        Send a direct message.
        Returns True on success, False on failure.
        """
        req = make_directmessage_request(self.token, message, recipient)
        self._send(req)
        resp = parse_response(self._recv())

        if resp.status == 'ok':
            dm = DirectMessage(
                sender=None,             # outgoing
                recipient=recipient,
                message=message,
                timestamp=str(time.time())
            )
            self.notebook.add_contact(recipient)
            self.notebook.add_message(dm)
            return True
        return False

    def retrieve_new(self) -> list[DirectMessage]:
        """
        Fetch only unread messages, persist them, and return a list
        of DirectMessage(sender, None, message, timestamp).
        """
        req = make_fetch_request(self.token, 'unread')
        self._send(req)
        resp = parse_response(self._recv())

        out = []
        for m in resp.messages:
            dm = DirectMessage(
                sender=m['from'],
                recipient=None,
                message=m['message'],
                timestamp=m['timestamp']
            )
            self.notebook.add_contact(dm.sender)
            self.notebook.add_message(dm)
            out.append(dm)
        return out

    def retrieve_all(self) -> list[DirectMessage]:
        """
        Fetch all history, persist anything new, and return a list of DirectMessage.
        """
        req = make_fetch_request(self.token, 'all')
        self._send(req)
        resp = parse_response(self._recv())

        out = []
        for m in resp.messages:
            dm = DirectMessage(
                sender=m.get('from'),
                recipient=m.get('recipient'),
                message=m['message'],
                timestamp=m['timestamp']
            )
            # figure out which side is the peer
            peer = dm.sender or dm.recipient
            self.notebook.add_contact(peer)
            self.notebook.add_message(dm)
            out.append(dm)
        return out