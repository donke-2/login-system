import sqlite3
from enum import Enum
from getpass import getpass
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()

# Menu 
class MenuOption(Enum):
    LOGIN = "1"
    FORGOT_LOGIN = "2"
    REGISTER = "3"
    EXIT = "4"

class WrongUsername(Enum):
    RETRY_USERNAME = "1"
    BACK = "2"

class WrongPassword(Enum):
    RETRY_PASSWORD = "1"
    BACK = "2"

# Database 
def createTables():
    connection = sqlite3.connect("data/userData.db")
    try:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS userData
        (
            id INTEGER PRIMARY KEY, 
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            pw TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT "user"
        )
        """)
        connection.commit()

    finally:
        connection.close()

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
        pw = getpass("Password: ") 

        if pw is None:
            getpass("Enter a password.")

        else:
            pwCheck = getpass("Enter password again to confirm: ")

            while pw != pwCheck:
                pwCheck = getpass("Enter password again to confirm: ")
            break

    pwHash = hasher.hash(pw)
    return user(email, username, pwHash, "user")

def saveUser(user):
    connection = sqlite3.connect("data/userData.db")
    try:
        connection.execute(
            "INSERT INTO userData (email, username, pw) VALUES (?, ?, ?)",
            (user.email, user.username, user.pw) 
        )
        connection.commit()

    finally:
        connection.close()
  
# Printing functions
def printMenu():
    print("----- Login -----")
    print("1. Login")
    print("2. Forgot Password?")
    print("3. Register")
    print("4. Exit")

# Option Functions

# Option 1 (Login)
def verify_pws(hashed_pw, pwIn):
    try:
        return hasher.verify(hashed_pw, pwIn)
    except VerifyMismatchError:
        return False
    
def login():
    connection = sqlite3.connect("data/userData.db")

    try:
        # Checks if username is linked to a valid account
        usernameIn = input("Username: ")

        userCheck = connection.execute(
            "SELECT username FROM userData WHERE username = ?",
            (usernameIn,)
        ).fetchone()

        while userCheck is None:
            print("Invalid username. Try again")

            print("1. Retry username")
            print("2. Back")
            choice = input("Enter an option: ")

            match choice:
                case WrongUsername.RETRY_USERNAME.value:
                    usernameIn = input("Username: ")
                    userCheck = connection.execute(
                        "SELECT username FROM userData WHERE username = ?",
                        (usernameIn,)
                    ).fetchone

                case WrongUsername.BACK.value:
                    return

                case _:
                    print("invalid option")

        # password check
        pwIn = getpass("Password: ")

        pwCheck = connection.execute(
            "SELECT pw FROM userData WHERE username = ?",
            (usernameIn,)
        ).fetchone()
        
        while not verify_pws(pwCheck[0], pwIn):
            print("Incorrect password. Try again")
        
            print("1. Retry password")
            print("2. Back")

            choice = input("Enter an option: ")
        
            match choice:
                case WrongPassword.RETRY_PASSWORD.value:
                    pwIn = getpass("Password: ")
        
                case WrongPassword.BACK.value:
                    return
        
                case _:
                    print("invalid option")

        print("success.")

    finally:
            connection.close()

# Option 2 (Forget Password)
def forgotLogin():
    print("")

# Option 3 (Register)
def register():
    user = createUser()
    saveUser(user)

# driver
def main():

    # Creates the tables in the db
    createTables()

    while True:
        printMenu()

        option = input("Choose an option: ")

        match option:

            case MenuOption.LOGIN.value:
                login()

            case MenuOption.FORGOT_LOGIN.value:
               forgotLogin()

            case MenuOption.REGISTER.value:
                register()

            case MenuOption.EXIT.value:
                break

            case _:
                print("Invalid option.")

if __name__ == "__main__":
    main()

