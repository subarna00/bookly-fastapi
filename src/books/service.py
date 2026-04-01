import uuid

from sqlalchemy import desc, select
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import CreateBookModel, UpdateBookModel
from .models import Book

class BookService:

    async def get_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return list(result.scalars().all())

    async def get_book(self, book_id: uuid.UUID, session: AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        return result.scalars().first()
    
    async def create_book(self, book_data: CreateBookModel, session: AsyncSession):
        book_dict = book_data.model_dump()
        published_raw = book_dict.pop("published_date")
        new_book = Book(**book_dict)
        new_book.published_date = datetime.strptime(published_raw, "%Y-%m-%d").date()
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_id: uuid.UUID, book_data: UpdateBookModel, session: AsyncSession):
        existing_book = await self.get_book(book_id, session)
        if existing_book is not None:
            book_dict = book_data.model_dump()
            published_raw = book_dict.pop("published_date", None)
            for field, value in book_dict.items():
                setattr(existing_book, field, value)
            if published_raw is not None:
                existing_book.published_date = datetime.strptime(
                    published_raw, "%Y-%m-%d"
                ).date()
            session.add(existing_book)
            await session.commit()
            await session.refresh(existing_book)
            return existing_book
        return None

    async def delete_book(self, book_id: uuid.UUID, session: AsyncSession):
        existing_book = await self.get_book(book_id, session)
        if existing_book is None:
            return None
        await session.delete(existing_book)
        await session.commit()
        return existing_book