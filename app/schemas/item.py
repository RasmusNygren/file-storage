from pydantic import BaseModel


class Item(BaseModel):
    title: str
    read: bool | None = None
    file_id: int
