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

    return {
        "message": "Transformation successful",
        "dataset_id": dataset.dataset_id,
        "rows": len(df),
        "columns": list(df.columns)
    }