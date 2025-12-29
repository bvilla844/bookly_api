# C:\bookly_api\scr\auth\schemas.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List
from scr.books.schemas import Book
from scr.reviews.schemas import  ReviewModel



class UserModel(BaseModel):
    uid: UUID
    user_name: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserBooksModel(UserModel):
    books: List[Book] = []
    reviews: List[ReviewModel] = []

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    user_name: str = Field(max_length=25)
    email: str = Field(max_length=40)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    password: str = Field(min_length=8)

class UserLoginModel(BaseModel):
    email: str
    password: str