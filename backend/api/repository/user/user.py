from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import UploadFile, HTTPException
from botocore.exceptions import NoCredentialsError

import boto3
import os
from dotenv import load_dotenv

from api.models.models import User
from api.schemes.profile import NewProfile

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
CLOUDFRONT_URL = os.getenv("CLOUD_FRONT_URL")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-northeast-1'
)

async def get_profile(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    profile = result.scalars().first()
    return profile

async def edit_profile(db: AsyncSession, profile_body: NewProfile):
    result = await db.execute(select(User).where(User.id == profile_body.user_id))
    prev_profile = result.scalars().first()
    
    prev_profile.nickname = profile_body.nickname
    prev_profile.biography = profile_body.biography
    prev_profile.birth_day = profile_body.birth_day
    
    db.add(prev_profile)
    
    return True

async def upload_to_s3(file: UploadFile, filename: str):
    try:
        # S3にアップロード
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, f"{UPLOAD_FOLDER}/{filename}")
        file_url = f"{CLOUDFRONT_URL}/{UPLOAD_FOLDER}/{filename}"
        return file_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    
async def save_user_icon_url(db: AsyncSession, user_id: int, file_url: str):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.icon_url = file_url
    db.add(user)
    return True