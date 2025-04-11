from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database import get_async_session
from src.companies.models import Company
from src.companies.schemas import CompanySchema, CompanyUpdateSchema

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)

@router.get("/", response_model=list[CompanySchema])
async def get_companies(session: AsyncSession = Depends(get_async_session)):
    """
    Get all companies.
    """
    result = await session.scalars(select(Company))
    companies = result.fetchall()
    return companies

@router.get("/{company_ticker}", response_model=CompanySchema)
async def get_company(company_ticker: str, session: AsyncSession = Depends(get_async_session)):
    """
    Get a company by Ticker.
    """
    result = await session.get(Company, company_ticker)
    if result is None:
        return {"error": "Company not found"}
    return result

@router.post("/add", response_model=CompanySchema)
async def add_company(company: CompanySchema, session: AsyncSession = Depends(get_async_session)):
    """
    Add a new company.
    """
    new_company = Company(**company.model_dump())
    result = await session.execute(select(Company).where(Company.ticker == new_company.ticker))
    existing_company = result.scalar_one_or_none()
    if existing_company:
        raise HTTPException(status_code=400, detail="Company with this ticker already exists")
    session.add(new_company)
    await session.commit()
    await session.refresh(new_company)
    return new_company

@router.delete("/{company_ticker}", response_model=CompanySchema)
async def delete_company(company_ticker: str, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a company by Ticker.
    """
    result = await session.get(Company, company_ticker)
    if result is None:
        return {"error": "Company not found"}
    await session.delete(result)
    await session.commit()
    return result

@router.put("/{company_ticker}", response_model=CompanySchema)
async def update_company(company_ticker: str, company: CompanyUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Update a company by Ticker.
    """
    result = await session.get(Company, company_ticker)
    if result is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for key, value in company.model_dump().items():
        if value is not None:
            setattr(result, key, value)
    await session.commit()
    await session.refresh(result)
    return result
