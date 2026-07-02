from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    logger.info("DataForge Started")

    yield


app = FastAPI(
    title="DataForge",
    description="Self-Service ETL & Data Engineering Platform",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def home():

    return {
        "message": "Welcome to DataForge",
        "version": "1.0.0",
        "status": "running"
    }