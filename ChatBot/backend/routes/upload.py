from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
from uuid import uuid4 # generate unique filename


# set router for upload endpoint
router = APIRouter(
    prefix="/upload",  
    tags=["File Upload"]
)


# directory where uploaded files will be saved
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# POST endpoint to handle file uploads
@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    
    
    try:
        # generate a unique filename to prevent overwriting existing files
        filename = f"{uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file to disk
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # return in JSON format
        return {
            "filename": filename,
            "path": file_path,
            "content_type": file.content_type
        }

    #if raise error if there is one during the upload or save
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
