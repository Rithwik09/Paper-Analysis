from fastapi import APIRouter, File, UploadFile, Request
from controllers.file import analyze_file  # Import the correct one

router = APIRouter()

@router.post("/analyze")
# async def upload_and_analyze(pdf: UploadFile = File(...)):
#     return await analyze_file(pdf)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    print("Headers:", request.headers)
    print("Content-Type:", request.headers.get("content-type"))
    print("Received file:", file.filename if file else "No file")
    return await analyze_file(request, file)