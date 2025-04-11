from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from src.database import Base

class Company(Base):
    __tablename__ = "companies"

    ticker: Mapped[str] = mapped_column(String(10), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    positions: Mapped[List["Position"]] = relationship("Position", back_populates="company", cascade="all, delete-orphan")
    prices: Mapped[List["Price"]] = relationship("Price", back_populates="company", cascade="all, delete-orphan")
