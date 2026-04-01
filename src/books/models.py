from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid

class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return super().__repr__()