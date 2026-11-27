from getpass import getpass

from auth import hash_password
from database import save_user

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

    password_hash = hash_password(password)
    return User(email, username, password_hash, "user")


def register():
    user = create_user()
    save_user(user)