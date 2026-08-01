from fastapi import APIRouter, UploadFile, File

from app.services.upload_service import UploadService

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await UploadService.upload(file)