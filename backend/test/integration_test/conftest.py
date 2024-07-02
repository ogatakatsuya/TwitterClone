import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions
from models.models import Base
from main import app
from db import get_db
from sqlalchemy.pool import NullPool
from httpx import AsyncClient

TEST_DB_URL = "mysql+aiomysql://root:rootpassword@db:3306/test_db?charset=utf8"

@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    async_engine = create_async_engine(TEST_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def get_db_for_testing():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_for_testing

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client

