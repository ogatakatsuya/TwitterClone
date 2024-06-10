from pydantic import BaseModel

class Likes(BaseModel):
    likes: int
    
class LikeInfo(BaseModel):
    user_id: int
    post_id: int