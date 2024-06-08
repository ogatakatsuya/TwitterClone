from datetime import datetime
from pydantic import BaseModel

class EditProfile(BaseModel):
    nickname: str
    biography: str
    birth_day: datetime
    
class NewProfile(EditProfile):
    user_id: int