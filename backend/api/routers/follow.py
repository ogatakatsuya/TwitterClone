from fastapi import Depends, APIRouter, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from psycopg2 import errors as psycopg2_errors

from api.db import get_db
from api.schemes.follow import CreateFollow, FollowBody
from api.repository.follow.follow import follow, count_followed_users, count_following_users, delete_follow
from api.repository.auth.user import get_current_user_id

router = APIRouter()

@router.get("/follow")
async def get_my_following_users(
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    following_num = await count_following_users(db, user_id)
    
    return following_num

@router.get("/followed")
async def get_users_following_me(
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    followed_num = await count_followed_users(db, user_id)
    
    return followed_num

@router.post("/follow/{follow_id}")
async def follow_user(
    follow_id: int, 
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    try:
        follow_body = FollowBody(
            user_id=user_id,
            follow_id=follow_id
        )
        await follow(db, follow_body)
        await db.commit()
        return {"message": "successfully followed"}
    
    except psycopg2_errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail="can't follow the same user.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.delete("/follow/{follow_id}")
async def remove_follow(
    follow_id: int, 
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    try:
        follow_body = FollowBody(
            user_id=user_id,
            follow_id=follow_id
        )
        await delete_follow(db, follow_body)
        await db.commit()
        return {"message": "successfully delete"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/follow/{user_id}")
async def get_users_following(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    following_num = await count_following_users(db, user_id)
    return following_num

@router.get("/followed/{user_id}")
async def get_users_followed(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    followed_num = await count_followed_users(db, user_id)
    return followed_num