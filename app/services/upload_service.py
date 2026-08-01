from app.repositories.dataset_repository import DatasetRepository
from fastapi import UploadFile, HTTPException
from app.core.config import settings
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.repositories.dataset_repository import DatasetRepository

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

        dataset = Dataset(
            dataset_id=str(uuid.uuid4()),
            original_filename=file.filename,
            stored_filename=unique_filename,
            extension=extension,
            file_size_mb=round(file_size_mb, 2),
            upload_time=datetime.now(),
            status="UPLOADED"
        )

        DatasetRepository.create(db, dataset)

        return {
            "message": "File uploaded successfully",
            "dataset_id": dataset.dataset_id,
            "filename": dataset.original_filename,
            "status": dataset.status
        }