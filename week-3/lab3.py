#lab3.py

# Starter code for lab 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chloe Chow
# ccchow2@uci.edu
# 62088321

FILENAME = "pynote.txt"

def read_notes():
    try:
        with open(FILENAME, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        with open(FILENAME, 'w') as f:
            pass
        return []

def print_notes(notes):
    print("Welcome to PyNote!")
    print("Here are your notes:\n")
    for note in notes:
        print(note.strip())
        print()
    print()

def add_note(note):
    with open(FILENAME, 'a') as f:
        f.write(note + '\n')
        
def main():
    notes = read_notes()
    print_notes(notes)

    while True:
        note = input("Please enter a new note (enter q to exit): ")
        if note == "q":
            break
        add_note(note)

main()
