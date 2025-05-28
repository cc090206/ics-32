# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321

import socket
from ds_protocol import (
    make_authenticate_request,
    make_directmessage_request,
    make_fetch_request,
    parse_response
)

class DirectMessage:
    def __init__(self):
        self.sender = None
        self.recipient = None
        self.message = None
        self.timestamp = None

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.username = username
        # Determine host and port
        if dsuserver:
            if ':' in dsuserver:
                host, port_str = dsuserver.split(':', 1)
                port = int(port_str)
            else:
                host = dsuserver
                port = 3001
        else:
            host = 'localhost'
            port = 3001
        # Open socket and makefile wrappers
        self._sock = socket.create_connection((host, port))
        self._send = self._sock.makefile('w')
        self._recv = self._sock.makefile('r')
        # Authenticate if credentials supplied
        if username and password:
            if not self._authenticate(username, password):
                raise RuntimeError("Authentication failed")

    def _authenticate(self, username: str, password: str) -> bool:
        req = make_authenticate_request(username, password)
        self._send.write(req + '\r\n')
        self._send.flush()
        line = self._recv.readline()
        resp = parse_response(line)
        if resp.status == 'ok':
            self.token = resp.token
            return True
        return False

    def send(self, message: str, recipient: str) -> bool:
        if not self.token:
            raise RuntimeError("Not authenticated")
        timestamp = __import__('time').time()
        req = make_directmessage_request(self.token, message, recipient, timestamp)
        self._send.write(req + '\r\n')
        self._send.flush()
        line = self._recv.readline()
        resp = parse_response(line)
        return resp.status == 'ok'

    def retrieve_new(self) -> list:
        return self._retrieve('unread')

    def retrieve_all(self) -> list:
        return self._retrieve('all')

    def _retrieve(self, what: str) -> list:
        if not self.token:
            raise RuntimeError("Not authenticated")
        req = make_fetch_request(self.token, what)
        self._send.write(req + '\r\n')
        self._send.flush()
        line = self._recv.readline()
        resp = parse_response(line)
        result = []
        if resp.status != 'ok' or not resp.messages:
            return result
        for msg in resp.messages:
            dm = DirectMessage()
            dm.message = msg.get('message')
            ts = msg.get('timestamp')
            dm.timestamp = float(ts) if ts is not None else None
            if 'from' in msg:
                dm.sender = msg['from']
                dm.recipient = self.username
            else:
                dm.sender = self.username
                dm.recipient = msg.get('recipient')
            result.append(dm)
        return result
