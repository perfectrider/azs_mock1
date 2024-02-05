# import logging
import uvicorn

from fastapi import FastAPI
from src.router import router


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger()


app = FastAPI(
    title="ttnft_Mock_service"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8001)