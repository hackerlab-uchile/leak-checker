from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import (
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_SERVER,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)

DATABASE_URL: str = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
TEST_DATABASE_URL: str = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_TEST_DB}"

test_engine = create_engine(TEST_DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(test_engine)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass
