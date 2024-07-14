from pydantic import BaseModel, Field
from typing import Optional

class Post(BaseModel):
    text: str
    file: Optional[bytes] = None
    
    
class CreatePost(Post):
    user_id: int
    parent_id: int = Field(None)
    file_url: Optional[str] = None