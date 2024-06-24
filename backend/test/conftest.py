import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db import ASYNC_DB_URL
import asyncio

# 非同期エンジンとセッションの作成
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

# データベースセッションのフィクスチャ
@pytest.fixture(scope='function') # dbセッションをテストで共有
async def db_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback() # テストが終わったらロールバック
            await session.close()

@pytest.fixture(scope='session') # 全てのテストで同一のsessionを共有
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
