from fastapi import UploadFile, HTTPException
from app.core.config import settings
import shutil
import uuid
from pathlib import Path

class UploadService:

    ALLOWED_EXTENSIONS = {
        ".csv",
        ".xlsx",
        ".json"
    }

    @staticmethod
    async def upload(file: UploadFile):

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

   

        return {
            "filename": file.filename,
            "stored_as": unique_filename,
            "path": str(file_path),
            "content_type": file.content_type,
            "message": "File uploaded successfully"
        }