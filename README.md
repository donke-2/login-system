# Python CLI Login System

A command-line login system built with Python and SQLite. Users can register an account, restart the program, and sign in with the same credentials. Password entry is hidden in the terminal, and passwords are stored as salted Argon2id hashes.

## Features

- Register with a unique email address and username.
- Verify passwords with `argon2-cffi` and look up accounts using parameterised SQL queries.
- Retry an incorrect password or return to the main menu.
- Pause login attempts for 10 minutes after five incorrect passwords and display the remaining time.

## Run locally

You’ll need Git and Python 3.10 or later. Run these commands in Windows PowerShell:

```powershell
git clone https://github.com/donke-2/login-system.git
cd login-system
py -m pip install argon2-cffi
New-Item -ItemType Directory -Force data
py main.py
```

The program creates `data/user_data.db` on the first run.

## Try it

1. Choose **3. Register** and create a test account.
2. Choose **4. Exit**, then run `py main.py` again.
3. Choose **1. Login** and sign in with your test account to confirm that registration persisted.
4. To test the cooldown, enter five incorrect passwords for an existing username. Choose **Login** again to see the remaining time.

## How the cooldown works

The program keeps one failure counter and one unlock time in memory, shared across all accounts. A successful login resets the failure counter. The fifth incorrect password starts a ten-minute cooldown and returns the user to the main menu.

Restarting the program clears the counter and cooldown. Registered accounts persist in SQLite.

## Planned features

- Per-account cooldowns stored in SQLite so they survive restarts.
- Password recovery with expiring, single-use codes. The **Forgot Password?** menu option is currently a placeholder.
- An admin-only view of login activity.
- Compromised-password checks during registration and password resets.