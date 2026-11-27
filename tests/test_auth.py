# Tests written by Claude (Anthropic) and reviewed by Richard Taing.

from auth import hash_password, verify_password


def test_correct_password_verifies():
    password_hash = hash_password("correct horse")
    assert verify_password(password_hash, "correct horse")


def test_wrong_password_rejected():
    password_hash = hash_password("correct horse")
    assert not verify_password(password_hash, "wrong horse")


def test_same_password_gives_different_hashes():
    # Each hash gets a random salt, so identical passwords never share a hash.
    assert hash_password("same") != hash_password("same")


def test_hash_uses_argon2id():
    assert hash_password("anything").startswith("$argon2id$")


def test_hash_does_not_contain_password():
    assert "secret123" not in hash_password("secret123")