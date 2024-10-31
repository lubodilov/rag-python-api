# app/routes.py

from fastapi import APIRouter, HTTPException, Request
from app.services import ingest_service, retrieve_service
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Initialize templates
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

# Existing DeleteRequest model and /delete endpoint
class DeleteRequest(BaseModel):
    datasetId: str

@router.post("/delete")
async def delete_dataset(request: DeleteRequest):
    try:
        result = await ingest_service.delete_dataset(request.datasetId)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# New UI routes
@router.get("/")
async def read_datasets(request: Request):
    # Get all unique datasetIds
    dataset_ids = await ingest_service.get_dataset_ids()
    return templates.TemplateResponse("index.html", {"request": request, "datasets": dataset_ids})

@router.get("/dataset/{datasetId}")
async def read_dataset(request: Request, datasetId: str):
    # Retrieve chunks associated with the datasetId
    chunks = await ingest_service.get_chunks_by_dataset(datasetId)
    return templates.TemplateResponse("dataset.html", {"request": request, "datasetId": datasetId, "chunks": chunks})
