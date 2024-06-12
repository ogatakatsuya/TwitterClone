from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from api.repository.like.like import create_like, delete_like, get_like_status
from api.repository.auth.user import get_current_user_id
from api.schemes.likes import LikeInfo
from api.db import get_db

router = APIRouter()

@router.get("/likes/{post_id}")
async def get_likes_num(
    post_id: int, db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    like_body = LikeInfo(user_id=user_id, post_id=post_id)
    likes_num, is_like = await get_like_status(db, like_body)
    return {
        "like_num": likes_num,
        "is_like": is_like,
        }

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