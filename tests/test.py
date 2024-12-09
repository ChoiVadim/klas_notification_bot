import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from app.database.database import init_db, get_all_users
from sqlalchemy import text
from app.database.database import init_db, engine


async def main():
    await init_db()
    users = await get_all_users()
    for user in users:
        print(user.user_id, user.username, user.encrypted_password)

    async with engine.begin() as conn:
        # Check if column exists first
        result = await conn.execute(text("PRAGMA table_info(users)"))
        columns = result.fetchall()
        column_names = [column[1] for column in columns]

        if "language" not in column_names:
            await conn.execute(
                text("ALTER TABLE users ADD COLUMN language VARCHAR DEFAULT 'en'")
            )
            await conn.commit()
            print("Migration completed successfully!")
        else:
            print("Column 'language' already exists!")


asyncio.run(main())
