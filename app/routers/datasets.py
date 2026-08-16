
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from app.services.cleaning_service import CleaningService
from app.database.database import get_db
from app.repositories.dataset_repository import DatasetRepository
from app.services.dataset_service import DatasetService
from app.core.config import settings
from datetime import datetime
from app.services.validation_service import ValidationService
from app.models.cleaning_history import CleaningHistory
from app.repositories.cleaning_history_repository import CleaningHistoryRepository
from app.models.validation_history import ValidationHistory
from app.repositories.validation_history_repository import ValidationHistoryRepository

router = APIRouter(
    prefix="/datasets",
    tags=["Dataset"]
)


@router.post("/{dataset_id}/clean")
def clean_dataset(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    dataset = DatasetRepository.get_by_id(
        db,
        dataset_id
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

    df, cleaning_info = CleaningService.clean_dataset(df)

    history = CleaningHistory(
        dataset_id=dataset.dataset_id,
        original_rows=cleaning_info["original_rows"],
        final_rows=cleaning_info["final_rows"],
        duplicates_removed=cleaning_info["duplicates_removed"],
        missing_values_before=cleaning_info["missing_values_before"],
        missing_values_after=cleaning_info["missing_values_after"],
        created_at=datetime.now()
    )

    CleaningHistoryRepository.create(db, history)

    cleaned_file = CleaningService.save_cleaned_dataset(
        df,
        dataset.original_filename
    )

    return {
        "message": "Dataset cleaned successfully",
        "dataset_id": dataset.dataset_id,
        "cleaning_info": cleaning_info,
        "cleaned_file": str(cleaned_file)
    }


@router.get("/{dataset_id}/cleaning-history")
def get_cleaning_history(
    dataset_id: str,
    db: Session = Depends(get_db)
):

    history = CleaningHistoryRepository.get_by_dataset_id(
        db,
        dataset_id
    )

    return history

@router.post("/{dataset_id}/validate")
def validate_dataset(
    dataset_id: str,
    db: Session = Depends(get_db)
):

    dataset = DatasetRepository.get_by_id(
        db,
        dataset_id
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

    required_columns = [
        "movie_title",
        "imdb_score",
        "title_year"
    ]

    validation = ValidationService.validate_dataset(
        df,
        required_columns
    )

    history = ValidationHistory(
        dataset_id=dataset.dataset_id,
        valid=validation["valid"],
        error_count=len(validation["errors"]),
        warning_count=len(validation["warnings"]),
        created_at=datetime.now()
    )

    ValidationHistoryRepository.create(db, history)


    return {
        "message": "Dataset validation completed",
        "dataset_id": dataset.dataset_id,
        "validation": validation
    }



@router.get("/{dataset_id}/validation-history")
def get_validation_history(
    dataset_id: str,
    db: Session = Depends(get_db)
):

    history = ValidationHistoryRepository.get_by_dataset_id(
        db,
        dataset_id
    )

    return history