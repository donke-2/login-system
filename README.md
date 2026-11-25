# Python CLI Login System

A small authentication project built with Python and SQLite. Users can register from the terminal, close the program, and sign in again with the same credentials. Password prompts are hidden, and the database stores salted Argon2id password hashes.

## Run locally

The following commands use Windows PowerShell, Git, and Python 3.10 or later. From a fresh clone, create the `data` folder before starting the program. SQLite creates `data/userData.db` on the first run.

```powershell
git clone https://github.com/donke-2/login-system.git
cd login-system
py -m pip install argon2-cffi
New-Item -ItemType Directory -Force data
py main.py
```

## Try the login flow

1. Choose **3. Register** and enter a test email, a username, and a password. Confirm the password when prompted.
2. Choose **4. Exit**, then run `py main.py` again.
3. Choose **1. Login** and enter the username you registered. Try a wrong password, select **1. Retry password**, then enter the correct one. The program prints `success.` and returns to the menu.

## How it works

- **Registration** uses `getpass` for password entry and `argon2-cffi` to hash the confirmed password. SQLite enforces unique usernames and email addresses.
- **Login** uses a parameterised SQL query to retrieve the stored hash. Argon2 verifies the entered password against it, and a mismatch opens the retry menu.

## Planned features

- Password recovery with expiring, single-use codes. The **Forgot Password?** menu option is currently a placeholder.
- A ten-minute cooldown after five failed login attempts.
- An admin-only view of login activity.
- Compromised-password checks during registration and password resets.
