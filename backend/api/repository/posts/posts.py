from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import UploadFile, HTTPException
from botocore.exceptions import NoCredentialsError

import boto3
import os
from dotenv import load_dotenv


from api.schemes.posts import CreatePost
from api.models.models import Post, User

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
CLOUDFRONT_URL = os.getenv("CLOUD_FRONT_URL")
FILE_UPLOAD_FOLDER = os.getenv("FILE_UPLOAD_FOLDER")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-northeast-1'
)

async def create_post(db: AsyncSession, post_body: CreatePost):
    post = Post(
        text=post_body.text, 
        file_url=post_body.file_url,
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
            "file_url": post.file_url,
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
            "file_url": post.file_url,
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
            "file_url": post.file_url,
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
            "file_url": post.file_url,
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

async def upload_to_s3(file: UploadFile, filename: str):
    try:
        # S3にアップロード
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, f"{FILE_UPLOAD_FOLDER}/{filename}")
        file_url = f"{CLOUDFRONT_URL}/{FILE_UPLOAD_FOLDER}/{filename}"
        return file_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")