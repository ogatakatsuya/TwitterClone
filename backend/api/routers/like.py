from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db

router = APIRouter()

@router.get("/likes/{post_id}")
def get_likes_num(
    post_id: int, db: AsyncSession = Depends(get_db)
):
    pass

@router.post("/like/{post_id}")
def create_like(
    post_id: int, db: AsyncSession = Depends(get_db)
):
    pass

@router.delete("/like/{post_id}")
def delete_like(
    post_id: int, db: AsyncSession = Depends(get_db)
):
    pass