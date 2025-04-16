# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321

import shlex
from command_parser import (
    create_notebook,
    load_notebook,
    edit_notebook,
    print_notebook
)

def main():
    loaded_notebook = None
    notebook_path = None

    while True:
        try:
            raw = input("")
            if not raw.strip():
                continue

            args = shlex.split(raw)
            if len(args) == 0:
                continue

            cmd = args[0].upper()

            if cmd == "Q":
                break
            elif cmd == "C":
                create_notebook(args)
            elif cmd == "O":
                loaded_notebook, notebook_path = load_notebook(args)
            elif cmd == "E":
                edit_notebook(args, loaded_notebook, notebook_path)
            elif cmd == "P":
                print_notebook(args, loaded_notebook)
            else:
                print("ERROR")
        except EOFError:
            break

if __name__ == "__main__":
    main()
