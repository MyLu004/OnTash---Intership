from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os
import io


'''
LIBRARY IMPORT DESCRIPTION
    - fitz : PyMuPDF - used for reading PDF files
    - PIL - Pillow : user for handling images
    - pytesseract : tesseract OCR, used to extract text from images
    - io : handling byte stream in memory
'''

# router for processing the file
router = APIRouter(
    prefix="/process", 
    tags=["File Processing"]
)

# POST route to accept an uploaded file and extract text content
@router.post("/")
async def process_uploaded_file(file: UploadFile = File(...)):
    try:
        content = "" #initial the extract content


        #case 1 : if the uploaded file is a PDF
        if file.content_type == "application/pdf":
            pdf_bytes = await file.read()
            pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in pdf:
                content += page.get_text()
            pdf.close()


        #case 2 : if the uploaded file is a images
        elif file.content_type.startswith("image/"):
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            content = pytesseract.image_to_string(image)

        #case 3 : unsupport file type
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        # rturn the extracted text with whitespace trimmed
        return {"text": content.strip()}

    # handle unexpected errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
