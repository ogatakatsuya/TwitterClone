from typing import Optional
from pydantic import BaseModel, Field
    
class UserCreate(BaseModel):
    user_name: Optional[str] = Field(None, example="user_name")
    password: Optional[str] = Field(None, example="password")
    
class UserCreateResponse(UserCreate):
    id: int