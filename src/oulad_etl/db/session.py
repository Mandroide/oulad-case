from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import Settings

settings = Settings()
db_url = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_engine(settings.db_url, echo=False)
SessionLocal = sessionmaker(bind=engine)
