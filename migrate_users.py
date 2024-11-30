import json
import asyncio
from database import init_db, save_user
from encryptor import encrypt_password


async def migrate_users():
    await init_db()
    try:
        with open("users.json", "r") as f:
            users = json.load(f)

        for user_id, credentials in users.items():
            await save_user(
                user_id=user_id,
                username=credentials["username"],
                encrypted_password=encrypt_password(credentials["password"]),
            )
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")


if __name__ == "__main__":
    asyncio.run(migrate_users())
