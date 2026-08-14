from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.dataset import Dataset
from app.repositories.dataset_repository import DatasetRepository
from app.services.dataset_service import DatasetService

import shutil
import uuid
from pathlib import Path
from datetime import datetime
from app.services.cleaning_service import CleaningService
from app.services.validation_service import ValidationService

class UploadService:

    ALLOWED_EXTENSIONS = {
        ".csv",
        ".xlsx",
        ".json"
    }

    @staticmethod
    async def upload(file: UploadFile, db: Session):

        extension = "." + file.filename.split(".")[-1].lower()

        if extension not in UploadService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type '{extension}'. Only CSV, Excel, and JSON files are allowed."
        )

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        file_size_mb = file_size / (1024 * 1024)

        if file_size_mb > settings.MAX_FILE_SIZE_MB:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds {settings.MAX_FILE_SIZE_MB} MB."
        )


       
        unique_filename = f"{uuid.uuid4()}{extension}"

        file_path = Path(settings.UPLOAD_DIR) / unique_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        dataset_analysis = DatasetService.analyze_dataset(
            file_path=file_path,
            extension=extension
        )

        df = DatasetService.read_dataset(
            file_path=file_path,
            extension=extension
        )

        cleaned_df, cleaning_report = CleaningService.clean_dataset(df)
        
        validation_report = ValidationService.validate_dataset(cleaned_df)

        cleaned_file_path = CleaningService.save_cleaned_dataset(
            cleaned_df,
            file.filename
        )

        dataset = Dataset(
            dataset_id=str(uuid.uuid4()),
            original_filename=file.filename,
            stored_filename=unique_filename,
            extension=extension,
            file_size_mb=round(file_size_mb, 2),
            upload_time=datetime.now(),
            status="UPLOADED"
        )

        print("ABOUT TO SAVE DATASET:", dataset.dataset_id)

        DatasetRepository.create(db, dataset)

        print("DATASET SAVED:", dataset.dataset_id)


        return {
            "message": "File uploaded successfully",
            "dataset_id": dataset.dataset_id,
            "filename": dataset.original_filename,
            "status": dataset.status,
            "file_size_mb": dataset.file_size_mb,
            "analysis": dataset_analysis,
            "cleaning_report": cleaning_report,
            "validation_report": validation_report,
            "cleaned_file": str(cleaned_file_path)
        }