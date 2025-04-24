from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from src.database import Base
from enum import Enum as pyEnum

class CurrencyEnum(str, pyEnum):
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro
    JPY = "JPY"  # Japanese Yen
    GBP = "GBP"  # British Pound
    AUD = "AUD"  # Australian Dollar
    CAD = "CAD"  # Canadian Dollar
    CHF = "CHF"  # Swiss Franc
    CNY = "CNY"  # Chinese Yuan
    HKD = "HKD"  # Hong Kong Dollar
    NZD = "NZD"  # New Zealand Dollar
    SEK = "SEK"  # Swedish Krona
    SGD = "SGD"  # Singapore Dollar
    NOK = "NOK"  # Norwegian Krone

    def currency_to_symbol(self) -> str:
        symbols = {
            "USD": "$",
            "EUR": "€",
            "JPY": "¥",
            "GBP": "£",
            "AUD": "A$",
            "CAD": "C$",
            "CHF": "CHF",  # Franc doesn't have a unique symbol
            "CNY": "¥",
            "HKD": "HK$",
            "NZD": "NZ$",
            "SEK": "kr",
            "SGD": "S$",
            "NOK": "kr"
        }
        return symbols[self.value]
    
    @staticmethod
    def symbol_to_currency(symbol: str) -> "CurrencyEnum":
        symbols_to_currency = {
            "$": "USD",
            "€": "EUR",
            "¥": "JPY",
            "£": "GBP",
            "A$": "AUD",
            "C$": "CAD",
            "CHF": "CHF",
            "¥": "CNY",
            "HK$": "HKD",
            "NZ$": "NZD",
            "kr": "SEK",  # Could also map to NOK
            "S$": "SGD",
            "kr": "NOK",
        }
        currency_code = symbols_to_currency.get(symbol)
        if currency_code:
            return CurrencyEnum(currency_code)
        return None

class Price(Base):
    __tablename__ = "prices"
    
    company_ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    company: Mapped["Company"] = relationship(back_populates="prices")
    market_date: Mapped[date] = mapped_column(primary_key=True, index=True)
    close: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(Enum(CurrencyEnum, name='currencyenum'), nullable=False)
