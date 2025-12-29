# C:\bookly_api\scr\auth\service.py
from scr.db.models import User
from .schemas import UserCreate
from .utils import generate_passwd_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) :
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exists(self, email: str, session: AsyncSession) :
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        user_dict = user_data.model_dump(exclude={"password"})

        new_user = User(**user_dict)
        new_user.password_hash = generate_passwd_hash(user_data.password)
        new_user.role = "user"

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user


