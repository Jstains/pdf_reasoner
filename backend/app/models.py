from pydantic import BaseModel
from typing import Optional, List

class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    pages: int

class QARequest(BaseModel):
    question: str
    doc_id: str
    top_k: int = 5

class SourceItem(BaseModel):
    page: int
    chunk_id: str
    text: str
    score: float

class QAResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
