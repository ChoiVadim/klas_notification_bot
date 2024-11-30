import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import asyncio
from app.database.database import init_db, save_user
from app.utils.encryption import encrypt_password


async def migrate_users():
    await init_db()
    try:
        with open("../users.json", "r") as f:
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
