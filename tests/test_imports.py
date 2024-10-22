# test_imports.py
try:
    import fastapi
    import uvicorn
    import requests
    import pdfplumber
    import nltk
    import sentence_transformers
    import qdrant_client
    from tika import parser
    from dotenv import load_dotenv

    print("All libraries imported successfully!")
except ImportError as e:
    print(f"ImportError: {e}")
