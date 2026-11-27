from enum import Enum

import actions


# Menu options
class MenuOption(Enum):
    LOGIN = "1"
    FORGOT_PASSWORD = "2"
    REGISTER = "3"
    EXIT = "4"


# Printing functions
def print_menu():
    print("----- Login -----")
    print("1. Login")
    print("2. Forgot Password?")
    print("3. Register")
    print("4. Exit")


def print_invalid_username():
    print("Invalid username. Try again.")
    print("1. Retry username")
    print("2. Back")


def print_invalid_password():
    print("Incorrect password. Try again.")
    print("1. Retry password")
    print("2. Back")


# Main menu loop
def main_menu():
    while True:
        print_menu()
        option = input("Choose an option: ")

        match option:
            case MenuOption.LOGIN.value:
                actions.login()

            case MenuOption.FORGOT_PASSWORD.value:
                actions.reset_password()

            case MenuOption.REGISTER.value:
                actions.register()

            case MenuOption.EXIT.value:
                break

            case _:
                print("Invalid option.")