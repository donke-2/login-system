import sqlite3
from enum import Enum
from getpass import getpass

# Menu 
class MenuOption(Enum):
    REGESTER = 1
    LOGIN = 2
    RESET_PW = 3
    EXIT = 4

def input(prompt, lower, upper):
    choice = input(prompt)
    if choice < lower or choice > upper:
        return 0
    else:
        return choice

# Database 
def createTables():
    connection = sqlite3.connect("data/userData.db")
    try:
        connection.execute("""
        CREATE TABLE IF NOT EXIST userData 
        (
            id INTEGER PRIMARY KEY, 
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            pw TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT "user"
        )
        """)
        connection.commit

    finally:
        connection.close

# user creation
class user():
    def __init__(self, email, username, pw, role):
        self.email = email
        self.username = username
        self.pw = pw
        self.role = role

def createUser():
    email = input("Email: ")
    username = input("Username: ")
    
    while True:
        pw = input("Password: ") 
        if pw is None:
            print("Enter a password.")
        elif pw is not None:
            pwCheck = input("Enter password again to confirm: ")
            break

    pwHash = hash(pw)

    return user(email, username, pwHash, "user")

def saveUser(user):
    connection = sqlite3.connect("data/userData.db")
    try:
        connection.execute(
            "INSERT INTO users (email, username, pw) VALUES (?, ?, ?)",
            (user.email, user.usermame, user.pwHash) 
        )
        connection.commit()

    finally:
        connection.close()
  
# Printing functions
def printMenu():
    print("----- Login -----")
    print("1. Login")
    print("2. Register")
    print("3. Forgot Password?")
    print("4. Exit")

# Option Functions
def register():
    user = createUser()
    saveUser(user)

def login():
    usernameIn = input("Username: ")
    pwIn = input("Password: ")

def resetPw():
    email = input("Enter email for recovery")


# driver
def main():

    createTables()

    while True:
        printMenu()

        option = input("Choose an option: ")

        match option:
            case MenuOption.REGISTER.value:
                register()

            case MenuOption.LOGIN.value:
                login()

            case MenuOption.RESET_PW.value:
               resetPw()

            case MenuOption.EXIT.value:
                break

            case _:
                print("Invalid option")

if __name__ == "__main__":
    main()

