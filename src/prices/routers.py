from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.database import get_async_session, get_or_404, get_responses
from src.prices.models import Price
from src.prices.schemas import PriceSchema, PriceUpdateSchema

router = APIRouter(
    prefix="/prices",
    tags=["prices"]
)

responses = get_responses(Price)

@router.get("/", response_model=list[PriceSchema])
async def get_prices(session: AsyncSession = Depends(get_async_session)):
    """
    Get all prices.
    """
    result = await session.scalars(select(Price))
    prices = result.fetchall()
    return prices

@router.post("/add", response_model=PriceSchema, status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def add_price(price: PriceSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Add a new price.
    """
    new_price = Price(**price.model_dump())
    result = await session.execute(select(Price).where(Price.company_ticker == new_price.company_ticker, Price.date == new_price.date))
    existing_price = result.scalar_one_or_none()
    if existing_price:
        raise HTTPException(status_code=400, detail="Price with this company ticker and date already exists")
    session.add(new_price)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Price could not be added")
    await session.refresh(new_price)
    return new_price

@router.get("/{company_ticker}/{date}", response_model=PriceSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def get_price(company_ticker: str, date: datetime, session: AsyncSession = Depends(get_async_session)):
    """
    Get a price by company ticker and date.
    """
    return await get_or_404(Price, session, (company_ticker, date))

@router.put("/{company_ticker}/{date}", response_model=PriceUpdateSchema, responses={k: responses[k] for k in [200, 400, 404, 422]})
async def update_price(company_ticker: str, date: datetime, price: PriceSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Update a price by company ticker and date.
    """
    result = await get_or_404(Price, session, (company_ticker, date))    
    for key, value in price.model_dump().items():
        if value is not None:
            setattr(result, key, value)
    try: 
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Price could not be updated")
    await session.refresh(result)
    return result

@router.delete("/{company_ticker}/{date}", response_model=PriceSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def delete_price(company_ticker: str, date: datetime, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a price by company ticker and date.
    """
    result = await get_or_404(Price, session, (company_ticker, date))
    await session.delete(result)
    await session.commit()
    return result
