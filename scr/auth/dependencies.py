from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from .utils import decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from scr.db.redis import token_in_blocklist
from scr.db.main import get_session
from .service import  UserService
from scr.auth.schemas import UserModel, UserBooksModel
from typing import List
from scr.db.models import  User
from scr.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission
)

user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        creds: HTTPAuthorizationCredentials = await super().__call__(request)

        if not creds:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authorization header missing"
            )

        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()

        if await token_in_blocklist(token_data["jti"]):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data


    def token_valid(self,token: str) -> bool:

        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(selfself, token_data):
        raise NotImplementedError("please override this method child classes")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) ->None:
        if token_data and token_data.get("refresh"):
            raise AccessTokenRequired ()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) ->None:
        if token_data and not token_data.get("refresh"):
            raise RefreshTokenRequired()

async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
) -> UserBooksModel:

    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(
        user_email,
        session,
    )

    return UserBooksModel.model_validate(user)


class RoleChecker:
    def __init__(self, allowed_roles:List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user:User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()
