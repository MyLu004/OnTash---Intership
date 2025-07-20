from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os
import io

router = APIRouter(
    prefix="/process",
    tags=["File Processing"]
)

@router.post("/")
async def process_uploaded_file(file: UploadFile = File(...)):
    try:
        content = ""

        if file.content_type == "application/pdf":
            pdf_bytes = await file.read()
            pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in pdf:
                content += page.get_text()
            pdf.close()

        elif file.content_type.startswith("image/"):
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            content = pytesseract.image_to_string(image)

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        return {"text": content.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
