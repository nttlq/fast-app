import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

os.environ["ENV_STATE"] = "TEST"

from app.config import config  # noqa: E402
from app.database import Base, async_engine, async_session_factory  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Comment, Post  # noqa: E402

async_engine.echo = False


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture()
# def client() -> Generator:
#     yield TestClient(app)


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# @pytest.fixture(autouse=True)
# async def db() -> AsyncGenerator:
#     """Restart DB and clear the tables for every test"""
#     async with async_engine.connect() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         # await conn.commit()
#         await conn.run_sync(Base.metadata.create_all)
#         await conn.commit()
#     yield
#     async with async_engine.connect() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.commit()


@pytest.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator:
    """Restart DB and clear the tables for every test"""
    # assert repr(config) == "TEST"
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


# @pytest.fixture(scope="session", autouse=True)
# async def connection_test(test_db, event_loop):
#     pg_host = test_db.host
#     pg_port = test_db.port
#     pg_user = test_db.user
#     pg_db = test_db.dbname
#     pg_password = test_db.password

#     with DatabaseJanitor(
#         pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
#     ):
#         connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
#         async_session_factory.init(connection_str)
#         yield
#         await async_session_factory.close()


# @pytest.fixture(scope="function", autouse=True)
# async def create_tables(connection_test):
#     async with async_session_factory.connect() as connection:
#         await sessionmanager.drop_all(connection)
#         await sessionmanager.create_all(connection)


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac
