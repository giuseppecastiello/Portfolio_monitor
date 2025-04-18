from datetime import date as pydate
from enum import Enum as pyEnum
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class TypeEnum(str, pyEnum):
    buy = "b"
    sell = "s"

class Position(Base):
    __tablename__ = "positions"
    
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    portfolio = relationship("Portfolio", back_populates="positions")
    company_ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    company = relationship("Company", back_populates="positions")
    quantity: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[pydate] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    type: Mapped[TypeEnum] = mapped_column(Enum(TypeEnum, name="typeenum"), nullable=False)
