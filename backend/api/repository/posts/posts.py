from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import api.schemes.posts as post_schema
from api.models.models import Post

async def create_post(db: AsyncSession, post_body: post_schema.CreatePost):
    post = Post(text=post_body.text, user_id=post_body.user_id)
    db.add(post)
    await db.flush()
    return post

async def get_posts(db: AsyncSession):
    result = await db.execute(
        select(Post)
        .where(Post.parent_id == None)
        .limit(10)
    )
    top_level_posts = result.scalars().all()
    return top_level_posts

async def delete_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).filter_by(id=post_id))
    post = result.scalar_one_or_none()
    
    if post is None:
        return False
    
    await db.delete(post)
    return True