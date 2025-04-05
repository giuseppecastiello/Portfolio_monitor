from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password.get_secret_value()}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = AsyncSession(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass