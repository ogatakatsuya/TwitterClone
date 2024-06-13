from pydantic import BaseModel

class CreateFollow(BaseModel):
    follow_id: int