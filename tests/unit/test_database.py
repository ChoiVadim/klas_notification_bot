import pytest
from sqlalchemy import select
from app.database.database import (
    save_user,
    get_user,
    get_user_language,
    set_user_language,
)
from app.database.models import User


@pytest.mark.asyncio
async def test_save_user(test_session):
    user_id = "test123"
    username = "testuser"
    password = "encrypted_pass"

    # Save user
    await save_user(user_id, username, password)

    # Verify user was saved
    stmt = select(User).where(User.user_id == user_id)
    result = await test_session.execute(stmt)
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.username == username
    assert user.encrypted_password == password


@pytest.mark.asyncio
async def test_set_user_language(test_session):
    user_id = "lang123"
    username = "languser"
    password = "testpass"

    # Create user first
    await save_user(user_id, username, password)

    # Set language
    await set_user_language(user_id, "ko")

    # Verify language was set
    language = await get_user_language(user_id)
    assert language.value == "ko"
