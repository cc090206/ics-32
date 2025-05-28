# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321

import json
from collections import namedtuple
from typing import List, Optional

# Named tuple for server responses
dsp_fields = ['status', 'message', 'token', 'messages']
DSPResponse = namedtuple('DSPResponse', dsp_fields)


def make_authenticate_request(username: str, password: str) -> str:
    """
    Build a JSON string to authenticate a user.

    Args:
        username: The user's username.
        password: The user's password.

    Returns:
        A JSON-formatted string for the authenticate request.
    """
    request = {
        "authenticate": {
            "username": username,
            "password": password
        }
    }
    return json.dumps(request)


def make_directmessage_request(token: str, entry: str, recipient: str, timestamp: float) -> str:
    """
    Build a JSON string to send a direct message.

    Args:
        token: Authentication token from a successful login.
        entry: The message text to send.
        recipient: The username of the message recipient.
        timestamp: Unix timestamp (float) when the message was created.

    Returns:
        A JSON-formatted string for the directmessage request.
    """
    request = {
        "token": token,
        "directmessage": {
            "entry": entry,
            "recipient": recipient,
            "timestamp": str(timestamp)
        }
    }
    return json.dumps(request)


def make_fetch_request(token: str, what: str) -> str:
    """
    Build a JSON string to fetch messages.

    Args:
        token: Authentication token.
        what: Either 'all' or 'unread' to specify which messages to retrieve.

    Returns:
        A JSON-formatted string for the fetch request.
    """
    request = {
        "token": token,
        "fetch": what
    }
    return json.dumps(request)


def parse_response(json_msg: str) -> DSPResponse:
    """
    Parse a JSON response from the DSP server into a DSPResponse tuple.

    Args:
        json_msg: The raw JSON string returned by the server.

    Returns:
        A DSPResponse(status, message, token, messages) object.

    Raises:
        ValueError: If the JSON is invalid or required fields are missing.
    """
    try:
        obj = json.loads(json_msg)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")

    if 'response' not in obj or not isinstance(obj['response'], dict):
        raise ValueError("Missing or invalid 'response' field in JSON")

    resp = obj['response']
    status = resp.get('type')
    message = resp.get('message')
    token = resp.get('token') if 'token' in resp else None
    messages = resp.get('messages') if 'messages' in resp else []

    # Ensure messages is always a list
    if messages is None:
        messages = []
    elif not isinstance(messages, list):
        raise ValueError("Expected 'messages' to be a list")

    return DSPResponse(status, message, token, messages)
