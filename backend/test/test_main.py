import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

import repository.auth.user as auth_modules
import schemes.auth as auth_schemes
from db import ASYNC_DB_URL

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

@pytest.mark.asyncio
async def test_create_user():
    async with async_session() as db:
        user_name = "testuser"
        new_user = await auth_modules.create_user(db, user_name)
        assert new_user.name == "testuser"
        
@pytest.mark.asyncio
async def test_create_password():
    async with async_session() as db:
        password_body = auth_schemes.PasswordCreate(user_id=1, password="testpassword")
        new_password = await auth_modules.create_password(db, password_body)
        assert new_password.id == 1
        assert new_password.password == "testpassword"