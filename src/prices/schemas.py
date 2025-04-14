from pydantic import Field
from typing import Optional
from datetime import date
from src.schemas import CustomModel


class PriceSchema(CustomModel):
    """
    Schema for price data.
    """
    company_ticker: str = Field(..., description="Ticker of the company", max_length=10)
    market_date: date = Field(..., description="Date of the price")
    close: float = Field(..., description="Close price", gt=0)

class PriceUpdateSchema(CustomModel):
    """
    Schema for updating price data.
    """
    company_ticker: Optional[str] = Field(None, description="Ticker of the company", max_length=10)
    market_date: Optional[date] = Field(None, description="Date of the price")
    close: Optional[float] = Field(None, description="Close price", gt=0)