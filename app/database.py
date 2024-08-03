from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: F401
from sqlalchemy.orm import DeclarativeBase  # noqa: F401

from app.config import config

print("config.DATABASE_URL:", config.DATABASE_URL)

async_engine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
