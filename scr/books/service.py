
from sqlmodel.ext.asyncio.session import AsyncSession
from.schemas import BookCreate, BookUpdate
from sqlmodel import select, desc
from scr.db.models import Book
from datetime import datetime

class BookService:
    async def get_all_books(self, session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self,user_uid:str, session:AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid:str, session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(
            self,
            book_data: BookCreate,
            user_uid: str,
            session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book (self, book_id:str, book_data:BookUpdate, session:AsyncSession):
        book_update = await self.get_book(book_id,session)

        if book_update is not None:
            book_update_dic = book_data.model_dump()
            for k, v in book_update_dic.items():
                setattr(book_update, k, v)
            book_update.updated_at = datetime.utcnow()
            await session.commit()
            return book_update
        return None

    async def delete_book (self, book_id:str, session:AsyncSession):
        book_delete = await self.get_book(book_id, session)
        if book_delete is not None:
            await session.delete(book_delete)
            await session.commit()
        else:
            return None
