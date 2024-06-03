from typing import Optional, Union
from pydantic import BaseModel, Field

class Posts(BaseModel):
    text: str
    user_id: int