from fastapi import APIRouter
from fastapi.params import Depends

from scr.db.models import User
from .schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from scr.db.main import get_session
from .service import ReviewService
from scr.auth.dependencies import get_current_user


review_service = ReviewService()
review_router = APIRouter()

@review_router.post("/book/{book_uid}")
async def add_review_books(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await review_service.add_review_books(
        user_email=current_user.email,
        review_data=review_data,
        book_uid=book_uid,
        session=session
    )

