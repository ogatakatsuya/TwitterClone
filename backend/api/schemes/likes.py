from pydantic import BaseModel

class LikeInfo(BaseModel):
    user_id: int
    post_id: int