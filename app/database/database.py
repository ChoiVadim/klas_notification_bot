import logging
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.database.models import Base, User, LibraryUser

# Create an async engine
engine = create_async_engine("sqlite+aiosqlite:///bot_users.db", echo=True)

# Create an async session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize the database, creating all tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database initialized successfully")


async def save_user(user_id: str, username: str, encrypted_password: str):
    """Save or update user in database"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                user = await session.get(User, user_id)
                if user:
                    user.username = username
                    user.encrypted_password = encrypted_password
                else:
                    user = User(
                        user_id=user_id,
                        username=username,
                        encrypted_password=encrypted_password,
                    )
                    session.add(user)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(f"Error saving user: {e}")
                return False


async def get_user(user_id: str):
    """Get user from database"""
    async with AsyncSessionLocal() as session:
        try:
            user = await session.get(User, user_id)
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error getting user: {e}")
            return None


async def get_all_users():
    """Get all users from database"""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logging.error(f"Error getting all users: {e}")
            return []


async def delete_user(user_id: str):
    """Delete user from database"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                user = await session.get(User, user_id)
                if user:
                    await session.delete(user)
                    await session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(f"Error deleting user: {e}")
                return False


async def save_library_user(
    user_id: str, username: str, encrypted_password: str, phone_number: str
):
    """Save or update library user in database"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                user = await session.get(LibraryUser, user_id)
                if user:
                    user.username = username
                    user.encrypted_password = encrypted_password
                    user.phone_number = phone_number
                else:
                    user = LibraryUser(
                        user_id=user_id,
                        username=username,
                        encrypted_password=encrypted_password,
                        phone_number=phone_number,
                    )
                    session.add(user)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(f"Error saving library user: {e}")
                return False


async def get_library_user(user_id: str):
    """Get library user from database"""
    async with AsyncSessionLocal() as session:
        try:
            user = await session.get(LibraryUser, user_id)
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error getting library user: {e}")
            return None


async def get_all_library_users():
    """Get all library users from database"""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(LibraryUser))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logging.error(f"Error getting all library users: {e}")
            return []


async def delete_library_user(user_id: str):
    """Delete library user from database"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                user = await session.get(LibraryUser, user_id)
                if user:
                    await session.delete(user)
                    await session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(f"Error deleting library user: {e}")
                return False
