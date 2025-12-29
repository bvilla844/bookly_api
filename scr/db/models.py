from sqlmodel import SQLModel, Field,Relationship
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, timezone, date
from uuid import UUID
import uuid
from typing import List, Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )

    user_name: str = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=False, unique=True)
    )

    email: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True, index=True)
    )

    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False)
    )

    first_name: str = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=False)
    )

    last_name: str = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=False)
    )

    role: str = Field(
        sa_column=Column(pg.VARCHAR(10), nullable=False, server_default="user")
    )

    is_verified: bool = Field(
        default=False,
        sa_column=Column(pg.BOOLEAN, nullable=False, server_default="false")
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False)
    )

    books: List["Book"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    reviews: List["Review"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.user_name}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4())
    )
    title: str = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=False)
    )
    author: str = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=False)
    )
    publisher: str = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=False)
    )
    published_date: date = Field(
        sa_column=Column(pg.DATE, nullable=False)
    )
    page_count: int = Field(
        sa_column=Column(pg.INTEGER, nullable=False)
    )
    language: str = Field(
        sa_column=Column(pg.VARCHAR(20), nullable=False)
    )
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False)
    )
    user: Optional["User"] = Relationship(back_populates="books")

    reviews: List["Review"] = Relationship(
        back_populates="book",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book uid={self.uid} title={self.title}>"

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4())
    )
    rating: int = Field(
        lt=5
    )
    review_text: str = Field(
        sa_column=Column(pg.VARCHAR(500), nullable=False)
    )
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False)
    )
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by {self.user_uid}>"


