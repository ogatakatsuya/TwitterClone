from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.schemes.reply import CreateReply
from api.models.models import Post

async def create_reply(db: AsyncSession, post_body: CreateReply):
    new_reply = Post(text=post_body.text, user_id=post_body.user_id, parent_id=post_body.parent_id)
    db.add(new_reply)
    return new_reply

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