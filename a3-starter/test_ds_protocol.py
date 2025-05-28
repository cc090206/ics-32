import unittest
import json
from ds_protocol import (
    make_authenticate_request,
    make_directmessage_request,
    make_fetch_request,
    parse_response,
    DSPResponse
)

class TestDSPProtocol(unittest.TestCase):
    def test_make_authenticate_request(self):
        username = "alice"
        password = "wonderland"
        req_str = make_authenticate_request(username, password)
        req = json.loads(req_str)
        self.assertIn('authenticate', req)
        self.assertEqual(req['authenticate']['username'], username)
        self.assertEqual(req['authenticate']['password'], password)

    def test_make_directmessage_request(self):
        token = "tok123"
        entry = "Hello, Bob!"
        recipient = "bob"
        timestamp = 1600000000.123
        req_str = make_directmessage_request(token, entry, recipient, timestamp)
        req = json.loads(req_str)
        self.assertEqual(req['token'], token)
        dm = req['directmessage']
        self.assertEqual(dm['entry'], entry)
        self.assertEqual(dm['recipient'], recipient)
        self.assertEqual(dm['timestamp'], str(timestamp))

    def test_make_fetch_request(self):
        token = "tok456"
        what = "unread"
        req_str = make_fetch_request(token, what)
        req = json.loads(req_str)
        self.assertEqual(req['token'], token)
        self.assertEqual(req['fetch'], what)

    def test_parse_response_ok_auth(self):
        resp_obj = {
            "response": {
                "type": "ok",
                "message": "Welcome back, alice",
                "token": "abc123"
            }
        }
        json_str = json.dumps(resp_obj)
        resp = parse_response(json_str)
        expected = DSPResponse(status='ok', message='Welcome back, alice', token='abc123', messages=None)
        self.assertEqual(resp, expected)

    def test_parse_response_error(self):
        resp_obj = {
            "response": {
                "type": "error",
                "message": "Authentication failed"
            }
        }
        json_str = json.dumps(resp_obj)
        resp = parse_response(json_str)
        expected = DSPResponse(status='error', message='Authentication failed', token=None, messages=None)
        self.assertEqual(resp, expected)

    def test_parse_response_fetch_unread(self):
        msgs = [
            {"message": "Hi!", "from": "bob", "timestamp": "1600000100.0"}
        ]
        resp_obj = {"response": {"type": "ok", "messages": msgs}}
        json_str = json.dumps(resp_obj)
        resp = parse_response(json_str)
        self.assertEqual(resp.status, 'ok')
        self.assertIsNone(resp.message)
        self.assertIsNone(resp.token)
        self.assertEqual(resp.messages, msgs)

    def test_parse_response_fetch_all(self):
        msgs = [
            {"message": "Hello!", "recipient": "bob", "timestamp": "1600000200.0"},
            {"message": "Hey", "from": "bob", "timestamp": "1600000300.0"}
        ]
        resp_obj = {"response": {"type": "ok", "messages": msgs}}
        json_str = json.dumps(resp_obj)
        resp = parse_response(json_str)
        self.assertEqual(resp.status, 'ok')
        self.assertIsNone(resp.message)
        self.assertIsNone(resp.token)
        self.assertEqual(resp.messages, msgs)

if __name__ == '__main__':
    unittest.main()
