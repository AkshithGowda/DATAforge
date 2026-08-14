from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.dataset_repository import DatasetRepository
from app.schemas.transformation import TransformationRequest
from app.services.transformation_service import TransformationService
from pathlib import Path

from app.core.config import settings
from app.services.dataset_service import DatasetService

router = APIRouter(
    prefix="/transform",
    tags=["Transformation"]
)


@router.post("/")
async def transform_dataset(
    request: TransformationRequest,
    db: Session = Depends(get_db)
):

    dataset = DatasetRepository.get_by_id(
        db,
        request.dataset_id
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    file_path = Path(settings.UPLOAD_DIR) / dataset.stored_filename

    df = DatasetService.read_dataset(
        file_path=file_path,
        extension=dataset.extension
    )

    if request.rename_columns:
        df = TransformationService.rename_columns(
            df,
            request.rename_columns
        )

    if request.drop_columns:
        df = TransformationService.drop_columns(
            df,
            request.drop_columns
        )

    if request.select_columns:
        df = TransformationService.select_columns(
            df,
            request.select_columns
        )

    if request.filter_condition:
        df = TransformationService.filter_rows(
            df,
            request.filter_condition
        )

    if request.sort_column:
        df = TransformationService.sort_rows(
            df,
            request.sort_column,
            request.sort_ascending
        )

    transformed_file = TransformationService.save_transformed_dataset(
        df,
        dataset.original_filename
    )

    return {
        "message": "Transformation successful",
        "dataset_id": dataset.dataset_id,
        "rows": len(df),
        "columns": list(df.columns),
        "transformed_file": str(transformed_file)
    }