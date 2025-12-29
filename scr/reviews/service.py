from scr.db.models import Review
from scr.auth.service import UserService
from scr.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from fastapi import HTTPException, status
import logging

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review_books(self, user_email: str, review_data: ReviewCreateModel,
                              book_uid: str, session:AsyncSession ):
        try:
            book = await book_service.get_book(session=session, book_uid= book_uid)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            user = await user_service.get_user_by_email(
                email=user_email,
                session=session
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            new_review = Review(**review_data.model_dump())
            new_review.user = user
            new_review.book = book

            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)

            return new_review
        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Oops, something went wrong")