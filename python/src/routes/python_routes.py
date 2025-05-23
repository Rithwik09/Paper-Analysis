from fastapi import APIRouter, File, UploadFile
from controllers.file import analyze_file  # Import the correct one

router = APIRouter()

@router.post("/analyze")
async def upload_and_analyze(pdf: UploadFile = File(...)):
    return await analyze_file(pdf)
