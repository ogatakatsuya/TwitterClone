import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from jose import jwt

import repository.auth.user as auth_modules
from repository.auth.user import SECRET_KEY, ALGORITHM
import schemes.auth as auth_schemes
from db import ASYNC_DB_URL
import asyncio

# 非同期エンジンとセッションの作成
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

# データベースセッションのフィクスチャ
@pytest.fixture(scope='session') # dbセッションをテストで共有
async def db_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback() # テストごとにロールバック

@pytest.fixture(scope='session') # 全てのテストで同一のsessionを共有
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

def test_get_password_hash():
    password = "test_password"
    hashed_password = auth_modules.get_password_hash(password)
    assert hashed_password != password, "failed at get_password_hash"

def test_verify_password_success():
    password = "test_password"
    hashed_password = auth_modules.get_password_hash(password)
    assert auth_modules.verify_password(password, hashed_password) == True, "failed at verify_password"

def test_verify_password_failure():
    password = "test_password"
    wrong_password = "wrong_password"
    hashed_password = auth_modules.get_password_hash(password)
    assert auth_modules.verify_password(wrong_password, hashed_password) == False, "failed at verify_password"

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    user_name = "test_user"
    new_user = await auth_modules.create_user(db_session, user_name)
    assert new_user.name == user_name, "failed at create_user"
    
@pytest.mark.asyncio
async def test_get_user(db_session: AsyncSession):
    user_name = "test_user"
    fetched_user = await auth_modules.get_user(db_session, user_name)
    assert fetched_user.name == user_name, "failed at get_user"

@pytest.mark.asyncio
async def test_create_password(db_session: AsyncSession):
    user_name = "test_user"
    fetched_user = await auth_modules.get_user(db_session, user_name)
    password_body = auth_schemes.PasswordCreate(user_id=fetched_user.id, password="test_password")
    new_password = await auth_modules.create_password(db_session, password_body)
    assert new_password is not None, "failed at create_password"

@pytest.mark.asyncio
async def test_get_password(db_session: AsyncSession):
    user_name = "test_user"
    password = "test_password"
    fetched_user = await auth_modules.get_user(db_session, user_name)
    hashed_password = await auth_modules.get_password(db_session, fetched_user.id)
    assert auth_modules.verify_password(password, hashed_password) == True, "failed at get_password"

@pytest.mark.asyncio
async def test_authenticate_user_success(db_session: AsyncSession):
    user_name = "test_user"
    user_password = "test_password"
    is_authenticated = await auth_modules.authenticate_user(db_session, user_name, user_password)
    assert is_authenticated, "failed at authenticate_user_success"

@pytest.mark.asyncio
async def test_authenticate_user_failure(db_session: AsyncSession):
    user_name = "test_user"
    user_password = "wrong_password"
    is_authenticated = await auth_modules.authenticate_user(db_session, user_name, user_password)
    assert is_authenticated == False, "failed at authenticate_user_failure"

# async def test_create_access_token(db_session: AsyncSession):
#     user_name = "test_user"
#     test_user = await auth_modules.get_user(db_session, user_name)
#     token = await auth_modules.create_access_token(data={"sub": str(test_user.id)})
#     assert token, "The access token should not be empty."
    
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     assert payload.get("sub") == test_user.id, "The token payload should contain the correct user ID."