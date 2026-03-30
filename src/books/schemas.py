from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
