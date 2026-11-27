# Python CLI Login System

A command-line login system built with Python and SQLite. Users can register, sign in, and reach a menu based on their role. Passwords are stored as salted Argon2id hashes, password entry is hidden in the terminal, and every login attempt is recorded.

## Features

- Register with a unique email address and username.
- Hash passwords with Argon2id (`argon2-cffi`) and never store them in plain text.
- Look up accounts using parameterised SQL queries to prevent SQL injection.
- Retry an incorrect username or password, or return to the main menu.
- Pause login attempts for 10 minutes after five incorrect passwords and show the time remaining.
- Record every login attempt (successful, unsuccessful or timed out) with a timestamp.
- Send users and admins to separate menus after login.
- Let admins view the login log as a formatted table.

## Run locally

You'll need Git and Python 3.10 or later. Run these commands in Windows PowerShell:

```powershell
git clone https://github.com/donke-2/login-system.git
cd login-system
py -m pip install -r requirements.txt
New-Item -ItemType Directory -Force data
py main.py
```

The program creates `data/database.db` on the first run.

## Try it

1. Choose **3. Register** and create a test account.
2. Choose **4. Exit**, then run `py main.py` again.
3. Choose **1. Login** and sign in with your test account to confirm that registration persisted.
4. To test the cooldown, enter five incorrect passwords for an existing username. Choose **Login** again to see the remaining time.

### Make an admin account

New accounts get the `user` role. To make one an admin, register it first, then run:

```powershell
py -c "import sqlite3; c = sqlite3.connect('data/database.db'); c.execute(\"UPDATE user_data SET role = 'admin' WHERE username = 'YOUR_USERNAME'\"); c.commit()"
```

Log in with that account and choose **View Login Log**.

## Tests

The tests use `pytest` and cover the authentication, database and lockout logic. Each test runs against a temporary database, so your real `data/database.db` is never touched.

Install the dependencies first (see **Run locally**), then run:

```powershell
py -m pytest -v
```

| File | What it checks |
|---|---|
| `test_auth.py` | Correct passwords verify, wrong ones are rejected, hashes are salted (the same password gives different hashes), hashes use Argon2id, and the plain-text password never appears in the hash |
| `test_database.py` | Users save and read back correctly, passwords are stored as hashes, duplicate usernames and emails are rejected, login attempts are logged, and a SQL injection payload (`' OR '1'='1`) matches no users |
| `test_lockout.py` | Failed attempts are counted, five failures start a 10-minute cooldown and reset the counter, and login refuses input while the cooldown is active |

The test files were written by Claude (Anthropic) and reviewed by me.

## Project structure

```
login-system/
â”œâ”€â”€ main.py            # Entry point: creates tables, starts the main menu
â”œâ”€â”€ auth.py            # Argon2id hashing and verification
â”œâ”€â”€ database.py        # Table creation, saving users, logging attempts
â”œâ”€â”€ conftest.py        # Lets pytest import the project's modules
â”œâ”€â”€ requirements.txt   # Python dependencies
â”œâ”€â”€ actions/
â”‚   â”œâ”€â”€ login.py       # Login flow, retries and cooldown
â”‚   â”œâ”€â”€ register.py    # Registration flow
â”‚   â””â”€â”€ reset_password.py
â”œâ”€â”€ menus/
â”‚   â”œâ”€â”€ main_menu.py   # Login / Forgot Password / Register / Exit
â”‚   â”œâ”€â”€ user_menu.py   # Menu for standard users
â”‚   â””â”€â”€ admin_menu.py  # Menu for admins, including the login log
â””â”€â”€ tests/
    â”œâ”€â”€ test_auth.py
    â”œâ”€â”€ test_database.py
    â””â”€â”€ test_lockout.py
```

## Database

| Table | Columns |
|---|---|
| `user_data` | `id`, `email` (unique), `username` (unique), `password` (Argon2id hash), `role` (`user` or `admin`) |
| `login_attempts` | `id`, `username`, `time` (UTC), `outcome` |

## How the cooldown works

The program keeps one failure counter and one unlock time in memory, shared across all accounts. A successful login resets the counter. The fifth incorrect password starts a ten-minute cooldown and returns the user to the main menu.

Restarting the program clears the counter and cooldown. Accounts and the login log persist in SQLite.

## Planned features

- Per-account cooldowns stored in SQLite so they survive restarts.
- Password recovery with expiring, single-use codes. The **Forgot Password?** option is currently a placeholder.
- Compromised-password checks during registration and password resets.
- Input validation for email addresses and empty usernames.
