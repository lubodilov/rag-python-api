# app/routes.py

from fastapi import APIRouter, HTTPException
from app.services import ingest_service
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class IngestRequest(BaseModel):
    files: List[str]
    datasetId: str

class FailedFile(BaseModel):
    file_url: str
    error: str

class IngestResponse(BaseModel):
    message: str
    ingestedFiles: int
    datasetId: str
    failedFiles: Optional[List[FailedFile]] = None

@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    try:
        result = await ingest_service.ingest_files(request.files, request.datasetId)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
