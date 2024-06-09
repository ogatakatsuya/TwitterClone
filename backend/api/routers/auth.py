from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

import api.repository.auth.user as auth_cruds
from api.db import get_db

from typing import List
import api.schemes.auth as auth_schema
from api.repository.auth.user import authenticate_user, create_access_token, get_current_user_id, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/auth/register")
async def register_new_account(
    auth_body : auth_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    success = await auth_cruds.create_user(db, auth_body)
    if not success:
        raise HTTPException(status_code=404, detail="Register user failed")
    return {"message" : "user created."}

@router.post("/auth/login")
async def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, path="/")
    return {"message": "Successfuly login"}

@router.delete("/auth/logout")
async def logout_user(
    response: Response
):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Successfully log out"}