from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from api.models.models import Like
from api.schemes.likes import LikeInfo

async def count_likes(
    db: AsyncSession, post_id: int
):
    result = await db.execute(
        select(func.count(Like.id))
        .where(Like.post_id == post_id)
    )
    like_num = result.scalar()
    return like_num

async def create_like(
    db: AsyncSession, like_body: LikeInfo
):
    result = await db.execute(
        select(Like)
        .where(Like.user_id == like_body.user_id)
        .where(Like.post_id == like_body.post_id)
    )
    existing_like = result.scalar_one_or_none()

    if existing_like:
        raise HTTPException(status_code=400, detail="User has already liked this post")

    new_like = Like(user_id=like_body.user_id, post_id=like_body.post_id)
    db.add(new_like)
    await db.flush()
    return new_like

async def delete_like(
    db: AsyncSession, like_body: LikeInfo
):
    result = await db.execute(
        select(Like)
        .where(Like.post_id == like_body.post_id)
        .where(Like.user_id == like_body.user_id)
    )
    like = result.scalar_one_or_none()
    
    await db.delete(like)
    return like