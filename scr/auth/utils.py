from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from scr.config import Config
import jwt
import uuid
import logging
from typing import Optional


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRY = 3600  # segundos


def generate_passwd_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hash_passwd: str) -> bool:
    return password_context.verify(password, hash_passwd)


def create_access_token(
    user_data: dict,
    expiry: timedelta | None = None,
    refresh: bool = False
) -> str:

    payload = {
        "user": user_data,
        "exp": datetime.now(timezone.utc)
        + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }

    token = jwt.encode(
        payload,
        Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(
            token,
            Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]  # ✅ LISTA
        )

    except jwt.ExpiredSignatureError:
        logging.warning("Token expired")
        return None

    except jwt.InvalidTokenError as e:
        logging.warning(f"Invalid token: {e}")
        return None
