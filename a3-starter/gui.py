import time
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from ds_messenger import DirectMessenger, DirectMessage
from notebook import Notebook

class ChatApp(tk.Tk):
    POLL_INTERVAL = 2000  # milliseconds

    def __init__(self):
        super().__init__()
        self.title("ICS 32 Distributed Social Messenger")

        # 1) Prompt for server and credentials
        server_input = simpledialog.askstring(
            "Server", 
            "Enter server address (host:port)", 
            initialvalue="localhost:3001"
        )
        if not server_input or ':' not in server_input:
            messagebox.showerror("Error", "Server must be host:port")
            self.destroy()
            return
        host, port_str = server_input.split(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", f"Invalid port: {port_str}")
            self.destroy()
            return

        username = simpledialog.askstring("Login", "Username:")
        if not username:
            messagebox.showerror("Error", "Username required")
            self.destroy()
            return

        password = simpledialog.askstring("Login", "Password:", show="*")
        if password is None:
            messagebox.showerror("Error", "Password required")
            self.destroy()
            return

        # 2) Instantiate messenger (this also loads <username>_notebook.json)
        try:
            self.messenger = DirectMessenger(
                server_host=host,
                server_port=port,
                username=username,
                password=password
            )
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect/authenticate:\n{e}")
            self.destroy()
            return

        # 3) Use the same Notebook the messenger has
        self.notebook = self.messenger.notebook
        self.username = username

        # 4) Build the UI
        self._build_ui()

        # 5) Load existing contacts into the tree
        self._load_contacts()

        # 6) Start polling for new messages
        self.after(self.POLL_INTERVAL, self._poll_new)

    def _build_ui(self):
        paned = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # --- Left: contacts ---
        left = ttk.Frame(paned, width=150)
        paned.add(left, weight=1)
        self.tree = ttk.Treeview(left, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_contact_select)
        ttk.Button(left, text="Add Contact", command=self._add_contact).pack(fill=tk.X)

        # --- Right: chat display + entry ---
        right = ttk.Frame(paned)
        paned.add(right, weight=3)

        self.chat_display = tk.Text(right, state="disabled", wrap="word")
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        entry_frame = ttk.Frame(right)
        entry_frame.pack(fill=tk.X)
        self.msg_entry = ttk.Entry(entry_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(entry_frame, text="Send", command=self._send_message).pack(side=tk.RIGHT)

        # --- Status bar ---
        self.status = ttk.Label(self, text="Ready.")
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

        # --- Styling tags ---
        self.chat_display.tag_config("incoming", justify="left", foreground="blue")
        self.chat_display.tag_config("outgoing", justify="right", foreground="green")

    def _load_contacts(self):
        for user in self.notebook.get_contacts():
            if not self.tree.exists(user):
                self.tree.insert("", "end", iid=user, text=user)

    def _on_contact_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        self.current = sel[0]
        self._show_messages(self.current)

    def _show_messages(self, contact):
        msgs = self.notebook.get_messages(contact)
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        for m in msgs:
            tag = "outgoing" if m["sender"] == self.username else "incoming"
            line = f"{m['sender']}: {m['message']}\n"
            self.chat_display.insert(tk.END, line, tag)
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def _add_contact(self):
        new_user = simpledialog.askstring("Add Contact", "Enter username:")
        if new_user:
            self.notebook.add_contact(new_user)
            if not self.tree.exists(new_user):
                self.tree.insert("", "end", iid=new_user, text=new_user)

    def _send_message(self):
        if not hasattr(self, "current"):
            messagebox.showwarning("No Contact", "Please select a contact first.")
            return

        text = self.msg_entry.get().strip()
        if not text:
            return

        success = self.messenger.send(text, self.current)
        if success:
            # locally reflect the sent message
            dm = DirectMessage(
                sender=self.username,
                recipient=self.current,
                message=text,
                timestamp=str(time.time())
            )
            self.notebook.add_message(dm)
            self._show_messages(self.current)
            self.msg_entry.delete(0, tk.END)
            self.status.config(text="Message sent.")
        else:
            self.status.config(text="Send failed.")

    def _poll_new(self):
        try:
            new_msgs = self.messenger.retrieve_new()
            if new_msgs:
                for dm in new_msgs:
                    # ensure contact is in the tree
                    if not self.tree.exists(dm.sender):
                        self.tree.insert("", "end", iid=dm.sender, text=dm.sender)
                    # if currently viewing that contact, refresh
                    if getattr(self, "current", None) == dm.sender:
                        self._show_messages(dm.sender)
                self.status.config(text=f"{len(new_msgs)} new message(s).")
            else:
                self.status.config(text="No new messages.")
        except Exception as e:
            self.status.config(text=f"Error fetching: {e}")
        finally:
