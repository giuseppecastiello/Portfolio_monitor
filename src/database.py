from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password.get_secret_value()}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        
async def get_or_404(model, session: AsyncSession, pk):
    """
    Helper function to get an object by primary key or raise a 404 error.
    """
    result = await session.get(model, pk)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return result

def get_responses(model: Base) -> dict:
    """
    Helper function to get the responses for a model.
    """
    return {
        200: {
            "description": f"{model.__name__} found"
        },
        201: {
            "description": f"{model.__name__} created"
        },
        400: {
            "description": f"Bad request"
        },
        404: {
            "description": f"{model.__name__} not found"
        },
        422: {
            "description": "Validation error"
        }
    }
    