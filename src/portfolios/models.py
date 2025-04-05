from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
