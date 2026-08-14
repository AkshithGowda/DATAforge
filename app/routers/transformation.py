from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.dataset_repository import DatasetRepository
from app.schemas.transformation import TransformationRequest
from app.services.transformation_service import TransformationService
from pathlib import Path

from app.core.config import settings
from app.services.dataset_service import DatasetService
from datetime import datetime

from app.models.transformation_history import TransformationHistory
from app.repositories.transformation_history_repository import TransformationHistoryRepository
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

    input_rows = len(df)

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

    history = TransformationHistory(
        dataset_id=dataset.dataset_id,
        operation="TRANSFORMATION",
        input_rows=input_rows,
        output_rows=len(df),
        created_at=datetime.now()
    )

    TransformationHistoryRepository.create(db, history)

@router.get("/history/{dataset_id}")
def get_history(
        dataset_id: str,
        db: Session = Depends(get_db)
 ):
    history = TransformationHistoryRepository.get_by_dataset_id(
        db,
        dataset_id
    )

    return history

    return {
        "message": "Transformation successful",
        "dataset_id": dataset.dataset_id,
        "rows": len(df),
        "columns": list(df.columns),
        "transformed_file": str(transformed_file)
    }