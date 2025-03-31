from fastapi import  File, UploadFile
import shutil
import  os  

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def analyze_file(pdf: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
        return {"message": "File uploaded successfully", "filename" : pdf.filename }
    except Exception as e:
        return {"error": str(e)}