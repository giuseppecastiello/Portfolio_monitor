from pydantic import Field
from src.schemas import CustomModel


class PortfolioSchema(CustomModel):
    """
    Schema for portfolio data.
    """
    name: str = Field(..., description="Name of the portfolio", max_length=30)

class PortfolioReadSchema(PortfolioSchema):
    """
    Schema for reading portfolio data.
    """
    id: int = Field(..., description="ID of the portfolio")