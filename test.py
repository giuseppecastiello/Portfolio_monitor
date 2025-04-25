from yfinance import Ticker
from src.yfinance_cache import session
ticker = Ticker('KWEB.AS', session=session)
print(ticker.info['shortName'])
print(ticker.info['sector'])