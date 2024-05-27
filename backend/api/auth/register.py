from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession

import api.models.auth as auth_model
import api.schemes.auth as auth_schema

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_user(db: AsyncSession, user_create: auth_schema.UserCreate) -> auth_model.User:
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.dict()
    user_data['password'] = hashed_password
    
    user = auth_model.User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user