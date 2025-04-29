from io import StringIO
from pandas import read_csv
from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.database import get_async_session
from src.util import get_or_404, get_responses
from src.positions.models import Position
from src.positions.schemas import PositionSchema, PositionUpdateSchema
from src.prices.models import CurrencyEnum
from src.companies.routers import get_company, add_company
from src.companies.schemas import CompanySchema

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

async def check_position(position: PositionSchema, session: AsyncSession):
    new_position = Position(**position.model_dump())
    try:
        await get_company(new_position.company_ticker, session)
    except HTTPException as exception:
        if exception.status_code == 404:
            await add_company(CompanySchema(ticker=new_position.company_ticker), session)
        else:
            raise HTTPException(exception.status_code, exception.detail, exception.headers)
    return new_position

@router.post("/add", response_model=PositionSchema, status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def add_position(position: PositionSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Add a new position.
    """
    new_position = await check_position(position, session)
    session.add(new_position)
    try:
        await session.commit()
    except IntegrityError as e:
        print(e.detail)
        raise HTTPException(status_code=400, detail="Position could not be added")
    await session.refresh(new_position)
    return new_position

@router.post("/add_bulk", response_model=list[PositionSchema], status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def add_positions(positions: list[PositionSchema], session: AsyncSession = Depends(get_async_session)):
    """
    Add a bulk of new positions.
    """
    new_positions = [await check_position(position, session) for position in positions]
    session.add_all(new_positions)
    try:
        await session.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail="One or more positions could not be added")
    for position in new_positions:
        await session.refresh(position)
    return new_positions

@router.post("/{portfolio_id}/upload_csv", response_model=list[PositionSchema], status_code=201, responses={k: responses[k] for k in [201, 400, 422]})
async def import_portfolio_positions(portfolio_id: int, file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    """
    Import data from csv file and create new positions associated with the given portfolio_id.
    """
    contents = await file.read()
    try:
        contents_str = contents.decode('utf-8')
        df = read_csv(StringIO(contents_str))
    except Exception:
        raise HTTPException(status_code=400, detail="The uploaded file could not be parsed as a CSV")
    positions = []
    for _, row in df.iterrows():
        try:
            positions.append(PositionSchema(
                portfolio_id=portfolio_id, 
                company_ticker=row['ticker'],
                quantity=row['quantity'],
                date=row['date'],
                price=row['price'],
                currency=CurrencyEnum.symbol_to_currency(row['currency']),
                type=row['type']
                ))
        except ValidationError as ve:
            for error in ve.errors():
                print(error)
            raise HTTPException(status_code=400, detail=f"{Position.__name__} {row} is not a valid {Position.__name__}")
    positions = await add_positions(positions, session)
    return positions

@router.get("/{position_id}", response_model=PositionSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def get_position(position_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get a position by ID.
    """
    return await get_or_404(Position, session, position_id)

@router.get("/portfolio/{portfolio_id}", response_model=list[PositionSchema], responses={k: responses[k] for k in [200, 404, 422]})
async def get_positions_of_a_portfolio(portfolio_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get a list of positions by portfolio ID.
    """
    result = await session.scalars(select(Position).where(Position.portfolio_id == portfolio_id))
    positions = result.fetchall()
    if not positions:
        raise HTTPException(status_code=404, detail=f"{Position.__name__}s not found for the given portfolio ID")
    return positions

@router.put("/{position_id}", response_model=PositionSchema, responses={k: responses[k] for k in [200, 400, 404, 422]})
async def update_position(position_id: int, position: PositionUpdateSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Update a position by ID.
    """
    result = await get_or_404(Position, session, position_id)
    for key, value in position.model_dump().items():
        if value is not None:
            setattr(result, key, value)
    try: 
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Position could not be updated")
    await session.refresh(result)
    return result

@router.delete("/{position_id}", response_model=PositionSchema, responses={k: responses[k] for k in [200, 404, 422]})
async def delete_position(position_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a position by ID.
    """
    result = await get_or_404(Position, session, position_id)
    await session.delete(result)
    await session.commit()
    return result

@router.delete("/delete_all/", responses={k: responses[k] for k in [200, 422]})
async def delete_all_positions(session: AsyncSession = Depends(get_async_session)):
    """
    Delete all positions.
    """
    await session.execute(delete(Position))
    await session.commit()
    return {'detail': 'done'}
