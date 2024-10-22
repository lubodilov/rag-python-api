# app/main.py

from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="RAG Python API", version="1.0.0")

app.include_router(router)
