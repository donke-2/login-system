import sqlite3
import time
from enum import Enum
from getpass import getpass

from auth import verify_password
import database
from menus.user_menu import user_menu
from menus.admin_menu import admin_menu


# Constants
MAX_ATTEMPS = 5


# Global variables
failed_attemps = 0
locked_until = 0


def record_failure():
    global failed_attemps
    failed_attemps += 1


def start_lockout():
    global locked_until, failed_attemps
    locked_until = int(time.time()) + (60 * 10)
    failed_attemps = 0


# Menu enumerations
class WrongUsername(Enum):
    RETRY_USERNAME = "1"
    BACK = "2"


class WrongPassword(Enum):
    RETRY_PASSWORD = "1"
    BACK = "2"


# Printing functions
def print_invalid_username():
    print("Invalid username. Try again.")
    print("1. Retry username")
    print("2. Back")


def print_invalid_password():
    print("Incorrect password. Try again.")
    print("1. Retry password")
    print("2. Back")


def login():
    global failed_attemps

    time_left = locked_until - int(time.time())

    if time_left > 0:
        print(f"Try again in {time_left} seconds.")
        return

    connection = sqlite3.connect("data/database.db")

    try:
        username = input("Username: ")

        # Fetch the password hash for the entered username.
        user_row = connection.execute(
            "SELECT password FROM user_data WHERE username = ?",
            (username,),
        ).fetchone()

        while user_row is None:
            print_invalid_username()
            choice = input("Enter an option: ")

            match choice:
                case WrongUsername.RETRY_USERNAME.value:
                    username = input("Username: ")
                    user_row = connection.execute(
                        "SELECT password FROM user_data WHERE username = ?",
                        (username,),
                    ).fetchone()

                case WrongUsername.BACK.value:
                    return

                case _:
                    print("Invalid option.")

        password_hash = user_row[0]
        password = getpass("Password: ")

        while not verify_password(password_hash, password):
            record_failure()

            if failed_attemps >= MAX_ATTEMPS:
                start_lockout()

                database.login_attempt(username, "TIMED OUT.")
                print("Too many attemps. Try again later.")
                return

            database.login_attempt(username, "UNSUCCESSFUL")

            print_invalid_password()
            choice = input("Enter an option: ")

            while choice not in ("1", "2"):
                print("Invalid option.")
                choice = input("Enter an option: ")

            match choice:
                case WrongPassword.RETRY_PASSWORD.value:
                    password = getpass("Password: ")

                case WrongPassword.BACK.value:
                    return

        database.login_attempt(username, "SUCCESSFUL")
        failed_attemps = 0

        role = connection.execute(
        "SELECT role FROM user_data WHERE username = ?",
        (username,),
        ).fetchone()

        if role is None:
            print("User not found")
        else:
    
            if role[0] == "user":
                user_menu(username)

            elif role[0] == "admin":
                admin_menu(username)

            else:
                print(f"Unknown role: {role}")

    finally:
        connection.close()