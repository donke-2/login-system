from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()


# returns the hash of a password
def hash_password(password):
    return hasher.hash(password)


# Verifys that the hash of an inputted password matches its coressponding hash from the database
def verify_password(password_hash, password):
    try:
        return hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False