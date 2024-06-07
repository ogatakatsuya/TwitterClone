from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.schemes.comment import CreateReply
from api.models.models import Post

async def create_reply(db: AsyncSession, post_body: CreateReply):
    new_reply = Post(text=post_body.text, user_id=post_body.user_id, parent_id=post_body.parent_id)
    db.add(new_reply)
    return new_reply

async def get_reply_by_parent_id(db: AsyncSession, parent_id: int):
    result = await db.execute(select(Post).where(Post.parent_id == parent_id))
    posts = result.scalars().all()
    return posts

async def remove_reply(db: AsyncSession, reply_id: int):
    result = await db.execute(select(Post).filter_by(id=reply_id))
    reply = result.scalar_one_or_none()
    
    if reply is None:
        return False
    
    await db.delete(reply)
    return True