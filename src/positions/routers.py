from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.database import get_async_session, get_or_404, get_responses
from src.positions.models import Position
from src.positions.schemas import PositionSchema, PositionUpdateSchema

router = APIRouter(
    prefix="/positions",
    tags=["positions"]
)

responses = get_responses(Position)

@router.get("/", response_model=list[PositionSchema])
async def get_positions(session: AsyncSession = Depends(get_async_session)):
    """
    Get all positions.
    """
    result = await session.scalars(select(Position))
    positions = result.fetchall()
    return positions

@router.post("/add", response_model=PositionSchema, status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def add_position(position: PositionSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Add a new position.
    """
    new_position = Position(**position.model_dump())
    result = await session.execute(select(Position).where(Position.portfolio_id == new_position.portfolio_id, Position.company_ticker == new_position.company_ticker))
    existing_position = result.scalar_one_or_none()
    if existing_position:
        raise HTTPException(status_code=400, detail="Position with this id already exists")
    session.add(new_position)
    await session.commit()
    await session.refresh(new_position)
    return new_position

@router.get("/{portfolio_id}/{company_ticker}", response_model=PositionSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def get_position(portfolio_id: int, company_ticker: str, session: AsyncSession = Depends(get_async_session)):
    """
    Get a position by portfolio ID and company ticker.
    """
    return await get_or_404(Position, session, (portfolio_id, company_ticker))

@router.put("/{portfolio_id}/{company_ticker}", response_model=PositionSchema, responses={k: responses[k] for k in [200, 400, 404, 422]})
async def update_position(portfolio_id: int, company_ticker: str, position: PositionUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Update a position by portfolio ID and company ticker.
    """
    result = await get_or_404(Position, session, (portfolio_id, company_ticker))    
    for key, value in position.model_dump().items():
        if value is not None:
            setattr(result, key, value)
    try: 
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Position could not be updated")
    await session.refresh(result)
    return result

@router.delete("/{portfolio_id}/{company_ticker}", response_model=PositionSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def delete_position(portfolio_id: int, company_ticker: str, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a position by portfolio ID and company ticker.
    """
    result = await get_or_404(Position, session, (portfolio_id, company_ticker))
    await session.delete(result)
    await session.commit()
    return result
