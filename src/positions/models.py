from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Position(Base):
    __tablename__ = "positions"
    # bug with primary key
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    portfolio = relationship("Portfolio", back_populates="positions")
    company_ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    company = relationship("Company", back_populates="positions")
    quantity: Mapped[int] = mapped_column(nullable=False)
