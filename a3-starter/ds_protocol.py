# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321

import json
from collections import namedtuple

# Namedtuple for parsed DSP server responses
DSPResponse = namedtuple('DSPResponse', ['status', 'message', 'token', 'messages'])


def make_authenticate_request(username: str, password: str) -> str:
    req = {
        "authenticate": {
            "username": username,
            "password": password
        }
    }
    return json.dumps(req)


def make_directmessage_request(token: str, entry: str, recipient: str, timestamp: float) -> str:
    req = {
        "token": token,
        "directmessage": {
            "entry": entry,
            "recipient": recipient,
            "timestamp": str(timestamp)
        }
    }
    return json.dumps(req)


def make_fetch_request(token: str, what: str) -> str:
    req = {
        "token": token,
        "fetch": what
    }
    return json.dumps(req)


def parse_response(json_msg: str) -> DSPResponse:
    try:
        obj = json.loads(json_msg)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")

    resp = obj.get('response', {})
    status = resp.get('type')
    message = resp.get('message')
    token = resp.get('token') if status == 'ok' and 'token' in resp else None
    messages = resp.get('messages') if 'messages' in resp else None

    return DSPResponse(status, message, token, messages)
