import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 3306))
    db_name: str = os.getenv("DB_NAME", "sakila")
    db_user: str | None = os.getenv("DB_USER")
    db_password: str | None = os.getenv("DB_PASSWORD")
