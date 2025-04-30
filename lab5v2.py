#lab5.py

# Starter code for lab 5 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chloe Chow
# ccchow2@uci.edu
# 62088321

# ---------------------

'''
from pathlib import Path

class Note:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_notes(self) -> list[str]:
        with self.file_path.open("r", encoding="utf-8") as file:
            notes = [line.strip() for line in file.readlines()]
        return notes

    def save_note(self, note: str) -> None:
        with self.file_path.open("a", encoding="utf-8") as file:
            file.write(note + "\n")

    def remove_note(self, note_id: int) -> str:
        notes = self.read_notes()
        if 0 <= note_id < len(notes):
            removed_note = notes.pop(note_id)
            with self.file_path.open("w", encoding="utf-8") as file:
                for note in notes:
                    file.write(note + "\n")
            return removed_note
        else:
            raise ValueError("Invalid note ID")

'''

# ---------------------
from pathlib import Path

NOTES_PATH = "."
NOTES_FILE = "pynote.txt"

def print_notes(notes:list[str]):
    id = 0
    for n in notes:
        print(f"{id}: {n}")
        id+=1

def delete_note(note:Note):
    try:
        remove_id = input("Enter the number of the note you would like to remove: ")
        remove_note = note.remove_note(int(remove_id))
        print(f"The following note has been removed: \n\n {remove_note}")
    except FileNotFoundError:
        print("The PyNote.txt file no longer exists")
    except ValueError:
        print("The value you have entered is not a valid integer")

def run():
    p = Path(NOTES_PATH) / NOTES_FILE
    if not p.exists():
        p.touch()
    note = Note(p)
    
    print("Here are your notes: \n")
    print_notes(note.read_notes())

    user_input = input("Please enter a note (enter :d to delete a note or :q to exit):  ")

    if user_input == ":d":
        delete_note(note)
    elif user_input == ":q":
        return
    else:    
        note.save_note(user_input)
    run()


if __name__ == "__main__":
    print("Welcome to PyNote! \n")

    run()
    
