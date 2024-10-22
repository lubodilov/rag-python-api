# app/utils.py

import requests
import os
from tika import parser
import nltk

from app.config import TEMP_DIR

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('punkt_pickle', quiet=True)  # Added this line to fix the missing resource

def download_file_from_url(file_url):
    local_filename = file_url.split('/')[-1]
    local_file_path = os.path.join(TEMP_DIR, local_filename)

    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as f:
            f.write(response.content)
        return local_file_path
    else:
        raise Exception(f"Failed to download file from {file_url}")

def extract_text_from_file(file_path):
    parsed = parser.from_file(file_path)
    text = parsed.get('content')
    if text:
        return text.strip()
    else:
        raise Exception(f"No text could be extracted from {file_path}")

def chunk_text(text, max_chunk_size=500):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += ' ' + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
