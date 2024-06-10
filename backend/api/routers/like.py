from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from api.repository.like.like import count_likes, create_like, delete_like
from api.repository.auth.user import get_current_user_id
from api.schemes.likes import LikeInfo
from api.db import get_db

router = APIRouter()

@router.get("/likes/{post_id}")
async def get_likes_num(
    post_id: int, db: AsyncSession = Depends(get_db)
):
    likes_num = await count_likes(db, post_id)
    return {"like_num":likes_num}

@router.post("/like/{post_id}")
async def post_like(
    post_id: int, db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    like_body = LikeInfo(user_id=user_id, post_id=post_id)
    await create_like(db, like_body)
    await db.commit()
    return {"message": "successfully like created."}

@router.delete("/like/{post_id}")
async def remove_like(
    post_id: int, db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    like_body = LikeInfo(user_id=user_id, post_id=post_id)
    await delete_like(db, like_body)
    await db.commit()
    return {"message": "successfully deleted like."}