import json
from pathlib import Path
from ds_messenger import DirectMessage

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
    """
    Local storage for contacts and messages, persisted to JSON.

    The filename should follow the pattern '<username>_notebook.json' so that we can
    infer the local user and correctly identify peers in conversations.
    """
    DEFAULT_FILENAME = "notebook.json"

    def __init__(self, filename: str = None):
        """
        Initialize Notebook and load existing data if available.
        """
        self.filename = filename or Notebook.DEFAULT_FILENAME
        # Derive local user from filename, if pattern matches
        stem = Path(self.filename).stem
        if stem.endswith("_notebook"):
            self.local_user = stem[:-len("_notebook")]
        else:
            self.local_user = None

        # Contacts and messages storage
        self.contacts = []  # list of usernames
        self.messages = {}  # username -> list of message dicts

        # Load any existing notebook data
        self.load()

    def add_contact(self, username: str) -> None:
        """
        Add a new contact and persist.
        """
        if username not in self.contacts and username != self.local_user:
            self.contacts.append(username)
            self.messages.setdefault(username, [])
            self.save()

    def add_message(self, dm: DirectMessage) -> None:
        """
        Store a DirectMessage under the correct peer and persist.
        """
        # Determine peer: who is the other party
        if self.local_user and dm.sender == self.local_user:
            peer = dm.recipient
        elif self.local_user and dm.recipient == self.local_user:
            peer = dm.sender
        else:
            # Fallback for cases without explicit local_user
            peer = dm.sender if dm.sender != dm.recipient else dm.recipient

        entry = {
            'message': dm.message,
            'sender': dm.sender,
            'recipient': dm.recipient,
            'timestamp': dm.timestamp
        }
        self.messages.setdefault(peer, []).append(entry)
        if peer not in self.contacts:
            self.contacts.append(peer)
        self.save()

    def get_contacts(self) -> list:
        """
        Return a list of all contacts (excluding the local user).
        """
        return [c for c in self.contacts if c != self.local_user]

    def get_messages(self, contact: str) -> list:
        """
        Return stored message dicts for a contact.
        """
        return list(self.messages.get(contact, []))

    def has_message_history(self, contact: str) -> bool:
        """
        Check if there are stored messages for contact.
        """
        return contact in self.messages and bool(self.messages[contact])

    def save(self) -> None:
        """
        Persist contacts and messages to a JSON file.
        Raises NotebookFileError on failure.
        """
        target = Path(self.filename)
        data = {
            'contacts': self.contacts,
            'messages': self.messages
        }
        try:
            with open(target, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise NotebookFileError(f"Error saving notebook: {e}")

    def load(self) -> None:
        """
        Load notebook data from a JSON file.
        If the file does not exist or is invalid JSON, start with empty state.
        """
        target = Path(self.filename)
        if not target.exists():
            # No existing file; start fresh
            self.contacts = []
            self.messages = {}
            return
        try:
            with open(target, 'r', encoding='utf-8') as f:
                obj = json.load(f)
            # Override only if structure is valid
            self.contacts = obj.get('contacts', [])
            self.messages = obj.get('messages', {})
        except (json.JSONDecodeError, IOError):
            # Corrupt or unreadable file; reset
            self.contacts = []
            self.messages = {}