from sqlalchemy import String, ForeignKey   
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.database import Base

class Price(Base):
    __tablename__ = "prices"

    company_ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    company: Mapped["Company"] = relationship(back_populates="prices")
    date: Mapped[datetime] = mapped_column(primary_key=True, index=True)
    close: Mapped[float] = mapped_column(nullable=False)
