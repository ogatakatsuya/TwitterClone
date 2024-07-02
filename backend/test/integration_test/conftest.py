import pytest
import asyncio
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions

from models.models import Base
from main import app
from db import get_db

TEST_DB_URL = "mysql+aiomysql://root:rootpassword@test_db:3305/test_data?charset=utf8"

@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def test_db(event_loop):
    async_engine = create_async_engine(TEST_DB_URL, echo=True)
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    async_session = TestSessionLocal()

    async def get_db_for_testing():
        try:
            yield async_session
            await async_session.commit()
        except SQLAlchemyError as e:
            assert e is not None
            await async_session.rollback()

    app.dependency_overrides[get_db] = get_db_for_testing

    yield async_session

    await async_session.rollback()
    await async_session.close()
    await async_engine.dispose()
    close_all_sessions()
