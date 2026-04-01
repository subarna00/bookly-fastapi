import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class Book(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CreateBookModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class UpdateBookModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str