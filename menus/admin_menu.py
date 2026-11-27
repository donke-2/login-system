import sqlite3
from enum import Enum

from tabulate import tabulate

class menu_options(Enum):
    VIEW_LOG = "1"
    LOGOUT = "2"


def print_menu():
    print("1. View Login Log")
    print("2. Logout")


def view_log():
    connection = sqlite3.connect("data/database.db")

    try:
        table = connection.execute("SELECT * FROM login_attempts")
        headers = [col[0] for col in table.description]
        print(tabulate(table.fetchall(), headers=headers, tablefmt="grid"))

    finally:
        connection.close()


def admin_menu(username):
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

            case menu_options.VIEW_LOG.value:
                view_log()

            case menu_options.LOGOUT.value:
                return

    finally:
        connection.close()
