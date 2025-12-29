from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .config import UPLOAD_DIR
from .routers import upload, qa

app = FastAPI(title="Agent-Based PDF Reasoner (Backend)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(upload.router, prefix="/api")
app.include_router(qa.router, prefix="/api")

# Serve uploads for frontend PDF viewer
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

@app.get("/")
async def root():
    return {"status": "ok"}
