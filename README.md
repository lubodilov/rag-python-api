## **Project Overview**

The RAG (Retrieval-Augmented Generation) Python API is designed to facilitate the ingestion and retrieval of document data using a vector database. The API allows users to ingest documents from AWS S3, process them using embeddings, store them in a vector database, and retrieve the most relevant chunks based on a given prompt. It also includes a basic UI for displaying datasets and chunks.

**Note:** The API is already deployed and accessible at:

```
http://
```

---

## **Features**

- **Ingest Documents**: Upload documents from S3 (PDF, TXT, DOC, DOCX, CSV, JSON) and store them in the vector database with associated metadata.
- **Retrieve Chunks**: Retrieve the top 3 most similar chunks based on a prompt and dataset ID.
- **Delete Datasets**: Remove all data associated with a specific dataset ID.
- **Basic UI**: View datasets and their chunks through a simple web interface.
- **Supports Multiple File Formats**: Including PDF, TXT, DOC, DOCX, CSV, and JSON.
- **Open Source Tools**: Built using open-source libraries and tools, avoiding any proprietary APIs.

---

## **Tools and Technologies**

- **Programming Language**: Python 3.8+
- **Web Framework**: FastAPI
- **Vector Database**: **Qdrant** – an open-source vector database for storing embeddings.
- **Document Processing**:
  - **Apache Tika**: For extracting text from various document formats.
  - **pdfplumber**: For extracting text from PDFs.
  - **python-docx**: For extracting text from DOC and DOCX files.
  - **pandas**: For reading CSV files.
  - **json**: For handling JSON files.
  - **NLTK (Natural Language Toolkit)**: For text processing, including tokenization and text normalization.
- **Embedding Model**: **SentenceTransformers** (`all-MiniLM-L6-v2`) – a pre-trained model for generating text embeddings.
- **AWS SDK**: **Boto3** – for downloading files from AWS S3.
- **Web Server**: **Gunicorn**
- **Reverse Proxy**: **Nginx**
- **Templating Engine**: **Jinja2**
- **Styling**: **Bootstrap 4**

---

## **Installation and Setup**

### **Prerequisites**

- **Python 3.8+**
- **pip** (Python package installer)
- **Git**
- **Java Runtime Environment**: Required for Apache Tika.
- **AWS Account**: For accessing S3 buckets.
- **AWS Credentials**: Configured on your local machine.

### **Setting Up the Project Locally**

Follow the steps below to set up the project on your local machine.

#### **1. Clone the Repository**

Open a terminal and clone the GitHub repository:

```bash
git clone https://github.com/yourusername/rag-python-api.git
cd rag-python-api
```

#### **2. Create a Virtual Environment**

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

#### **3. Install Dependencies**

Update pip and install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### **4. Install System Dependencies**

For Apache Tika and other processing tools, you need Java and other system packages.

**On Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install default-jre poppler-utils
```

**On macOS:**

```bash
brew update
brew install java poppler
```

#### **5. Set Up Environment Variables**

Create a `.env` file in the project root directory to store environment variables.

```bash
touch .env
```

Add the following variables to the `.env` file:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=your_aws_region

QDRANT_HOST=localhost
QDRANT_PORT=6333
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
MAX_CHUNK_SIZE=500
TEMP_DIR=/tmp
LOG_LEVEL=INFO
```

**Note:** Replace the placeholders with your actual AWS credentials and desired settings.

#### **6. Run Qdrant Vector Database Locally**

You can run Qdrant locally using Docker.

**Install Docker if not already installed.**

**Run Qdrant using Docker:**

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Alternatively, you can install Qdrant natively. Refer to Qdrant's [documentation](https://qdrant.tech/documentation/) for installation instructions.

#### **7. Start the FastAPI Application**

Run the application using Uvicorn.

```bash
uvicorn app.main:app --reload
```

This will start the server at `http://localhost:8000/`.

#### **8. Access the API and UI**

- **API Endpoints:** You can access the API endpoints at `http://localhost:8000/ingest`, `/retrieve`, and `/delete`.
- **Basic UI:** Open your web browser and navigate to `http://localhost:8000/` to access the basic UI.

---

## **API Endpoints**

### **POST /ingest**

- **Description**: Ingests files from S3 URLs, processes them, and stores the chunks in the vector database with the provided dataset ID.
- **Request Body**:

    ```json
    {
        "files": ["s3://your-bucket-name/file1.pdf", "s3://your-bucket-name/file2.txt"],
        "datasetId": "your_dataset_id"
    }
    ```

- **Response**:

    ```json
    {
        "message": "Files successfully ingested and stored in the vector database",
        "ingestedFiles": 2,
        "datasetId": "your_dataset_id"
    }
    ```

### **POST /retrieve**

- **Description**: Retrieves the top 3 most similar chunks from the database, filtered by the dataset ID, based on the provided prompt.
- **Request Body**:

    ```json
    {
        "prompt": "Your query here",
        "datasetId": "your_dataset_id"
    }
    ```

- **Response**:

    ```json
    {
        "prompt": "Your query here",
        "datasetId": "your_dataset_id",
        "results": [
            {"chunk": "First similar chunk..."},
            {"chunk": "Second similar chunk..."},
            {"chunk": "Third similar chunk..."}
        ]
    }
    ```

### **POST /delete**

- **Description**: Deletes all data associated with the provided dataset ID from the vector database.
- **Request Body**:

    ```json
    {
        "datasetId": "your_dataset_id"
    }
    ```

- **Response**:

    ```json
    {
        "message": "All data associated with datasetId 'your_dataset_id' has been deleted."
    }
    ```

---

## **Basic UI**

- **Access**: Navigate to `http://localhost:8000/` in your web browser.
- **Features**:
    - **Datasets List**: View all available datasets.
    - **Dataset Details**: Click on a dataset to view all associated chunks.
    - **Styled Interface**: Basic styling using Bootstrap for improved user experience.

---

## **Testing the API**

To fully test the API, follow the steps below using cURL commands or any HTTP client like Postman.

---

## **Examples**

### **Full API Testing Example**

#### **Step 1: Ingest Files**

Use the `/ingest` endpoint to ingest files from your S3 bucket.

**Request:**

```bash
curl -X POST http://localhost:8000/ingest \
-H "Content-Type: application/json" \
-d '{
    "files": [
        "s3://your-bucket-name/file1.pdf",
        "s3://your-bucket-name/file2.txt"
    ],
    "datasetId": "dataset123"
}'
```

**Response:**

```json
{
    "message": "Files successfully ingested and stored in the vector database",
    "ingestedFiles": 2,
    "datasetId": "dataset123"
}
```

#### **Step 2: Retrieve Chunks**

Use the `/retrieve` endpoint to retrieve the top 3 most similar chunks based on a prompt.

**Request:**

```bash
curl -X POST http://localhost:8000/retrieve \
-H "Content-Type: application/json" \
-d '{
    "prompt": "Tell me about the features",
    "datasetId": "dataset123"
}'
```

**Response:**

```json
{
    "prompt": "Tell me about the features",
    "datasetId": "dataset123",
    "results": [
        {"chunk": "First similar chunk..."},
        {"chunk": "Second similar chunk..."},
        {"chunk": "Third similar chunk..."}
    ]
}
```

#### **Step 3: Delete Dataset**

Use the `/delete` endpoint to delete all data associated with the dataset ID.

**Request:**

```bash
curl -X POST http://localhost:8000/delete \
-H "Content-Type: application/json" \
-d '{
    "datasetId": "dataset123"
}'
```

**Response:**

```json
{
    "message": "All data associated with datasetId 'dataset123' has been deleted."
}
```

#### **Step 4: Access the UI**

Open your web browser and navigate to:

```
http://
```

- **View Datasets**: You should see a list of datasets (if any).
- **View Chunks**: Click on a dataset to view its chunks.

---

## **Project Structure**

```
rag-python-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── config.py
│   ├── utils.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ingest_service.py
│   │   └── retrieve_service.py
├── templates/
│   ├── index.html
│   └── dataset.html
├── static/
│   └── styles.css
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```

---

## **Dependencies**

- **Python Packages**:
    - **fastapi**: Web framework for building APIs.
    - **uvicorn[standard]**: ASGI server for running FastAPI applications.
    - **requests**: For making HTTP requests.
    - **pdfplumber**: For extracting text from PDFs.
    - **tika**: Apache Tika for text extraction.
    - **nltk**: Natural Language Toolkit for text processing.
    - **sentence-transformers**: For generating embeddings using models like `all-MiniLM-L6-v2`.
    - **qdrant-client**: Client library for interacting with Qdrant vector database.
    - **python-dotenv**: For loading environment variables from a `.env` file.
    - **numpy**: For numerical computations.
    - **boto3**: AWS SDK for Python, used for accessing S3.
    - **jinja2**: Templating engine for rendering HTML pages.
    - **aiofiles**: For asynchronous file operations.
    - **python-docx**: For extracting text from DOC and DOCX files.
    - **pandas**: For reading CSV files.
- **System Packages**:
    - **Java Runtime Environment**: Required for Apache Tika.
    - **poppler-utils**: Required for PDF processing (e.g., `pdftotext`).
- **Other Tools**:
    - **Qdrant**: Open-source vector database for storing embeddings.
    - **SentenceTransformers Model**: `all-MiniLM-L6-v2`, an open-source embedding model.
    - **Bootstrap**: Front-end framework for styling the UI.
