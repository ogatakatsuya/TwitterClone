from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemes.profile import EditProfile, NewProfile

from api.repository.auth.user import get_current_user_id
from api.repository.posts.posts import get_posts_by_user_id
from api.repository.user.user import get_profile, edit_profile

router = APIRouter()

@router.get("/profile")
async def get_own_profile_information(
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    profile = await get_profile(db, user_id)
    return profile

@router.put("/profile")
async def edit_own_profile_information(
    profile_body : EditProfile, 
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    new_post = NewProfile(
        user_id = user_id,
        nickname = profile_body.nickname,
        biography = profile_body.biography,
        birth_day = profile_body.birth_day,
    )
    
    await edit_profile(db, new_post)
    await db.commit()
    return {"message": "Successfully edit profile"}

@router.get("/profile/post") #ログインしているユーザーの投稿の取得
async def get_own_posts(
    offset: int,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    posts = await get_posts_by_user_id(db, user_id)
    return posts

@router.get("/profile/post/{user_id}") #ログインしているユーザー以外のユーザーの投稿の取得
async def get_personal_posts(
    user_id: int,
    offset: int,
    db: AsyncSession = Depends(get_db), 
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