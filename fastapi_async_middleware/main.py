from fastapi import FastAPI
from data_service import DataService
from middleware import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)

data_service = DataService()

@app.get("/data")
async def read_data(input_data: str):
    data = await data_service.fetch_data(input_data)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
