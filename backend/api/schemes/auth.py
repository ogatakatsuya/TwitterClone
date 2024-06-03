from typing import Optional, Union
from pydantic import BaseModel, Field
    
class UserCreate(BaseModel):
    user_name: Optional[str] = Field(None, example="user_name")
    password: Optional[str] = Field(None, example="password")
    
class UserCreateResponse(UserCreate):
    id: int
    
# トークンのデータモデル
class Token(BaseModel):
    access_token: str
    token_type: str

# トークンに含まれるデータモデル
class TokenData(BaseModel):
    username: Union[str, None] = None
    
class AccessToken(BaseModel):
    access_token: str