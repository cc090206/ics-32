# lab8v2.py

# Starter code for lab 8 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Chloe Chow
# ccchow2@uci.edu
# 62088321


from abc import ABC, abstractmethod
import random


class Appetite:
    LOW = 3
    MEDIUM = 4
    HIGH = 5


class Dog(ABC):
    def __init__(self, name, age, appetite=Appetite.MEDIUM):
        self._name = name
        self._age = age
        self.hunger_clock = 0
        self.appetite = appetite

    def name(self):
        return self._name

    def age(self):
        return self._age

    def hungry(self):
        if self.hunger_clock > self.appetite:
            return bool(random.getrandbits(1))
        else:
            self.hunger_clock += 1
            return False

    def feed(self):
        self.hunger_clock = 0

    @abstractmethod
    def breed(self):
        pass


class GermanShepherd(Dog):
    def breed(self):
        return "German Shepherd"


class Poodle(Dog):
    def breed(self):
        return "Poodle"


class Bulldog(Dog):
    def breed(self):
        return "Bulldog"


def choose_dog():
    print("Welcome to the Dog Feeder 3000!")
    name = input("What is your dog's name? ")
    age = int(input("How old is your dog? "))
    print("Choose your dog's breed:")
    print("1. German Shepherd")
    print("2. Poodle")
    print("3. Bulldog")
    breed_choice = input("Enter the number: ")

    print("Choose appetite level:")
    print("1. Low")
    print("2. Medium")
    print("3. High")
    appetite_choice = input("Enter the number: ")
    appetite_map = {"1": Appetite.LOW, "2": Appetite.MEDIUM, "3": Appetite.HIGH}
    appetite = appetite_map.get(appetite_choice, Appetite.MEDIUM)

    if breed_choice == "1":
        return GermanShepherd(name, age, appetite)
    elif breed_choice == "2":
        return Poodle(name, age, appetite)
    elif breed_choice == "3":
        return Bulldog(name, age, appetite)
    else:
        print("Invalid breed. Defaulting to German Shepherd.")
        return GermanShepherd(name, age, appetite)


if __name__ == "__main__":
    dog = choose_dog()

    while True:
        h_text = "" if dog.hungry() else "not "
        print(f"Your {dog.breed()}, {dog.name()} is {h_text}hungry.")
        feed = input(f"Would you like to feed {dog.name()}? (y/n/q): ")

        if feed == "y":
            dog.feed()
        elif feed == "q":
            print(f"Goodbye! {dog.name()} waves their paw.")
            break
