#lab2.py

# Starter code for lab 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chloe Chow
# ccchow2@uci.edu
# 62088321

def add(a, b):
    return  a + b

def sub(a, b):
    return  a - b

def div(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "The right operand cannot be 0"

def mul(a, b):
    return  a * b

def get_operator():
    while True:
        operator = input("What type of calculation would you like to perform (+, -, x, /)? ")
        if operator in ("+", "-", "x", "/"):
            return operator
        else:
            print("Invalid operator. Please choose from +, -, x, or /.")

def run():
    try:
        a = int(input("Enter left operand: "))
        b = int(input("Enter right operand: "))
    except ValueError:
        print("Please enter valid integers.")
        run()
        return

    operator = get_operator()

    if operator == "+":
        r = add(a, b)
    elif operator == "-":
        r = sub(a, b)
    elif operator == "x":
        r = mul(a, b)
    elif operator == "/":
        r = div(a, b)
    
    print(r)
    
    if input("Run another calculation (y/n)? ") == "y":
        run()


if __name__ == "__main__":
    print("Welcome to PyCalc!")
    run()
