# @Author: LeonSong
# @Date:   2026-07-31 11:30
# @Description: Get database session

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings

engine = create_engine(url=settings.DATABASE_URL, echo=settings.DATABASE_LOG_ECHO)


SessionLocal = sessionmaker(
    bind=engine,  # target database engine
    autoflush=False,  # sync changes before querying
    expire_on_commit=False,  # keep object avaiable after committing
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
