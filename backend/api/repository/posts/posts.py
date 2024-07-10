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
        select(Post, User.name, User.nickname, User.icon_url)
        .join(User, Post.user_id == User.id)
        .where(Post.id == post_id)
    )
    post, user_name, user_nickname, icon_url = result.first()
    
    if post:
        return{
            "id": post.id,
            "text": post.text,
            "parent_id": post.parent_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user_id": post.user_id,
            "user_name": user_name,
            "user_nickname": user_nickname,
            "icon_url": icon_url
        }
    return None

async def get_posts(db: AsyncSession, offset: int, limit: int):
    result = await db.execute(
        select(Post, User.name, User.nickname, User.icon_url)
        .join(User, Post.user_id == User.id)
        .where(Post.parent_id.is_(None))
        .order_by(Post.id.desc())
        .limit(limit)
        .offset(offset)
    )
    
    posts_with_users = result.fetchall()
    top_level_posts = []
    
    for post, user_name, user_nickname, icon_url in posts_with_users:
        top_level_posts.append({
            "id": post.id,
            "text": post.text,
            "parent_id": post.parent_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user_id": post.user_id,
            "user_name": user_name,
            "user_nickname": user_nickname,
            "icon_url": icon_url,
        })
    
    return top_level_posts

async def get_posts_by_parent_id(db: AsyncSession, parent_id: int):
    result = await db.execute(
        select(Post, User.name, User.nickname, User.icon_url)
        .join(User, Post.user_id == User.id)
        .where(Post.parent_id == parent_id)
    )
    posts_with_users = result.fetchall()
    top_level_posts = []
    
    for post, user_name, user_nickname, icon_url in posts_with_users:
        top_level_posts.append({
            "id": post.id,
            "text": post.text,
            "parent_id": post.parent_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user_id": post.user_id,
            "user_name": user_name,
            "user_nickname": user_nickname,
            "icon_url": icon_url,
        })
    
    return top_level_posts

async def get_posts_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Post, User.name, User.nickname, User.icon_url)
        .join(User, Post.user_id == User.id)
        .where(Post.user_id == user_id)
        .where(Post.parent_id.is_(None))
    )
    posts_with_users = result.fetchall()
    top_level_posts = []
    
    for post, user_name, user_nickname, icon_url in posts_with_users:
        top_level_posts.append({
            "id": post.id,
            "text": post.text,
            "parent_id": post.parent_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user_id": post.user_id,
            "user_name": user_name,
            "user_nickname": user_nickname,
            "icon_url": icon_url,
        })
    
    return top_level_posts

async def delete_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).filter_by(id=post_id))
    post = result.scalar_one_or_none()
    
    if post is None:
        return False
    
    await db.delete(post)
    return True