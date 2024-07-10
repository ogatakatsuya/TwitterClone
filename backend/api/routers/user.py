from fastapi import APIRouter, Cookie, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemes.profile import EditProfile, NewProfile

from api.repository.auth.user import get_current_user_id
from api.repository.posts.posts import get_posts_by_user_id
from api.repository.user.user import get_profile, edit_profile
from api.repository.user.user import save_user_icon_url, upload_to_s3

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

# @router.put("/profile/icon")
# async def edit_icon(
#     # db: AsyncSession = Depends(get_db),
#     # access_token: str | None = Cookie(default=None),
#     file: UploadFile,  # ファイルアップロードにはUploadFileを使用
# ):
#     # user_id = await get_current_user_id(db, access_token)
#     filename = file.filename
#     return {"message": filename}
#     file_url = await upload_to_s3(file, filename)
#     return {"message": "Successfully connect to s3"}
#     _ = await save_user_icon_url(db, user_id, file_url)
#     return {"message": "Successfully edit icon"}

@router.post("/profile/icon")
async def get_uploadfile(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
): # フロント側のFormDataのkeyに合わせる(upload_file)
    user_id = await get_current_user_id(db, access_token)
    filename = file.filename
    file_url = await upload_to_s3(file, filename)
    _ = await save_user_icon_url(db, user_id, file_url)
    await db.commit()
    return {"message": "Successfully edit icon"}