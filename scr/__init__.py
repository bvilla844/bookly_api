
#C:\bookly_api\scr\__init__.py
from fastapi import FastAPI
from scr.books.routes import book_router
from scr.auth.routes import auth_router
from scr.reviews.routes import review_router
from contextlib import asynccontextmanager
from scr.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting...")
    from scr.db.models import Book
    await init_db()
    yield
    print(f"server has been stopped...")

version = "v1"
app = FastAPI(
    title = "bookly api",
    description = "a REST API for a book review web service",
    version =version,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
