# app/routes.py

from fastapi import APIRouter, HTTPException
from app.services import ingest_service, retrieve_service
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Existing IngestRequest model and /ingest endpoint
class IngestRequest(BaseModel):
    files: List[str]
    datasetId: str

@router.post("/ingest")
async def ingest(request: IngestRequest):
    try:
        result = await ingest_service.ingest_files(request.files, request.datasetId)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# New RetrieveRequest model and /retrieve endpoint
class RetrieveRequest(BaseModel):
    prompt: str
    datasetId: str

@router.post("/retrieve")
async def retrieve(request: RetrieveRequest):
    try:
        results = await retrieve_service.retrieve_chunks(request.prompt, request.datasetId)
        return {
            "prompt": request.prompt,
            "datasetId": request.datasetId,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
