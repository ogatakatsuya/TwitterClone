from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from api.models.models import Follow
from api.schemes.follow import FollowBody

async def follow(db: AsyncSession, follow_body: FollowBody):
    try:
        follow_create = Follow(
            follow_id = follow_body.user_id,
            followed_id = follow_body.follow_id
        )
        db.add(follow_create)
        await db.flush()
    
    except IntegrityError as sqlalchemy_error:
        db.rollback()
        raise sqlalchemy_error.orig
    
async def delete_follow(db: AsyncSession, follow_body: FollowBody):
    result = await db.execute(
        select(Follow)
        .where(Follow.follow_id == follow_body.user_id)
        .where(Follow.followed_id == follow_body.follow_id)
    )
    follow = result.scalar_one_or_none()
    await db.delete(follow)
    return follow

async def count_following_users(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(func.count(Follow.id))
        .where(Follow.follow_id == user_id)
    )
    following_num = result.scalar()
    
    return following_num

async def count_followed_users(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(func.count(Follow.id))
        .where(Follow.followed_id == user_id)
    )
    followed_num = result.scalar()
    
    return followed_num