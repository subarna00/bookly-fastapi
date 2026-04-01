from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg 
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            default=uuid.uuid4,
            primary_key=True
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    password_hash: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"