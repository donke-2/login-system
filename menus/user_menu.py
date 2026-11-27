import sqlite3
from enum import Enum

class menu_options(Enum):
    LOGOUT = "1"



def print_menu():
    print("1. Logout")


def user_menu(username):
    connection = sqlite3.connect("data/database.db")

    try:
        username = connection.execute(
            "SELECT username FROM user_data WHERE username = ?",
            (username,),
            ).fetchone()

        print(f"Welcome {username[0]}!")

        print("")

        print_menu()

        option = input("Enter an option: ")

        match option:

            case menu_options.LOGOUT.value:
                return

    finally:
        connection.close()
