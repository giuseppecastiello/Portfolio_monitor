from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.util import get_or_404, get_responses
from src.portfolios.models import Portfolio
from src.portfolios.schemas import PortfolioSchema, PortfolioReadSchema

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"]
)

responses = get_responses(Portfolio)

@router.get("/", response_model=list[PortfolioReadSchema])
async def get_portfolios(session: AsyncSession = Depends(get_async_session)):
    """
    Get all portfolios.
    """
    result = await session.scalars(select(Portfolio))
    portfolios = result.fetchall()
    return portfolios

@router.post("/add", response_model=PortfolioReadSchema, status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def add_portfolio(portfolio: PortfolioSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Add a new portfolio.
    """
    new_portfolio = Portfolio(**portfolio.model_dump())
    result = await session.execute(select(Portfolio).where(Portfolio.id == new_portfolio.id))
    existing_portfolio = result.scalar_one_or_none()
    if existing_portfolio:
        raise HTTPException(status_code=400, detail="Portfolio with this id already exists")
    session.add(new_portfolio)
    await session.commit()
    await session.refresh(new_portfolio)
    return new_portfolio

@router.get("/{portfolio_id}", response_model=PortfolioReadSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def get_portfolio(portfolio_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get a portfolio by ID.
    """
    return await get_or_404(Portfolio, session, portfolio_id)

@router.put("/{portfolio_id}", response_model=PortfolioReadSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def update_portfolio(portfolio_id: str, portfolio: PortfolioSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Update a portfolio by ID.
    """
    result = await get_or_404(Portfolio, session, portfolio_id)
    for key, value in portfolio.model_dump().items():
        if value is not None:
            setattr(result, key, value)
    await session.commit()
    await session.refresh(result)
    return result

@router.delete("/{portfolio_id}", response_model=PortfolioReadSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def delete_portfolio(portfolio_id: str, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a portfolio by ID.
    """
    result = await get_or_404(Portfolio, session, portfolio_id)
    await session.delete(result)
    await session.commit()
    return result
