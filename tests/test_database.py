# Tests written by Claude (Anthropic) and reviewed by Richard Taing.

import sqlite3
from types import SimpleNamespace

import pytest

import database
from auth import hash_password


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    # The code uses the relative path "data/database.db", so running each
    # test inside a fresh temp folder keeps the real database untouched.
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    database.create_tables()


def make_user(email="a@test.com", username="alice", password="pw"):
    return SimpleNamespace(
        email=email,
        username=username,
        password_hash=hash_password(password),
        role="user",
    )


def query(sql, params=()):
    connection = sqlite3.connect("data/database.db")
    try:
        return connection.execute(sql, params).fetchall()
    finally:
        connection.close()


def test_saved_user_can_be_read_back():
    database.save_user(make_user())
    rows = query("SELECT email, username, role FROM user_data")
    assert rows == [("a@test.com", "alice", "user")]


def test_password_stored_as_hash_not_plaintext():
    database.save_user(make_user(password="secret123"))
    stored = query("SELECT password FROM user_data")[0][0]
    assert stored != "secret123"
    assert stored.startswith("$argon2id$")


def test_duplicate_username_rejected():
    database.save_user(make_user())
    with pytest.raises(sqlite3.IntegrityError):
        database.save_user(make_user(email="other@test.com"))


def test_duplicate_email_rejected():
    database.save_user(make_user())
    with pytest.raises(sqlite3.IntegrityError):
        database.save_user(make_user(username="bob"))


def test_login_attempt_is_logged():
    database.login_attempt("alice", "UNSUCCESSFUL")
    rows = query("SELECT username, outcome FROM login_attempts")
    assert rows == [("alice", "UNSUCCESSFUL")]


def test_sql_injection_in_username_matches_nothing():
    database.save_user(make_user())
    # Same lookup login.py uses. If the query were built with string
    # formatting, this input would match every row.
    rows = query(
        "SELECT password FROM user_data WHERE username = ?",
        ("' OR '1'='1",),
    )
    assert rows == []