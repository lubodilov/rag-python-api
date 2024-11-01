# app/utils.py

import os
import boto3
import requests
from tika import parser
import nltk
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from app.config import TEMP_DIR, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
import pandas as pd
from docx import Document
import json

# Initialize NLTK
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name=AWS_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def download_file_from_s3(s3_url):
    """
    Download a file from a private S3 bucket using AWS SDK.
    """
    try:
        # Extract bucket name and file key from the S3 URL
        bucket_name, key = parse_s3_url(s3_url)
        
        # Define the local path where the file will be saved
        local_file_path = os.path.join(TEMP_DIR, os.path.basename(key))
        
        # Download the file from S3 to the local path
        s3_client.download_file(bucket_name, key, local_file_path)
        
        return local_file_path
    except NoCredentialsError:
        raise Exception("AWS credentials not found.")
    except PartialCredentialsError:
        raise Exception("Incomplete AWS credentials.")
    except Exception as e:
        raise Exception(f"Error downloading file from S3: {e}")

def parse_s3_url(s3_url):
    """
    Parse the S3 URL to extract the bucket name and key.
    """
    if s3_url.startswith("s3://"):
        # Remove 's3://' from the URL and split into bucket name and key
        s3_url_parts = s3_url.replace("s3://", "").split("/", 1)
    elif s3_url.startswith("https://") or s3_url.startswith("http://"):
        # Parse virtual-hosted–style URL
        # Example: https://bucket-name.s3.region.amazonaws.com/key
        import re
        match = re.match(r'https?://(.+?)\.s3[.-](?:[a-z0-9-]+)\.amazonaws\.com/(.+)', s3_url)
        if match:
            bucket_name, key = match.groups()
        else:
            raise ValueError("Invalid S3 URL format")
    else:
        raise ValueError("Invalid S3 URL. Expected URL starting with 's3://' or 'https://'")

    if len(s3_url_parts) != 2:
        raise ValueError("Invalid S3 URL format")
    
    return s3_url_parts[0], s3_url_parts[1]

def extract_text_from_file(file_path):
    # Determine file type based on the file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    text = None

    if file_extension == '.pdf':
        # Existing PDF extraction code
        parsed = parser.from_file(file_path)
        text = parsed.get('content')
    elif file_extension == '.txt':
        # TXT file handling
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_extension in ['.doc', '.docx']:
        # DOC and DOCX file handling
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    elif file_extension == '.csv':
        # CSV file handling
        df = pd.read_csv(file_path)
        text = df.to_string()
    elif file_extension == '.json':
        # JSON file handling
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = json.dumps(data)
    else:
        # Fallback to Tika for other formats
        parsed = parser.from_file(file_path)
        text = parsed.get('content')

    if text:
        return text.strip()
    else:
        raise Exception(f"No text could be extracted from {file_path}")

def chunk_text(text, max_chunk_size=500):
    """
    Chunk text into smaller parts for vector embedding.
    """
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
