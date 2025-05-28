import json
from pathlib import Path

class NotebookFileError(Exception):
    """
    Raised when saving notebook data fails.
    """
    pass

class IncorrectNotebookError(Exception):
    """
    Raised when loading notebook data fails unexpectedly.
    """
    pass

class Notebook:
    def __init__(self, filename: str):
        self.path = Path(filename)
        self.contacts = set()
        # messages will be stored as a list of dicts:
        # { 'sender': str, 'recipient': str, 'message': str, 'timestamp': str }
        self.messages = []
        self._load()

    def _load(self):
        if self.path.exists():
            with self.path.open('r') as f:
                data = json.load(f)
            self.contacts = set(data.get('contacts', []))
            self.messages = data.get('messages', [])

    def _save(self):
        with self.path.open('w') as f:
            json.dump({
                'contacts': sorted(self.contacts),
                'messages': self.messages
            }, f, indent=2)

    def add_contact(self, username: str):
        """Add a new contact (if not already present) and persist."""
        if username not in self.contacts:
            self.contacts.add(username)
            self._save()

    def add_message(self, dm):
        """
        Add a DirectMessage instance to the message history and persist.
        Expects dm to have attributes: sender, recipient, message, timestamp.
        """
        entry = {
            'sender': dm.sender,
            'recipient': dm.recipient,
            'message': dm.message,
            'timestamp': dm.timestamp
        }
        self.messages.append(entry)
        self._save()
