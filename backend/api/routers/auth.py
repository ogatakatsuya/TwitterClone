from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.auth.register as auth_cruds
from api.db import get_db

from typing import List
import api.schemes.auth as auth_schema

router = APIRouter()

@router.post("/auth/register", response_model=auth_schema.UserCreateResponse)
async def register(
    auth_body : auth_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await auth_cruds.create_user(db, auth_body)