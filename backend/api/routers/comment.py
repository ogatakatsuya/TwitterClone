from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemes.comment import Reply, CreateReply
from api.controller.auth.user import get_current_user_id
from api.controller.reply.reply import create_reply, get_reply_by_parent_id, remove_reply
from api.db import get_db

router = APIRouter()

@router.get("/comment/{parent_id}")
async def get_replies(parent_id: int, db: AsyncSession = Depends(get_db)):
    replies = await get_reply_by_parent_id(db, parent_id)
    return replies

@router.post("/comment/{parent_id}")
async def post_reply(
    parent_id: int, reply_body: Reply, db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    new_reply = CreateReply(text=reply_body.text, user_id=user_id, parent_id=parent_id)
    is_success = await create_reply(db, new_reply)
    
    if is_success :
        await db.commit()
        return {"message": "Successfully created reply."}
    else:
        return {"message": "Something went wrong, please retry."}

@router.delete("/comment/{reply_id}")
async def delete_reply(reply_id: int, db: AsyncSession =Depends(get_db)):
    is_success = await remove_reply(db, reply_id)
    if is_success :
        await db.commit()
        return {"message": "Successfully deleted reply."}
    else:
        return {"message": "Something went wrong, please retry."}