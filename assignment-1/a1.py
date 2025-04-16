# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321

import shlex
from pathlib import Path
from notebook import Notebook, NotebookFileError
from command_parser import parse_command
from notebook import Diary

def create_notebook(args: list[str]):
    if len(args) < 4 or "-n" not in args:
        print("ERROR")
        return

    try:
        name_index = args.index("-n")
        path_input = args[1]
        name_input = args[name_index + 1]

        # Convert to full path with pathlib
        path = Path(path_input)
        if not path.exists() or not path.is_dir():
            print("ERROR")
            return

        file_path = path / f"{name_input}.json"
        if file_path.exists():
            print("ERROR")
            return

        # Prompt for user info
        username = input("")
        password = input("")
        bio = input("")

        # Create and save the notebook
        nb = Notebook(username, password, bio)
        nb.save(file_path)

        print(str(file_path.resolve()) + " CREATED")

    except Exception:
        print("ERROR")

def delete_notebook(args: list[str]):
    if len(args) != 2:
        print("ERROR")
        return

    try:
        path = Path(args[1])
        if not path.exists() or path.suffix != '.json' or not path.is_file():
            print("ERROR")
            return

        path.unlink()  # Delete the file
        print(f"{path.resolve()} DELETED")

    except Exception:
        print("ERROR")

def load_notebook(args):
    if len(args) < 2:
        print("ERROR")
        return None, None

    try:
        file_path = Path(args[1])
        if not file_path.exists() or file_path.suffix != ".json":
            print("ERROR")
            return None, None

        username = input("")
        password = input("")

        nb = Notebook("", "", "")  # placeholder init
        nb.load(file_path)

        if nb.username == username and nb.password == password:
            print("Notebook loaded.")
            print(nb.username)
            print(nb.bio)
            return nb, file_path  # return both the object and path for later reuse
        else:
            print("ERROR")
            return None, None

    except (NotebookFileError, IncorrectNotebookError, Exception):
        print("ERROR")
        return None, None

def edit_notebook(args, nb, path):
    if nb is None or path is None:
        print("ERROR")
        return

    try:
        i = 1  # Skip the "E"
        while i < len(args):
            option = args[i]

            if option == "-usr" and i + 1 < len(args):
                nb.username = args[i + 1]
                nb.save(path)
                i += 2
            elif option == "-pwd" and i + 1 < len(args):
                nb.password = args[i + 1]
                nb.save(path)
                i += 2
            elif option == "-bio" and i + 1 < len(args):
                nb.bio = args[i + 1]
                nb.save(path)
                i += 2
            elif option == "-add" and i + 1 < len(args):
                new_diary = Diary(args[i + 1])
                nb.add_diary(new_diary)
                nb.save(path)
                i += 2
            elif option == "-del" and i + 1 < len(args):
                try:
                    index = int(args[i + 1])
                    success = nb.del_diary(index)
                    if not success:
                        print("ERROR")
                        return
                    nb.save(path)
                    i += 2
                except:
                    print("ERROR")
                    return
            else:
                print("ERROR")
                return
    except Exception:
        print("ERROR")

def print_notebook(args, nb):
    if nb is None:
        print("ERROR")
        return

    try:
        i = 1
        while i < len(args):
            option = args[i]

            if option == "-usr":
                print(nb.username)
                i += 1
            elif option == "-pwd":
                print(nb.password)
                i += 1
            elif option == "-bio":
                print(nb.bio)
                i += 1
            elif option == "-diaries":
                for idx, d in enumerate(nb.get_diaries()):
                    print(f"{idx}: {d.entry}")
                i += 1
            elif option == "-diary" and i + 1 < len(args):
                try:
                    idx = int(args[i + 1])
                    print(nb.get_diaries()[idx].entry)
                    i += 2
                except:
                    print("ERROR")
                    return
            elif option == "-all":
                print(nb.username)
                print(nb.password)
                print(nb.bio)
                for idx, d in enumerate(nb.get_diaries()):
                    print(f"{idx}: {d.entry}")
                i += 1
            else:
                print("ERROR")
                return
    except Exception:
        print("ERROR")

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
