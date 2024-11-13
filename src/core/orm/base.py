from sqlalchemy.orm import DeclarativeBase

from src.core.orm.database import sync_engine

class Base(DeclarativeBase):
    pass


def create_db_and_tables():
    Base.metadata.create_all(sync_engine)
