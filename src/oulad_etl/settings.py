from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    db_url: str = Field(..., env="DB_URL")  # mysql+pymysql://user:pass@host/db

settings = Settings()