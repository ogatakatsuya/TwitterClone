from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException

import api.schemes.posts as post_schema
from api.models.models import Post

async def create_post(db: AsyncSession, post_create: post_schema.Posts) -> post_schema.Posts:
    post_data = post_create.dict()
    
    post = Post(**post_data)
    db.add(post)
    await db.commit()
    return post

async def get_post(db: AsyncSession):
    result = await db.execute(select(Post))
    all_posts = result.scalars().all()
    return all_posts

async def delete_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).filter_by(id=post_id))
    post = result.scalar_one_or_none()
    
    if post is None:
        return False
    
    await db.delete(post)
    await db.commit()
    return True