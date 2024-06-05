from typing import Optional, Union
from pydantic import BaseModel, Field

class Posts(BaseModel):
    text: str
    
class CreatePosts(Posts):
    access_token: str