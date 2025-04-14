from pydantic import Field
from typing import Optional
from src.schemas import CustomModel


class PositionSchema(CustomModel):
    """
    Schema for position data.
    """
    portfolio_id: int = Field(..., description="ID of the portfolio", gt=0)
    company_ticker: str = Field(..., description="Ticker of the company", max_length=10)
    quantity: int = Field(..., description="Quantity of the position", gt=0)

class PositionUpdateSchema(CustomModel):
    """
    Schema for updating position data.
    """
    portfolio_id: Optional[int] = Field(None, description="ID of the portfolio", gt=0)
    company_ticker: Optional[str] = Field(None, description="Ticker of the company", max_length=10)
    quantity: Optional[int] = Field(None, description="Quantity of the position", gt=0)