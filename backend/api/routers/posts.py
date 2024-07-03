from fastapi import Depends, APIRouter, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

import api.repository.posts.posts as post_cruds
from api.db import get_db
from api.repository.auth.user import get_current_user_id
import api.schemes.posts as post_schema

router = APIRouter()

@router.post("/post")
async def create_post(
    post: post_schema.Post, db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="アクセストークンが見つかりません．再度ログインしてください．")

    user_id = await get_current_user_id(db, access_token)

    post_body = post_schema.CreatePost(text=post.text, user_id=user_id)
    new_post = await post_cruds.create_post(db, post_body)
    await db.commit()
    await db.refresh(new_post)
    return {"new_post": new_post}

@router.get("/posts")
async def get_posts(
    offset: int,
    limit: int,
    db: AsyncSession = Depends(get_db)
):
    posts= await post_cruds.get_posts(db, offset, limit)
    return posts

@router.get("/post/{post_id}")
async def get_post(
    post_id : int,
    db: AsyncSession = Depends(get_db)
):
    post = await post_cruds.get_post(db, post_id)
    return post

@router.delete("/post/{post_id}")
async def delete_post(
    post_id: int, db: AsyncSession = Depends(get_db)
):
    success = await post_cruds.delete_post(db, post_id)
    if success:
        await db.commit()
        return {"detail": "Post deleted"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")