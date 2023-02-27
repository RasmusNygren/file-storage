# from sqlalchemy import String, Integer, ForeignKey, Boolean
# from sqlalchemy.orm import Mapped, mapped_column
# from ..db.db import Base

# class File(Base):
#     id: Mapped[int] =  mapped_column(Integer, primary_key=True)
#     s3_object_name: Mapped[str] = mapped_column(String(100))

# class Item(Base):
#     id: Mapped[int] =  mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(100), nullable=False)
#     file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False)
#     read: Mapped[bool] = mapped_column(Boolean, default=False)
#     owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
