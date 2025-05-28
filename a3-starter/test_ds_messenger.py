import os
import sys
import time
import uuid
import subprocess
import unittest

# Ensure modules in current directory are importable
TEST_DIR = os.path.dirname(__file__)
if TEST_DIR not in sys.path:
    sys.path.insert(0, TEST_DIR)

from ds_messenger import DirectMessenger, DirectMessage

class TestDSMessenger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start DSP server on port 3001
        cls.server_proc = subprocess.Popen(
            [sys.executable, os.path.join(TEST_DIR, 'server.py'), '3001'],
            cwd=TEST_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)  # give server time to start  # give server time to start

    @classmethod
    def tearDownClass(cls):
        # Terminate server process
        cls.server_proc.terminate()
        try:
            cls.server_proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            cls.server_proc.kill()

    def test_authentication_and_send_retrieve(self):
        # generate unique users
        user1 = f"user_{uuid.uuid4().hex}"
        user2 = f"user_{uuid.uuid4().hex}"
        pw = "testpass"
        # Create messengers
        alice = DirectMessenger(username=user1, password=pw)
        bob = DirectMessenger(username=user2, password=pw)

        # Ensure tokens set
        self.assertIsNotNone(alice.token)
        self.assertIsNotNone(bob.token)

        # Alice sends message to Bob
        text = "Hello Bob!"
        success = alice.send(text, user2)
        self.assertTrue(success)

        # Bob retrieves new messages
        new_msgs = bob.retrieve_new()
        self.assertIsInstance(new_msgs, list)
        self.assertEqual(len(new_msgs), 1)
        msg = new_msgs[0]
        self.assertIsInstance(msg, DirectMessage)
        self.assertEqual(msg.message, text)
        self.assertEqual(msg.sender, user1)
        self.assertEqual(msg.recipient, user2)
        self.assertIsInstance(msg.timestamp, float)

        # retrieve_all should also include the message
        all_msgs = bob.retrieve_all()
        # might have exactly one or more (depending on unread state)
        self.assertTrue(any(m.message == text for m in all_msgs))

    def test_send_without_authentication_raises(self):
        dm = DirectMessenger()
        with self.assertRaises(RuntimeError):
            dm.send("Hi", "someone")

    def test_retrieve_without_authentication_raises(self):
        dm = DirectMessenger()
        with self.assertRaises(RuntimeError):
            dm.retrieve_new()
        with self.assertRaises(RuntimeError):
            dm.retrieve_all()

if __name__ == '__main__':
    unittest.main()
