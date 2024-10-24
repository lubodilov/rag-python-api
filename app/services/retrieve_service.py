# app/services/retrieve_service.py

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from app.config import (
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
)

# Initialize the embedding model
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Initialize Qdrant client
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

async def retrieve_chunks(prompt: str, datasetId: str):
    if not prompt or not datasetId:
        raise ValueError("Prompt and datasetId are required")

    # Generate embedding for the prompt
    query_vector = model.encode(prompt).tolist()

    # Create a filter to match the datasetId
    query_filter = Filter(
        must=[
            FieldCondition(
                key="datasetId",
                match=MatchValue(value=datasetId)
            )
        ]
    )

    # Perform search in Qdrant
    search_result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        query_filter=query_filter,
        limit=3,
        with_payload=True
    )

    # Extract the chunks from the search results
    results = []
    for hit in search_result:
        payload = hit.payload
        chunk_text = payload.get('chunk', '')
        results.append({
            "chunk": chunk_text
        })

    return results
