from app.database.database import init_db, get_all_users

import asyncio


async def main():
    await init_db()
    users = await get_all_users()
    for user in users:
        print(user.user_id, user.username, user.encrypted_password)


asyncio.run(main())
