import sqlite3
from enum import Enum
from getpass import getpass

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()


# Menu options
class MenuOption(Enum):
    LOGIN = "1"
    FORGOT_PASSWORD = "2"
    REGISTER = "3"
    EXIT = "4"

class WrongUsername(Enum):
    RETRY_USERNAME = "1"
    BACK = "2"

class WrongPassword(Enum):
    RETRY_PASSWORD = "1"
    BACK = "2"


# Database
def create_tables():
    connection = sqlite3.connect("data/userData.db")

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS userData (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)
        connection.commit()
    finally:
        connection.close()


# User creation
class User:
    def __init__(self, email, username, password_hash, role):
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.role = role


def create_user():
    email = input("Email: ")
    username = input("Username: ")

    while True:
        password = getpass("Password: ")

        if not password:
            print("Enter a password.")
            continue

        password_confirmation = getpass("Enter password again to confirm: ")

        if password == password_confirmation:
            break

        print("Passwords do not match. Try again.")

    password_hash = hasher.hash(password)
    return User(email, username, password_hash, "user")


def save_user(user):
    connection = sqlite3.connect("data/userData.db")

    try:
        connection.execute(
            "INSERT INTO userData (email, username, password) VALUES (?, ?, ?)",
            (user.email, user.username, user.password_hash),
        )
        connection.commit()
    finally:
        connection.close()


# Main menu
def print_menu():
    print("----- Login -----")
    print("1. Login")
    print("2. Forgot Password?")
    print("3. Register")
    print("4. Exit")


# Option 1 (Login)
def verify_password(password_hash, password):
    try:
        return hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def login():
    connection = sqlite3.connect("data/userData.db")

    try:
        username = input("Username: ")

        # Fetch the password hash for the entered username.
        user_row = connection.execute(
            "SELECT password FROM userData WHERE username = ?",
            (username,),
        ).fetchone()

        while user_row is None:
            print("Invalid username. Try again.")
            print("1. Retry username")
            print("2. Back")
            choice = input("Enter an option: ")

            match choice:
                case WrongUsername.RETRY_USERNAME.value:
                    username = input("Username: ")
                    user_row = connection.execute(
                        "SELECT password FROM userData WHERE username = ?",
                        (username,),
                    ).fetchone()

                case WrongUsername.BACK.value:
                    return

                case _:
                    print("Invalid option.")

        password_hash = user_row[0]
        password = getpass("Password: ")

        while not verify_password(password_hash, password):
            print("Incorrect password. Try again.")
            print("1. Retry password")
            print("2. Back")
            choice = input("Enter an option: ")

            match choice:
                case WrongPassword.RETRY_PASSWORD.value:
                    password = getpass("Password: ")

                case WrongPassword.BACK.value:
                    return

                case _:
                    print("Invalid option.")

        print("Success.")
    finally:
        connection.close()


# Option 2 (Forgot password)
def forgot_password():
    print("")


# Option 3 (Register)
def register():
    user = create_user()
    save_user(user)


def main():
    create_tables()

    while True:
        print_menu()
        option = input("Choose an option: ")

        match option:
            case MenuOption.LOGIN.value:
                login()

            case MenuOption.FORGOT_PASSWORD.value:
                forgot_password()

            case MenuOption.REGISTER.value:
                register()

            case MenuOption.EXIT.value:
                break

            case _:
                print("Invalid option.")


if __name__ == "__main__":
    main()