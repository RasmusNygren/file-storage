from pydantic import BaseModel

from .item import Item


class User(BaseModel):
    email: str
    username: str | None = None
    items: list[Item] | None = None


class UserInDb(User):
    password: str


class UserCreate(User):
    email: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


