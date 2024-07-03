from pydantic import BaseModel, Field

class Post(BaseModel):
    text: str
    
class CreatePost(Post):
    user_id: int
    parent_id: int = Field(None)