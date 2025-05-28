# a3.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321
#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog, messagebox
from ds_messenger import DirectMessenger
from gui import ChatUI

def main():
    # --- hide the main window while we log in ---
    root = tk.Tk()
    root.withdraw()

    # --- get credentials ---
    username = simpledialog.askstring("Login", "Username:")
    if not username:
        messagebox.showerror("Error", "Username required")
        return

    password = simpledialog.askstring("Login", "Password:", show="*")
    if not password:
        messagebox.showerror("Error", "Password required")
        return

    # --- connect & authenticate (also loads <username>_notebook.json) ---
    try:
        messenger = DirectMessenger(
            server_host="localhost",
            server_port=3001,
            username=username,
            password=password
        )
    except RuntimeError as e:
        messagebox.showerror("Authentication Failed", str(e))
        return

    # --- ready to show chat UI ---
    root.deiconify()
    app = ChatUI(root, messenger)
    app.load_history()    # populate UI from messenger.notebook
    app.poll_new()        # start polling for new messages
    app.run()             # enter mainloop()

if __name__ == "__main__":
    main()