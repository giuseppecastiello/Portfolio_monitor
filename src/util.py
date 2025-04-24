from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
import pandas as pd
from io import StringIO

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
