from pydantic import BaseModel

class CreateFollow(BaseModel):
    follow_id: int
    
class FollowBody(BaseModel):
    user_id: int
    follow_id: int