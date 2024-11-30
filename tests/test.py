import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from app.database.database import init_db, get_all_users


async def main():
    await init_db()
    users = await get_all_users()
    for user in users:
        print(user.user_id, user.username, user.encrypted_password)


asyncio.run(main())
