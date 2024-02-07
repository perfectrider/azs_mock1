import uvicorn

from fastapi import FastAPI
from src.router import router


app = FastAPI(
    title="ttnft_Mock_service"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8001)