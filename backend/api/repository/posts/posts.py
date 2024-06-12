from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.schemes.posts import CreatePost
from api.models.models import Post, User

async def create_post(db: AsyncSession, post_body: CreatePost):
    post = Post(
        text=post_body.text, 
        user_id=post_body.user_id, 
        parent_id=post_body.parent_id
    )
    db.add(post)
    await db.flush()
    return post

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(Post, User.name)
        .join(User, Post.user_id == User.id)
        .where(Post.id == post_id)
    )
    post, user_name = result.first()
    
    if post:
        return{
            "id": post.id,
            "text": post.text,
            "parent_id": post.parent_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user_id": post.user_id,
            "user_name": user_name
        }
    return None

async def get_posts(db: AsyncSession, offset: int):
    result = await db.execute(
        select(Post, User.name)
        .join(User, Post.user_id == User.id)
        .where(Post.parent_id == None)
        .order_by(Post.id.desc())
        .limit(10)
        .offset(offset)
    )
    
    posts_with_users = result.fetchall()
    top_level_posts = []
    
    for post, user_name in posts_with_users:
        top_level_posts.append({
            "id": post.id,
            "text": post.text,
            "parent_id": post.parent_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user_id": post.user_id,
            "user_name": user_name
        })
    
    return top_level_posts

async def get_posts_by_parent_id(db: AsyncSession, parent_id: int):
    result = await db.execute(
        select(Post, User.name)
        .join(User, Post.user_id == User.id)
        .where(Post.parent_id == parent_id)
    )
    posts_with_users = result.fetchall()
    top_level_posts = []
    
    for post, user_name in posts_with_users:
        top_level_posts.append({
            "id": post.id,
            "text": post.text,
            "parent_id": post.parent_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user_id": post.user_id,
            "user_name": user_name
        })
    
    return top_level_posts

async def get_posts_by_user_id(db: AsyncSession, user_id: int):
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