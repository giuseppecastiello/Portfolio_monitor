from datetime import date as pydate
from pydantic import Field
from typing import Optional
from src.schemas import CustomModel
from src.positions.models import TypeEnum

class PositionSchema(CustomModel):
    """
    Schema for position data.
    """
    portfolio_id: int = Field(..., description="ID of the portfolio", gt=0)
    company_ticker: str = Field(..., description="Ticker of the company", max_length=10)
    quantity: int = Field(..., description="Quantity of the position", gt=0)
    date: pydate = Field(..., description="Date of the position")
    price: float = Field(..., description="Price of the position")
    type: TypeEnum = Field(..., description="Type of the position (buy/sell)")

class PositionUpdateSchema(CustomModel):
    """
    Schema for updating position data.
    """
    portfolio_id: Optional[int] = Field(None, description="ID of the portfolio", gt=0)
    company_ticker: Optional[str] = Field(None, description="Ticker of the company", max_length=10)
    quantity: Optional[int] = Field(None, description="Quantity of the position", gt=0)
    date: Optional[pydate] = Field(..., description="Date of the position")
    price: Optional[float] = Field(..., description="Price of the position")
    type: Optional[TypeEnum] = Field(..., description="Type of the position (buy/sell)")
    