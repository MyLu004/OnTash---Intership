from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
from uuid import uuid4

router = APIRouter(
    prefix="/upload",
    tags=["File Upload"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate unique filename to avoid collisions
        filename = f"{uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file to disk
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return {
            "filename": filename,
            "path": file_path,
            "content_type": file.content_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
