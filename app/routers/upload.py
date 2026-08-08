from fastapi import APIRouter, UploadFile, File
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.upload_service import UploadService

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
   return await UploadService.upload(file, db)

