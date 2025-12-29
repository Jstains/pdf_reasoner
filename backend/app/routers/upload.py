from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from ..utils import save_upload_file, num_pages, make_doc_id
from ..ingestion import ingest_pdf
from ..models import UploadResponse
from ..config import UPLOAD_DIR

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    doc_id = make_doc_id()
    dest = Path(UPLOAD_DIR) / f"{doc_id}.pdf"
    try:
        save_upload_file(file, dest)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        pages = ingest_pdf(doc_id, dest)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return UploadResponse(doc_id=doc_id, filename=file.filename, pages=pages)
