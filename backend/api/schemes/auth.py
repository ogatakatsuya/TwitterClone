from typing import Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
    
class UserCreate(BaseModel):
    user_name: Optional[str] = Field(None, example="user_name")
    password: Optional[str] = Field(None, example="password")
    
class UserCreateResponse(BaseModel):
    id: int
    name: str
    nickname: Optional[str] = None
    biography: Optional[str] = None
    birth_day: Optional[datetime] = None
    is_deleted: bool
    created_at: datetime
    
# トークンのデータモデル
class Token(BaseModel):
    access_token: str
    token_type: str

# トークンに含まれるデータモデル
class TokenData(BaseModel):
    username: Union[str, None] = None
    
class AccessToken(BaseModel):
    access_token: str