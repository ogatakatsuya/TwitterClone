from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

import api.auth.user as auth_cruds
import api.posts.posts as post_cruds
from api.db import get_db

from typing import List
import api.schemes.posts as post_schema

router = APIRouter()

@router.post("/post")
async def create_post(
    post: post_schema.Posts, db: AsyncSession = Depends(get_db)
):
    return await post_cruds.create_post(db, post)

@router.get("/post")
async def get_post(
    db: AsyncSession = Depends(get_db)
):
    success = await post_cruds.get_post(db)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return success

@router.delete("/post/{post_id}")
async def delete_post(
    post_id: int, db: AsyncSession = Depends(get_db)
):
    success = await post_cruds.delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}