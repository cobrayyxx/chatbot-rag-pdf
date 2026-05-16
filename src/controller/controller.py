from fastapi import FastAPI, File, UploadFile, HTTPException
from pypdf import PdfReader
from service.preprocess_pdf import PreprocessPDF
from service.embedding import Embedding
from database.qdrant import QdrantSetup
from model.model import SearchRequest
from service.ollama_service import OllamaService

import uvicorn
import io
import requests
import os

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
embedding = Embedding()
ollama_service = OllamaService()
qdrant_host = os.getenv("QDRANT_HOST", "http://localhost:6333")


@app.post("/extract-pdf")
async def upload_file(file: UploadFile = File(...)):

    # validate pdf file
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload a PDF file."
        )
    
    try:
        # Read the PDF file
        contents = await file.read()  # Read the file content into memory
        # Process the PDF file using the PreprocessPDF class
        pdf_processor = PreprocessPDF(contents)
        extracted_text, num_pages = pdf_processor.extract_pdf()
        # Save extracted_text into embedding
        embedding_result, chunks = embedding.get_embedding(extracted_text)
        qdrant = QdrantSetup(collection_name="pdf_embeddings_text", vector_size=embedding_result.shape[1], url=qdrant_host)
        qdrant.create_collection()
        points = []
        for i, vector in enumerate(embedding_result):
            points.append(
                {
                    "id": i,
                    "vector": vector.tolist(),
                    "payload": {"title": file.filename, "text": chunks[i]}
                }
            )
        qdrant.upsert_points(points=points)

        return {"message": "File uploaded successfully", "file_text": extracted_text, "num_pages": num_pages}
    except Exception as e:
        raise HTTPException(    
            status_code=500, 
            detail=f"An error occurred while processing the PDF file: {str(e)}"
        )

@app.post("/search")
async def search(request: SearchRequest):
    query_embedding, _ = embedding.get_embedding(request.query)
    qdrant = QdrantSetup(collection_name="pdf_embeddings_text", vector_size=query_embedding.shape[1], url=qdrant_host)
    search_results = qdrant.client.query_points(
        collection_name=qdrant.collection_name,
        query=query_embedding[0].tolist(),
        limit=5
    )

    prompt = ollama_service.create_prompt(request.query, search_results)
    response = ollama_service.generate_response(prompt)
    return {"response": response, "query": request.query, "results": search_results}


if __name__ == "__main__":
    uvicorn.run(
        "controller:app",  # Replace "main" with your actual file name if it differs
        host="127.0.0.1",
        port=8000,
        reload=True,  # Auto-restarts server when code changes
    )

