from fastapi import Depends, APIRouter, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemes.follow import CreateFollow
from api.repository.follow.follow import follow, get_users_followed, get_users_following
from api.repository.auth.user import get_current_user_id

router = APIRouter()

@router.get("/follow")
async def get_following_users(
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    pass

@router.get("/followed")
async def get_users_following_me(
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    pass

@router.post("/follow")
async def follow_user(
    follow_id: CreateFollow, 
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    
    pass