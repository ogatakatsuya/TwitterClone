from fastapi import APIRouter, Cookie, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemes.profile import EditProfile, NewProfile

from api.repository.auth.user import get_current_user_id
from api.repository.posts.posts import get_posts_by_user_id
from api.repository.user.user import get_profile, edit_profile

router = APIRouter()

@router.get("/profile/post/{user_id}")
async def get_personal_post(
    user_id: int,
    db: AsyncSession = Depends(get_db), 
    offset: int = Query()
):
    posts = await get_posts_by_user_id(db, user_id)
    return posts


@router.get("/profile/{user_id}")
async def get_profile_information(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    profile = await get_profile(db, user_id)
    return profile

@router.put("/profile/{user_id}")
async def edit_profile_information(
    user_id: int, profile_body : EditProfile, db: AsyncSession = Depends(get_db)
):
    new_post = NewProfile(
        user_id = user_id,
        nickname = profile_body.nickname,
        biography = profile_body.biography,
        birth_day = profile_body.birth_day,
    )
    
    await edit_profile(db, new_post)
    await db.commit()
    return {"message": "Successfully edit profile"}