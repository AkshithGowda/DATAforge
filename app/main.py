from contextlib import asynccontextmanager
from app.routers import pipelines
from app.models.pipeline import Pipeline
from fastapi import FastAPI
from app.routers import datasets
from app.models.dataset import Dataset
from app.database.database import Base
from app.database.database import engine
from app.utils.logger import logger
from app.models.cleaning_history import CleaningHistory
from app.routers import upload, transformation
from app.models.transformation_history import TransformationHistory
from app.routers import transformation
from app.models.validation_history import ValidationHistory
from app.models.pipeline_step import PipelineStep


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


app.include_router(upload.router)
app.include_router(transformation.router)
app.include_router(datasets.router)
app.include_router(pipelines.router)

@app.get("/")
def home():

    return {
        "message": "Welcome to DataForge",
        "version": "1.0.0",
        "status": "running"
    }