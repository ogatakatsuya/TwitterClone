import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
ASYNC_DB_URL = "mysql+aiomysql://root:rootpassword@db:3306/data?charset=utf8"

# 非同期エンジンとセッションの作成
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

# データベースセッションのフィクスチャ
@pytest.fixture() # dbセッションをテストごとに生成・ロールバック・クローズ
async def db_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
