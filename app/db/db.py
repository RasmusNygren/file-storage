from sqlmodel import SQLModel, create_engine, Session, func, Field
from datetime import datetime

import os

pg_password = os.environ["pg_password"]

engine = create_engine(f"postgresql://postgres:{pg_password}@db.yzotxmtbzhslbigptkkj.supabase.co:5432/postgres", echo=True)
def get_session():
    with Session(engine) as session:
        yield session


class Base(SQLModel):
    created_at: datetime = Field(default=func.now())
    modified_at: datetime = Field(default=func.now(), sa_column_kwargs={"on_update": func.now()})
