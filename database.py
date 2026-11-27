import sqlite3


# Creates the SQL tables in the database
def create_tables():
    connection = sqlite3.connect("data/database.db")

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                outcome TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


# Saves the users details into a row in the user_data table
def save_user(user):
    connection = sqlite3.connect("data/database.db")

    try:
        connection.execute(
            "INSERT INTO user_data (email, username, password) VALUES (?, ?, ?)",
            (user.email, user.username, user.password_hash),
        )
        connection.commit()

    finally:
        connection.close()


# Saves the details of a login attempt into a row in the login_attemps table
def login_attempt(username, outcome):
    connection = sqlite3.connect("data/database.db")

    try:
        connection.execute(
            "INSERT INTO login_attempts (username, outcome) VALUES (?, ?)",
            (username, outcome)
        )
        connection.commit()

    finally:
        connection.close()