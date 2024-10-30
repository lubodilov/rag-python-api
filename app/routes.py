# app/routes.py

from fastapi import APIRouter, HTTPException, Request
from app.services import ingest_service, retrieve_service
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Templates for UI (if implemented later)
templates = Jinja2Templates(directory="templates")

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

# Existing RetrieveRequest model and /retrieve endpoint
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

# New DeleteRequest model and /delete endpoint
class DeleteRequest(BaseModel):
    datasetId: str

@router.post("/delete")
async def delete_dataset(request: DeleteRequest):
    try:
        result = await ingest_service.delete_dataset(request.datasetId)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
