# from sqlalchemy import String, Integer
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from ..db.db import Base
# from ..models.file import Item


# class User(Base):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     email: Mapped[str] = mapped_column(String(100), nullable=False)
#     username: Mapped[str] = mapped_column(String(100))
#     password: Mapped[str] = mapped_column(String(100), nullable=False)
#     items: Mapped[list["Item"] | None] = relationship()

#     class Config:
#         orm_mode = True
