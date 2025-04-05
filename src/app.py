from fastapi import FastAPI
from uvicorn import run

app = FastAPI(title='Portfolio_monitor_api', version='0.1.0')

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    run(app, port='8000', host='127.0.0.1')
