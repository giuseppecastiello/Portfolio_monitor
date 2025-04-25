from pydantic import Field
from typing import Optional
from src.schemas import CustomModel


class CompanySchema(CustomModel):
    """
    Schema for company data.
    """
    ticker: str = Field(..., description="Ticker symbol of the company", max_length=20)
    name: Optional[str] = Field(None, description="Name of the company", max_length=50)
    sector: Optional[str] = Field(None, description="Sector of the company", max_length=50)

class CompanyUpdateSchema(CustomModel):
    """
    Schema for updating an existing company.
    """
    ticker: Optional[str] = Field(None, description="Ticker symbol of the company", max_length=20)
    name: Optional[str] = Field(None, description="Name of the company", max_length=50)
    sector: Optional[str] = Field(None, description="Sector of the company", max_length=50)
