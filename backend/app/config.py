import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

VECTORSTORE_DIR = Path(os.getenv("VECTORSTORE_DIR", UPLOAD_DIR / "vectorstores"))
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

# chunking config
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Models / API keys
# For LLM (Gemini) - set GOOGLE_API_KEY or GEMINI_API_KEY in env or .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY", "")
GEMINI_CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.0-flash")
# HuggingFace model to use for embeddings (local, free)
HUGGINGFACE_EMBED_MODEL = os.getenv("HUGGINGFACE_EMBED_MODEL", "sentence-transformers/all-mpnet-base-v2")

def vectorstore_path_for_doc(doc_id: str) -> Path:
    p = VECTORSTORE_DIR / doc_id
    p.mkdir(parents=True, exist_ok=True)
    return p
