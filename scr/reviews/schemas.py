
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class ReviewModel(BaseModel):

    uid: UUID
    rating: int = Field(ge=1, le=5)
    review_text: str
    user_uid: UUID
    book_uid: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewCreateModel(BaseModel):
    rating: int = Field(ge=1, le=5)
    review_text: str