import uvicorn
from fastapi import FastAPI

from src.api_v1 import api_router
from src.config import settings
from src.utils import logger


app = FastAPI(docs_url="/")
app.include_router(router=api_router, prefix=f"{settings.api_v1_prefix}")

logger.debug(f"Starting application:\n{settings=}")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.LOG_LEVEL,
        workers=settings.WORKERS,
    )
