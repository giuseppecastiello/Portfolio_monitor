from fastapi import FastAPI
from uvicorn import run
from src.companies.routers import router as companies_router
from src.portfolios.routers import router as portfolios_router
from src.positions.routers import router as positions_router
from src.prices.routers import router as prices_router
from src.companies.models import Company
from src.portfolios.models import Portfolio
from src.positions.models import Position
from src.prices.models import Price

app = FastAPI(title='Portfolio_monitor_api', version='0.1.0')
app.include_router(companies_router)
app.include_router(portfolios_router)
app.include_router(positions_router)
app.include_router(prices_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    run(app, port='8000', host='127.0.0.1')
