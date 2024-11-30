import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    DATABASE_URL: str = "sqlite+aiosqlite:///bot_users.db"
    NOTIFICATION_CHECK_INTERVAL: int = 900  # 15 minutes

    class Config:
        env_file = ".env"


settings = Settings()
