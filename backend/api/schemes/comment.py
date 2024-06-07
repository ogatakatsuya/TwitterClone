from pydantic import BaseModel

class Reply(BaseModel):
    text: str
    
class CreateReply(Reply):
    user_id: int
    parent_id: int