from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Server is starting up...")
    await init_db()
    yield
    print(f"Server is shutting down...")




version = "v1"
app = FastAPI(
    version=version,
    title="Bookly API",
    description="A simple API for managing books",
    contact={
        "name": "Narendra Uprety",
        "email": "narendra@example.com"
    },
    lifespan=lifespan
)
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentication"])