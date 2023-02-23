from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, declared_attr

import os

pg_password = os.environ["pg_password"]
engine = create_engine(f"postgresql://postgres:{pg_password}@db.yzotxmtbzhslbigptkkj.supabase.co:5432/postgres")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base():
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() # type: ignore
    created_at: Mapped["DateTime"] = mapped_column(DateTime, nullable=False, default=func.now())
    modified_at: Mapped["DateTime"] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

Base = declarative_base(cls=Base)
