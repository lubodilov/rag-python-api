# app/services/ingest_service.py

import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue
)

from app.utils import download_file_from_s3, extract_text_from_file, chunk_text
from app.config import (
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    MAX_CHUNK_SIZE,
)
import os

# Initialize the embedding model
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Initialize Qdrant client
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Ensure the collection exists
def create_qdrant_collection():
    collections = qdrant_client.get_collections()
    collection_names = [collection.name for collection in collections.collections]
    if QDRANT_COLLECTION_NAME not in collection_names:
        qdrant_client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

async def ingest_files(files: list, datasetId: str):
    if not files or not datasetId:
        raise ValueError("Files and datasetId are required")

    create_qdrant_collection()

    all_vectors = []
    failed_files = []

    for file_url in files:
        try:
            # Download the file using AWS SDK
            file_path = download_file_from_s3(file_url)

            # Extract text
            text = extract_text_from_file(file_path)

            # Chunk text
            chunks = chunk_text(text, max_chunk_size=MAX_CHUNK_SIZE)

            # Generate embeddings
            embeddings = model.encode(chunks)

            # Prepare vectors and payloads
            for chunk, embedding in zip(chunks, embeddings):
                vector_id = str(uuid.uuid4())
                all_vectors.append(
                    {
                        'id': vector_id,
                        'vector': embedding.tolist(),
                        'payload': {
                            'chunk': chunk,
                            'datasetId': datasetId
                        }
                    }
                )

            # Clean up temporary file
            os.remove(file_path)

        except Exception as e:
            error_message = f"Error processing {file_url}: {e}"
            print(error_message)
            failed_files.append({'file_url': file_url, 'error': str(e)})
            continue  # Skip this file and proceed to the next

    # Insert vectors into Qdrant
    if all_vectors:
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            wait=True,
            points=all_vectors
        )

    response = {
        "message": "Files successfully ingested and stored in the vector database",
        "ingestedFiles": len(files) - len(failed_files),
        "datasetId": datasetId
    }

    if failed_files:
        response['failedFiles'] = failed_files

    return response

async def delete_dataset(datasetId: str):
    if not datasetId:
        raise ValueError("datasetId is required")

    # Create a filter to match the datasetId
    delete_filter = Filter(
        must=[
            FieldCondition(
                key="datasetId",
                match=MatchValue(value=datasetId)
            )
        ]
    )

    # Perform deletion
    qdrant_client.delete(
        collection_name=QDRANT_COLLECTION_NAME,
        points_selector=delete_filter,
        wait=True
    )

    return {
        "message": f"All data associated with datasetId '{datasetId}' has been deleted."
    }

# New helper function to get all datasetIds
async def get_dataset_ids():
    # Retrieve all unique datasetIds from the collection
    response = qdrant_client.scroll(
        collection_name=QDRANT_COLLECTION_NAME,
        scroll_filter=None,
        with_payload=True,
        limit=1000
    )
    dataset_ids = set()
    for point in response[0]:
        dataset_id = point.payload.get("datasetId")
        if dataset_id:
            dataset_ids.add(dataset_id)
    return list(dataset_ids)

# New helper function to get chunks by datasetId
async def get_chunks_by_dataset(datasetId: str):
    # Create a filter to match the datasetId
    query_filter = Filter(
        must=[
            FieldCondition(
                key="datasetId",
                match=MatchValue(value=datasetId)
            )
        ]
    )
    # Scroll through all points with the given datasetId
    all_chunks = []
    scroll_id = None
    while True:
        response = qdrant_client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter=query_filter,
            with_payload=True,
            limit=100,
            offset=scroll_id
        )
        points, next_scroll_id = response
        for point in points:
            chunk = point.payload.get("chunk", "")
            all_chunks.append(chunk)
        if not next_scroll_id:
            break
        scroll_id = next_scroll_id
    return all_chunks
