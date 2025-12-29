# C:\bookly_api\scr\db\main.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from scr.config import Config
from scr.db.models import Book

# Engine async
async_engine = create_async_engine(
    Config.DATABASE_URL,  # Debe ser postgresql+asyncpg://...
    echo=True
)

# Sessionmaker async
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Inicializar base de datos
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependencia para FastAPI
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
