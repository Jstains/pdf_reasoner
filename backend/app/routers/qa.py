from fastapi import APIRouter, HTTPException
from typing import List

from ..models import QARequest, QAResponse, SourceItem
from ..agent import get_agent_executor
from ..ingestion import retrieve_sources

router = APIRouter()

@router.post("/qa", response_model=QAResponse)
async def ask_question(req: QARequest):
    if not req.question or not req.doc_id:
        raise HTTPException(status_code=400, detail="question and doc_id are required")

    # 1) run agent to get the answer text (agent will call search_pdf tool)
    agent_exec = get_agent_executor()
    try:
        agent_result = agent_exec.invoke({
            "input": req.question,
            "doc_id": req.doc_id
        })
        answer = agent_result.get("output") or agent_result.get("result") or str(agent_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent failed: {e}")

    # 2) retrieve top-k chunks for structured sources to show in UI
    try:
        docs_and_scores = retrieve_sources(req.doc_id, req.question, k=req.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {e}")

    sources: List[SourceItem] = []
    for doc, score in docs_and_scores:
        meta = doc.metadata or {}
        page = int(meta.get("page", 0)) or 0
        chunk_id = meta.get("chunk_id", "")
        snippet = doc.page_content[:400]
        sources.append(SourceItem(page=page, chunk_id=chunk_id, text=snippet, score=float(score)))

    return QAResponse(answer=answer, sources=sources)
