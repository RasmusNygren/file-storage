from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str | None = None

class User(UserBase, table=True):
    id: int | None = Field(primary_key=True)
    items: list["Item"] | None = Relationship(back_populates="owner")
    is_admin: bool | None = False
    password: str


class UserCreate(UserBase):
    email: str
    username: str | None
    password: str


class File(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    s3_object_name: str = Field(nullable=False)


class ItemBase(SQLModel):
    title: str
    read: bool | None = None
    file_id: int

    owner_id: int = Field(foreign_key="user.id")

class Item(ItemBase, table=True):
    id: int | None = Field(primary_key=True)

    owner: Optional["User"] = Relationship(back_populates="items")


class Token(SQLModel):
    access_token: str
    token_type: str

