"""
Ingest PDFs using LangChain loaders + HuggingFace embeddings + FAISS.
Corrected so each chunk keeps the correct original PDF page number.
"""

from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from .config import CHUNK_SIZE, CHUNK_OVERLAP, HUGGINGFACE_EMBED_MODEL, vectorstore_path_for_doc

def _get_embeddings():
    return HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBED_MODEL)

def ingest_pdf(doc_id: str, pdf_path: Path) -> int:
    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()  # list of Documents (one per page)
    num_pages = len(pages)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    docs = []
    for page_number, page_doc in enumerate(pages):
        page_doc.metadata["page"] = page_number + 1  # FIX: make pages 1-based
        page_chunks = splitter.split_documents([page_doc])

        for idx, chunk in enumerate(page_chunks):
            chunk.metadata["page"] = page_number + 1   # FIX: keep page number
            chunk.metadata["doc_id"] = doc_id
            chunk.metadata["chunk_id"] = f"{doc_id}_p{page_number+1}_c{idx}"

            docs.append(chunk)

    embeddings = _get_embeddings()
    vs = FAISS.from_documents(docs, embeddings)

    store_dir = vectorstore_path_for_doc(doc_id)
    vs.save_local(str(store_dir))

    return num_pages

def load_vectorstore(doc_id: str) -> FAISS:
    embeddings = _get_embeddings()
    store_dir = vectorstore_path_for_doc(doc_id)
    return FAISS.load_local(str(store_dir), embeddings, allow_dangerous_deserialization=True)

def retrieve_sources(doc_id: str, query: str, k: int = 5) -> List[Tuple]:
    vs = load_vectorstore(doc_id)
    return vs.similarity_search_with_score(query, k=k)
