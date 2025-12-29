from pathlib import Path
from pypdf import PdfReader
from typing import List
import uuid

def save_upload_file(upload_file, destination: Path):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "wb") as f:
        f.write(upload_file.file.read())
    return destination

def num_pages(pdf_path: Path) -> int:
    reader = PdfReader(str(pdf_path))
    return len(reader.pages)

def make_doc_id() -> str:
    return uuid.uuid4().hex
