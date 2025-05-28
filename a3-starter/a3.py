# a2.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ds_messenger import DirectMessenger
from notebook import Notebook, DirectMessage
import threading

class ChatApp(tk.Tk):
    POLL_INTERVAL = 2000  # ms

    def __init__(self):
        super().__init__()
        self.title("ICS 32 Distributed Social Messenger")
        # Prompt for server and credentials
        self.server = simpledialog.askstring("Server", "Enter server address (host:port)", initialvalue="localhost:3001")
        self.username = simpledialog.askstring("Login", "Username:")
        self.password = simpledialog.askstring("Login", "Password:", show='*')
        # Instantiate messenger and notebook
        try:
            self.messenger = DirectMessenger(self.server, self.username, self.password)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect/authenticate: {e}")
            self.destroy(); return
        self.notebook = Notebook(f"{self.username}_notebook.json")
        # UI setup
        self._build_ui()
        # Load contacts and messages
        self._load_contacts()
        # Start polling for new messages
        self.after(self.POLL_INTERVAL, self._poll_new)

    def _build_ui(self):
        # Paned layout
        paned = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        # Contacts frame
        left_frame = ttk.Frame(paned, width=150)
        paned.add(left_frame, weight=1)
        self.tree = ttk.Treeview(left_frame, show='tree')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_contact_select)
        add_btn = ttk.Button(left_frame, text="Add Contact", command=self._add_contact)
        add_btn.pack(fill=tk.X)
        # Chat frame
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        self.chat_display = tk.Text(right_frame, state='disabled', wrap='word')
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        # Entry and send
        entry_frame = ttk.Frame(right_frame)
        entry_frame.pack(fill=tk.X)
        self.msg_entry = ttk.Entry(entry_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        send_btn = ttk.Button(entry_frame, text="Send", command=self._send_message)
        send_btn.pack(side=tk.RIGHT)
        # Status bar
        self.status = ttk.Label(self, text="Ready.")
        self.status.pack(fill=tk.X, side=tk.BOTTOM)
        # Text tags
        self.chat_display.tag_config('incoming', justify='left', foreground='blue')
        self.chat_display.tag_config('outgoing', justify='right', foreground='green')

    def _load_contacts(self):
        for user in self.notebook.get_contacts():
            self.tree.insert('', 'end', iid=user, text=user)

    def _on_contact_select(self, event=None):
        sel = self.tree.selection()
        if not sel: return
        self.current = sel[0]
        self._show_messages(self.current)

    def _show_messages(self, contact):
        msgs = self.notebook.get_messages(contact)
        self.chat_display.config(state='normal')
        self.chat_display.delete('1.0', tk.END)
        for m in msgs:
            tag = 'incoming' if m['sender'] != self.username else 'outgoing'
            text = f"{m['sender']}: {m['message']}\n"
            self.chat_display.insert(tk.END, text, tag)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def _add_contact(self):
        new = simpledialog.askstring("Add Contact", "Enter contact username:")
        if new:
            self.notebook.add_contact(new)
            if not self.tree.exists(new):
                self.tree.insert('', 'end', iid=new, text=new)

    def _send_message(self):
        if not hasattr(self, 'current'):
            messagebox.showwarning("No Contact", "Select a contact first.")
            return
        text = self.msg_entry.get().strip()
        if not text: return
        success = self.messenger.send(text, self.current)
        if success:
            dm = DirectMessage()
            dm.sender = self.username
            dm.recipient = self.current
            dm.message = text
            dm.timestamp = __import__('time').time()
            self.notebook.add_message(dm)
            self._show_messages(self.current)
            self.msg_entry.delete(0, tk.END)
            self.status.config(text="Message sent.")
        else:
            self.status.config(text="Send failed.")

    def _poll_new(self):
        try:
            new = self.messenger.retrieve_new()
            for dm in new:
                self.notebook.add_message(dm)
                if not self.tree.exists(dm.sender):
                    self.tree.insert('', 'end', iid=dm.sender, text=dm.sender)
                if getattr(self, 'current', None) == dm.sender:
                    self._show_messages(dm.sender)
            self.status.config(text=f"{len(new)} new messages.")
        except Exception as e:
            self.status.config(text=f"Error fetching: {e}")
        finally:
            self.after(self.POLL_INTERVAL, self._poll_new)

if __name__ == '__main__':
    app = ChatApp()
    app.mainloop()
