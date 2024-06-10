from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.schemes.posts import CreatePost
from api.models.models import Post

async def create_post(db: AsyncSession, post_body: CreatePost):
    post = Post(text=post_body.text, user_id=post_body.user_id)
    db.add(post)
    await db.flush()
    return post

async def get_posts(db: AsyncSession):
    result = await db.execute(
        select(Post)
        .where(Post.parent_id == None)
        .order_by(Post.id.desc())
        .limit(10)
        .offset(0)
    )
    top_level_posts = result.scalars().all()
    return top_level_posts

async def get_posts_by_parent_id(db: AsyncSession, parent_id: int):
    result = await db.execute(
        select(Post)
        .where(Post.parent_id == parent_id)
    )
    posts = result.scalars().all()
    return posts

async def get_posts_by_use_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Post)
        .where(Post.user_id == user_id)
        .where(Post.parent_id == None)
    )
    posts = result.scalars().all()
    return posts

async def delete_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).filter_by(id=post_id))
    post = result.scalar_one_or_none()
    
    if post is None:
        return False
    
    await db.delete(post)
    return True