import pytest
from app.database.models import User, LibraryUser


def test_user_model():
    # Test User model creation and to_dict method
    user = User(
        user_id="test123",
        username="testuser",
        encrypted_password="encrypted_pass",
        language="en",
    )

    user_dict = user.to_dict()
    assert user_dict["username"] == "testuser"
    assert user_dict["password"] == "encrypted_pass"
    assert user_dict["language"] == "en"


def test_library_user_model():
    # Test LibraryUser model creation and to_dict method
    lib_user = LibraryUser(
        user_id="lib123",
        username="libuser",
        encrypted_password="lib_pass",
        phone_number="1234567890",
    )

    lib_user_dict = lib_user.to_dict()
    assert lib_user_dict["username"] == "libuser"
    assert lib_user_dict["password"] == "lib_pass"
    assert lib_user_dict["phone_number"] == "1234567890"
