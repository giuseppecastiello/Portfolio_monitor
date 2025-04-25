from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from yfinance import Ticker
from src.database import get_async_session
from src.util import get_or_404, get_responses
from src.companies.models import Company
from src.companies.schemas import CompanySchema, CompanyUpdateSchema
from src.yfinance_cache import session as yfSession

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)

responses = get_responses(Company)

@router.get("/", response_model=list[CompanySchema])
async def get_companies(session: AsyncSession = Depends(get_async_session)):
    """
    Get all companies.
    """
    result = await session.scalars(select(Company))
    companies = result.fetchall()
    return companies

async def check_company(company: CompanySchema, session: AsyncSession) -> Company:
    new_company = Company(**company.model_dump())
    result = await session.execute(select(Company).where(Company.ticker == new_company.ticker))
    existing_company = result.scalar_one_or_none()
    if existing_company:
        raise HTTPException(status_code=400, detail="Company with this ticker already exists")
    ticker = Ticker(new_company.ticker, session=yfSession)
    try:
        new_company.name = ticker.info['shortName']
    except KeyError:
        raise HTTPException(status_code=400, detail=f"No Company with this ticker ({new_company.ticker}) was found")
    if 'sector' in ticker.info.keys():
        new_company.sector = ticker.info['sector']
    return new_company

@router.post("/add", response_model=CompanySchema, status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def add_company(company: CompanySchema, session: AsyncSession = Depends(get_async_session)):
    """
    Add a new company.
    """
    new_company = await check_company(company, session)
    session.add(new_company)
    await session.commit()
    await session.refresh(new_company)
    return new_company

@router.post("/add_bulk", response_model=list[CompanySchema], status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def add_companies(companies: list[CompanySchema], session: AsyncSession = Depends(get_async_session)):
    """
    Add a bulk of new companies.
    """
    new_companies = [await check_company(company, session) for company in companies]
    
    session.add_all(new_companies)
    await session.commit()
    for new_company in new_companies:
        await session.refresh(new_company)
    return new_companies

@router.get("/{company_ticker}", response_model=CompanySchema, responses={k: responses[k] for k in [200, 404, 422]})
async def get_company(company_ticker: str, session: AsyncSession = Depends(get_async_session)):
    """
    Get a company by Ticker.
    """
    return await get_or_404(Company, session, company_ticker)

@router.put("/{company_ticker}", response_model=CompanySchema, responses={k: responses[k] for k in [200, 400, 404, 422]})
async def update_company(company_ticker: str, company: CompanyUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Update a company by Ticker.
    """
    result = await get_or_404(Company, session, company_ticker)
    for key, value in company.model_dump().items():
        if value is not None:
            setattr(result, key, value)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Company could not be updated")
    await session.refresh(result)
    return result

@router.delete("/{company_ticker}", response_model=CompanySchema, responses={k: responses[k] for k in [200, 404, 422]})
async def delete_company(company_ticker: str, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a company by Ticker.
    """
    result = await get_or_404(Company, session, company_ticker)
    await session.delete(result)
    await session.commit()
    return result

@router.delete("/delete_all/", responses={k: responses[k] for k in [200, 422]})
async def delete_position(session: AsyncSession = Depends(get_async_session)):
    """
    Delete all companies.
    """
    await session.execute(delete(Company))
    await session.commit()
    return {'detail': 'done'}
