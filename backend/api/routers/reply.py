from typing import Dict

from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemes.posts import Post, CreatePost
from api.repository.auth.user import get_current_user_id
from api.repository.posts.posts import create_post, get_posts_by_parent_id, delete_post
from api.db import get_db

router = APIRouter()

@router.get("/replies/{parent_id}")
async def get_replies(parent_id: int, db: AsyncSession = Depends(get_db)):
    replies = await get_posts_by_parent_id(db, parent_id)
    return replies

@router.post("/reply/{parent_id}")
async def post_reply(
    parent_id: int, reply_body: Post, db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    create_reply = CreatePost(text=reply_body.text, user_id=user_id, parent_id=parent_id)
    new_reply = await create_post(db, create_reply)
    await db.commit()
    await db.refresh(new_reply)
    return {"message": "Successfully created reply.","new_reply": new_reply}

@router.delete("/reply/{reply_id}", response_model=Dict[str, str])
async def delete_reply(reply_id: int, db: AsyncSession = Depends(get_db)):
    is_success = await delete_post(db, reply_id)
    if is_success:
        await db.commit()
        return {"message": "Successfully deleted reply."}
    else:
        return {"message": "Something went wrong, please retry."}
