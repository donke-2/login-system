# Tests written by Claude (Anthropic) and reviewed by Richard Taing.

import builtins
import importlib
import time

import pytest

# import_module returns the login.py module itself, even if actions/__init__.py
# re-exports a function that is also called "login".
login_module = importlib.import_module("actions.login")


@pytest.fixture(autouse=True)
def reset_lockout_state():
    login_module.failed_attemps = 0
    login_module.locked_until = 0
    yield
    login_module.failed_attemps = 0
    login_module.locked_until = 0


def test_record_failure_increments_counter():
    login_module.record_failure()
    login_module.record_failure()
    assert login_module.failed_attemps == 2


def test_start_lockout_sets_ten_minute_cooldown():
    login_module.start_lockout()
    time_left = login_module.locked_until - int(time.time())
    assert 595 <= time_left <= 600


def test_start_lockout_resets_counter():
    for _ in range(login_module.MAX_ATTEMPS):
        login_module.record_failure()
    login_module.start_lockout()
    assert login_module.failed_attemps == 0


def test_login_blocked_during_lockout(monkeypatch, capsys):
    login_module.start_lockout()

    def fail_if_called(prompt=""):
        raise AssertionError("login asked for input during lockout")

    monkeypatch.setattr(builtins, "input", fail_if_called)
    login_module.login()
    assert "Try again in" in capsys.readouterr().out