from pydantic import Field
from typing import Optional
from src.schemas import CustomModel


class CompanySchema(CustomModel):
    """
    Schema for company data.
    """
    ticker: str = Field(..., description="Ticker symbol of the company", max_length=10)
    name: str = Field(..., description="Name of the company", max_length=30)
    sector: str = Field(None, description="Sector of the company", max_length=30)

class CompanyUpdateSchema(CustomModel):
    """
    Schema for updating an existing company.
    """
    ticker: Optional[str] = Field(None, description="Ticker symbol of the company", max_length=10)
    name: Optional[str] = Field(None, description="Name of the company", max_length=30)
    sector: Optional[str] = Field(None, description="Sector of the company", max_length=30)
