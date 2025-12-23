import os
import logging
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables locally (Render will use actual env vars)
from dotenv import load_dotenv
load_dotenv()

from database import SessionLocal, Document
from rag import rag_service
from vector_store import qdrant_service
from translation_service import translation_service

# ===================== LOGGING =====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== APP LIFESPAN =====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting RAG Chatbot API...")

    if not qdrant_service.connected:
        logger.warning("⚠️ Qdrant vector database is not connected. RAG functionality will be limited.")
    else:
        logger.info("✅ Successfully connected to Qdrant vector database")

    yield
    logger.info("🛑 Shutting down RAG Chatbot API...")

# ===================== FASTAPI APP =====================
app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0",
    lifespan=lifespan
)

# ===================== CORS =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== SCHEMAS =====================
class ChatMessage(BaseModel):
    message: str
    chat_history: Optional[List[Dict[str, str]]] = []
    selected_text: Optional[str] = None
    target_language: Optional[str] = "en"

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    tokens_used: int

class DocumentIndexRequest(BaseModel):
    content: str
    doc_id: str
    doc_title: str
    doc_section: Optional[str] = None

class DocumentIndexResponse(BaseModel):
    success: bool
    chunks_processed: int

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "ur"

class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str
    tokens_used: int

# ===================== ROUTES =====================
@app.get("/")
async def root():
    return {
        "message": "RAG Chatbot API is running!",
        "status": "ready",
        "qdrant_connected": qdrant_service.connected,
        "instructions": "Send POST requests to /chat"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "qdrant_connected": qdrant_service.connected
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatMessage):
    try:
        result = await rag_service.query(
            query=payload.message,
            selected_context=payload.selected_text,
            target_language=payload.target_language
        )
        return ChatResponse(
            response=result.response,
            sources=result.sources,
            tokens_used=result.tokens_used
        )
    except Exception as e:
        logger.exception("Chat endpoint failed")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.post("/translate", response_model=TranslationResponse)
async def translate_endpoint(request: TranslationRequest):
    try:
        result = await translation_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        return result
    except Exception as e:
        logger.exception("Translation failed")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/index-document", response_model=DocumentIndexResponse)
async def index_document_endpoint(request: DocumentIndexRequest):
    try:
        chunks = chunk_document(request.content)
        db = SessionLocal()
        try:
            existing_doc = db.query(Document).filter(Document.doc_id == request.doc_id).first()
            if existing_doc:
                existing_doc.title = request.doc_title
                existing_doc.content = request.content
                existing_doc.section = request.doc_section or "unknown"
                existing_doc.is_indexed = True
            else:
                document = Document(
                    doc_id=request.doc_id,
                    title=request.doc_title,
                    content=request.content,
                    section=request.doc_section or "unknown",
                    is_indexed=True
                )
                db.add(document)
            db.commit()
        finally:
            db.close()

        if chunks and qdrant_service.connected:
            doc_ids = [request.doc_id] * len(chunks)
            metadata_list = [{"section": request.doc_section or "unknown", "title": request.doc_title} for _ in chunks]
            vector_ids = await qdrant_service.store_embeddings(chunks, doc_ids, metadata_list)
        else:
            vector_ids = []

        return DocumentIndexResponse(success=True, chunks_processed=len(chunks))
    except Exception as e:
        logger.exception("Document indexing failed")
        raise HTTPException(status_code=500, detail=f"Document indexing failed: {str(e)}")

# ===================== UTIL =====================
def chunk_document(content: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    if not content:
        return []

    chunks = []
    start = 0
    length = len(content)
    max_chunks = len(content) // 100
    chunk_count = 0

    while start < length and chunk_count < max_chunks:
        end = min(start + chunk_size, length)
        chunk = content[start:end]
        if chunk.strip():
            chunks.append(chunk)
            chunk_count += 1
        start = end - overlap
        if start <= 0:
            start += chunk_size
        if start >= length:
            break
    return chunks

# ===================== RUN ON RENDER =====================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
