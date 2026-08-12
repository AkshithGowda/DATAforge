from fastapi import APIRouter, HTTPException

from app.schemas.transformation import TransformationRequest

from app.services.transformation_service import TransformationService


router = APIRouter(
    prefix="/transform",
    tags=["Transformation"]
)


@router.post("/")
async def transform_dataset(request: TransformationRequest):

    return {
        "message": "Transformation request received",
        "dataset_id": request.dataset_id
    }