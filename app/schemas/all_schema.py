from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserAdd(UserBase):
    api_key: str
    active: bool=False

class PostBase(BaseModel):
    title: str
    body: str

class PostAdd(PostBase):
    created: datetime
    author_id: str
    active: bool = False
    thumbs_up: list
    thumbs_down: list