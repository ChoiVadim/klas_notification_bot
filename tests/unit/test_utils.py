import pytest
from app.utils.encryption import encrypt_password, decrypt_password


@pytest.mark.asyncio
async def test_encryption():
    # Test data
    original_password = "test_password123"

    # Test encryption
    encrypted = encrypt_password(original_password)
    assert encrypted != original_password

    # Test decryption
    decrypted = decrypt_password(encrypted)
    assert decrypted == original_password

    # Test different passwords produce different encryptions
    another_encrypted = encrypt_password(original_password)
    assert encrypted != another_encrypted


@pytest.mark.asyncio
async def test_invalid_decryption():
    with pytest.raises(Exception):
        decrypt_password("invalid_encrypted_password")
