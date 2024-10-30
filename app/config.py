# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file, if it exists
load_dotenv()

# Qdrant Configuration
QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', '6333'))
QDRANT_COLLECTION_NAME = 'documents'

# Embedding Model Configuration
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'all-MiniLM-L6-v2')

# Other Configurations
MAX_CHUNK_SIZE = int(os.getenv('MAX_CHUNK_SIZE', '500'))
TEMP_DIR = os.getenv('TEMP_DIR', '/tmp')

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')  # Replace with your region

# Logging Configuration (Optional)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
