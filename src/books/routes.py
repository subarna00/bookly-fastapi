from fastapi import status, APIRouter
from fastapi.exceptions import HTTPException
from src.books.book_data import books
from src.books.schemas import Book, BookUpdate

book_router = APIRouter()

@book_router.get("/", response_model=list[Book])
async def get_books():
    return books

@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "published_date": book.published_date,
        "page_count": book.page_count,
        "language": book.language,
    }
    books.append(new_book)
    return new_book

@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@book_router.patch("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update.title
            book["author"] = book_update.author
            book["publisher"] = book_update.publisher
            book["page_count"] = book_update.page_count
            book["language"] = book_update.language
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return 
    raise HTTPException(status_code=404, detail="Book not found")