from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database.database import get_db

from app.models.pipeline import Pipeline
from app.models.pipeline_step import PipelineStep

from app.repositories.pipeline_repository import PipelineRepository
from app.repositories.pipeline_step_repository import PipelineStepRepository
from app.repositories.dataset_repository import DatasetRepository

from app.services.pipeline_service import PipelineService


router = APIRouter(
    prefix="/pipelines",
    tags=["Pipeline"]
)


@router.post("/")
def create_pipeline(
    name: str,
    dataset_id: str,
    db: Session = Depends(get_db)
):

    pipeline = Pipeline(
        pipeline_id=str(uuid.uuid4()),
        name=name,
        dataset_id=dataset_id,
        status="CREATED",
        created_at=datetime.now()
    )

    return PipelineRepository.create(
        db,
        pipeline
    )

@router.post("/{pipeline_id}/steps")
def add_pipeline_step(
    pipeline_id: str,
    operation: str,
    step_order: int,
    db: Session = Depends(get_db)
):

    pipeline = PipelineRepository.get_by_id(
        db,
        pipeline_id
    )

    if pipeline is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found."
        )

    step = PipelineStep(
        pipeline_id=pipeline_id,
        step_order=step_order,
        operation=operation,
        status="PENDING",
        created_at=datetime.now()
    )

    return PipelineStepRepository.create(
        db,
        step
    )


@router.get("/{pipeline_id}/steps")
def get_pipeline_steps(
    pipeline_id: str,
    db: Session = Depends(get_db)
):

    pipeline = PipelineRepository.get_by_id(
        db,
        pipeline_id
    )

    if pipeline is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found."
        )

    return PipelineStepRepository.get_by_pipeline_id(
        db,
        pipeline_id
    )



@router.post("/{pipeline_id}/run")
def run_pipeline(
    pipeline_id: str,
    db: Session = Depends(get_db)
):

    pipeline = PipelineRepository.get_by_id(
        db,
        pipeline_id
    )

    if pipeline is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found."
        )

    dataset = DatasetRepository.get_by_id(
        db,
        pipeline.dataset_id
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    steps = PipelineStepRepository.get_by_pipeline_id(
        db,
        pipeline_id
    )

    df = PipelineService.load_dataset(dataset)

    results = []

    for step in steps:

        operation = PipelineService.normalize_operation(
            step.operation
        )

        if operation == "CLEAN":

            df, result = PipelineService.execute_clean(
                df,
                dataset
            )

        elif operation == "VALIDATE":

            result = PipelineService.execute_validate(df)

        elif operation == "TRANSFORM":

            df, result = PipelineService.execute_transform(
                df,
                dataset
            )

        elif operation == "PROFILE":

            result = PipelineService.execute_profile(
                df,
                dataset
            )

        else:

            raise HTTPException(
                status_code=400,
                detail=f"Unsupported operation: {operation}"
            )

        results.append(result)

    return {
        "message": "Pipeline executed",
        "pipeline_id": pipeline_id,
        "results": results
    }


