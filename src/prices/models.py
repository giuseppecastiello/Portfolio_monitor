from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.database import Base

class Price(Base):
    __tablename__ = "prices"

    ticker: Mapped[str] = mapped_column(String(10), primary_key=True, index=True)
    company: Mapped["Company"] = relationship("Company", back_populates="prices")
    date: Mapped[datetime] = mapped_column(primary_key=True, index=True)
    open: Mapped[float] = mapped_column(nullable=False)
    close: Mapped[float] = mapped_column(nullable=False)
    high: Mapped[float] = mapped_column(nullable=False)
    low: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[int] = mapped_column(nullable=False)
