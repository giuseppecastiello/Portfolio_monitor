from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
   pass

session = CachedLimiterSession(
   limiter=Limiter(RequestRate(10, Duration.SECOND)),  # max 2 requests per 5 seconds
   bucket_class=MemoryQueueBucket,
   backend=SQLiteCache("yfinance.cache"),
)