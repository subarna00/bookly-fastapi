from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import CreateBookModel, UpdateBookModel, Book
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db import get_session
from src.books.service import BookService
import uuid
from src.auth.dependencies import AccessTokenBearer


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

@book_router.get("/", response_model=list[Book])
async def get_books(session: AsyncSession = Depends(get_session), user_details: str = Depends(access_token_bearer)):
    return await book_service.get_books(session)


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: CreateBookModel, session: AsyncSession = Depends(get_session), user_details: str = Depends(access_token_bearer)):
    return await book_service.create_book(book, session)  
      

@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: uuid.UUID, session: AsyncSession = Depends(get_session), user_details: str = Depends(access_token_bearer)):
    book = await book_service.get_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@book_router.patch("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: uuid.UUID, book_update: UpdateBookModel, session: AsyncSession = Depends(get_session), user_details: str = Depends(access_token_bearer)):
    book = await book_service.update_book(book_id, book_update, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: uuid.UUID, session: AsyncSession = Depends(get_session), user_details: str = Depends(access_token_bearer)):
    book = await book_service.delete_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return None