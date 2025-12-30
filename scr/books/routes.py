from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from scr.books.service import BookService
from scr.db.main import get_session
from fastapi.exceptions import HTTPException
from .schemas import Book, BookUpdate, BookCreate, BookDetail
from scr.db.models import Book
from typing import List
from scr.db.main import get_session
from uuid import UUID
from scr.auth.dependencies import AccessTokenBearer, RoleChecker
from scr.errors import (
    BookNotFound,

)

book_router = APIRouter()
book_service = BookService()
role_checker =  Depends(RoleChecker(["admin", "user"]))
acces_token_bearer = AccessTokenBearer()

@book_router.get("/",response_model=List[Book], dependencies= [role_checker], status_code= status.HTTP_200_OK)
async def get_books(session:AsyncSession = Depends(get_session), token_details:dict =Depends(acces_token_bearer),) -> list:
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/user/{user_uid}",response_model=List[Book], dependencies= [role_checker], status_code= status.HTTP_200_OK)
async def get_use_books_submission(user_uid: str, session:AsyncSession = Depends(get_session), token_details:dict =Depends(acces_token_bearer),) -> list:
    books = await book_service.get_user_books(user_uid, session)
    return books

@book_router.get("/{book_uid}", response_model = BookDetail, dependencies= [role_checker], status_code = status.HTTP_200_OK)
async def get_book_by_id(book_uid : UUID, session:AsyncSession = Depends(get_session), token_details:dict =Depends(acces_token_bearer)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise BookNotFound()

@book_router.post("/", response_model = Book, dependencies= [role_checker], status_code = status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate, session:AsyncSession = Depends(get_session), token_details:dict =Depends(acces_token_bearer)) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book

@book_router.patch("/", response_model = Book, dependencies= [role_checker], status_code = status.HTTP_200_OK)
async def update_book(book_uid: UUID, book_data: BookUpdate,  session:AsyncSession = Depends(get_session), token_details:dict =Depends(acces_token_bearer) )-> dict:
    updated_book = await book_service.update_book(book_uid, book_data, session)

    if updated_book is None:
        raise BookNotFound()
    else:
        return updated_book



@book_router.delete("/", dependencies= [role_checker], status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: UUID, session:AsyncSession = Depends(get_session), token_details:dict =Depends(acces_token_bearer)):
    delete_book = await book_service.delete_book(book_uid, session)

    if delete_book is None:
        raise BookNotFound()
    else:
        return delete_book








