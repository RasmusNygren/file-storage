from pydantic import BaseModel

from .item import Item


class User(BaseModel):
    email: str
    username: str | None = None
    items: list[Item] | None = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserInDb(User):
    password: str
    
