# import os
# from fastapi import FastAPI, HTTPException, Depends, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Optional, Dict, Any
# import asyncio
# import logging
# from contextlib import asynccontextmanager

# from database import SessionLocal, Document
# from rag import rag_service
# from vector_store import qdrant_service

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Initialize FastAPI app with lifespan to properly manage resources
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     logger.info("Starting up RAG Chatbot API...")
#     yield
#     # Shutdown
#     logger.info("Shutting down RAG Chatbot API...")

# app = FastAPI(
#     title="RAG Chatbot API",
#     description="API for RAG chatbot integrated with Physical AI book",
#     version="1.0.0",
#     lifespan=lifespan
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, replace with specific origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatMessage(BaseModel):
#     message: str
#     chat_history: Optional[List[Dict[str, str]]] = []
#     selected_text: Optional[str] = None

# class ChatResponse(BaseModel):
#     response: str
#     sources: List[Dict[str, Any]]
#     tokens_used: int

# class DocumentIndexRequest(BaseModel):
#     content: str
#     doc_id: str
#     doc_title: str
#     doc_section: Optional[str] = None

# class DocumentIndexResponse(BaseModel):
#     success: bool
#     chunks_processed: int

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# async def root():
#     return {"message": "RAG Chatbot API is running!"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}

# @app.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(chat_message: ChatMessage):
#     """
#     Main chat endpoint that handles user queries and returns RAG-enhanced responses
#     """
#     try:
#         response = await rag_service.query(
#             query=chat_message.message,
#             selected_context=chat_message.selected_text
#         )

#         return ChatResponse(
#             response=response.response,
#             sources=response.sources,
#             tokens_used=response.tokens_used
#         )
#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/index-document", response_model=DocumentIndexResponse)
# async def index_document_endpoint(request: DocumentIndexRequest):
#     """
#     Endpoint to index a document for RAG retrieval
#     """
#     try:
#         # In a real implementation, we would:
#         # 1. Chunk the document content
#         # 2. Generate embeddings for each chunk
#         # 3. Store chunks in the database
#         # 4. Store embeddings in Qdrant

#         # For now, implementing basic functionality
#         # Chunk the document into smaller pieces
#         chunks = chunk_document(request.content)

#         # Store document metadata in database
#         db = SessionLocal()
#         try:
#             # Create document record
#             doc = Document(
#                 doc_id=request.doc_id,
#                 title=request.doc_title,
#                 content=request.content,
#                 section=request.doc_section or "unknown",
#                 is_indexed=True
#             )
#             db.add(doc)
#             db.commit()
#         finally:
#             db.close()

#         # Store embeddings in Qdrant
#         if chunks:
#             doc_ids = [request.doc_id] * len(chunks)
#             metadata_list = [{"section": request.doc_section, "title": request.doc_title} for _ in chunks]
#             vector_ids = await qdrant_service.store_embeddings(chunks, doc_ids, metadata_list)

#             # Update document record with embedding reference
#             db = SessionLocal()
#             try:
#                 doc = db.query(Document).filter(Document.doc_id == request.doc_id).first()
#                 if doc:
#                     doc.embedding_vector_id = ",".join(vector_ids)
#                     db.commit()
#             finally:
#                 db.close()

#         return DocumentIndexResponse(
#             success=True,
#             chunks_processed=len(chunks)
#         )
#     except Exception as e:
#         logger.error(f"Error in index document endpoint: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/docs")
# async def get_documents():
#     """
#     Get list of indexed documents
#     """
#     try:
#         db = SessionLocal()
#         try:
#             documents = db.query(Document).all()
#             return [
#                 {
#                     "doc_id": doc.doc_id,
#                     "title": doc.title,
#                     "section": doc.section,
#                     "created_at": doc.created_at.isoformat(),
#                     "is_indexed": doc.is_indexed
#                 }
#                 for doc in documents
#             ]
#         finally:
#             db.close()
#     except Exception as e:
#         logger.error(f"Error getting documents: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# def chunk_document(content: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
#     """
#     Simple function to chunk a document into smaller pieces
#     """
#     if not content:
#         return []

#     chunks = []
#     start = 0
#     content_length = len(content)

#     while start < content_length:
#         end = start + chunk_size

#         # Ensure we don't go beyond the content
#         if end > content_length:
#             end = content_length

#         chunk = content[start:end]
#         chunks.append(chunk)

#         # Move start position with overlap
#         start = end - overlap

#         # If the last chunk is very small and it's the last one, merge it with the previous chunk
#         if len(chunk) < chunk_size and end >= content_length and len(chunks) > 1:
#             last_chunk = chunks.pop()
#             combined_chunk = chunks.pop() + " " + last_chunk
#             chunks.append(combined_chunk)
#             break

#     return chunks

# @app.post("/index-book")
# async def index_book():
#     """
#     Index the entire book from the frontend documentation
#     This would be a more complex endpoint that processes all docs
#     """
#     try:
#         # This is a simplified implementation
#         # In a real implementation, this would read from the frontend docs
#         # and index all content

#         # For now, returning a placeholder
#         return {"message": "Book indexing would occur here", "status": "not_implemented_yet"}
#     except Exception as e:
#         logger.error(f"Error in index book endpoint: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


import os
import logging
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import SessionLocal, Document
from rag import rag_service
from vector_store import qdrant_service

# ===================== LOGGING =====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== APP LIFESPAN =====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting RAG Chatbot API for Physical AI & Humanoid Robotics Book...")

    # Verify services are available
    if not qdrant_service.connected:
        logger.warning("⚠️ Qdrant vector database is not connected. RAG functionality will be limited.")
    else:
        logger.info("✅ Successfully connected to Qdrant vector database")

    yield

    logger.info("🛑 Shutting down RAG Chatbot API...")

# ===================== FASTAPI APP =====================
app = FastAPI(
    title="RAG Chatbot API for Physical AI & Humanoid Robotics Book",
    description="API for RAG chatbot that answers questions based on the Physical AI & Humanoid Robotics book content",
    version="1.0.0",
    lifespan=lifespan
)

# ===================== CORS =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== SCHEMAS =====================
class ChatMessage(BaseModel):
    message: str
    chat_history: Optional[List[Dict[str, str]]] = []
    selected_text: Optional[str] = None


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

# ===================== ROUTES =====================
@app.get("/")
async def root():
    return {
        "message": "RAG Chatbot API for Physical AI & Humanoid Robotics Book is running!",
        "status": "ready",
        "qdrant_connected": qdrant_service.connected,
        "instructions": "Send POST requests to /chat to ask questions about the book"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "qdrant_connected": qdrant_service.connected,
        "services": {
            "qdrant": "connected" if qdrant_service.connected else "disconnected",
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatMessage):
    """
    Main chat endpoint that processes user queries against the book content
    """
    try:
        logger.info(f"Received query: {payload.message[:100]}{'...' if len(payload.message) > 100 else ''}")

        # Pass the query to the RAG service
        result = await rag_service.query(
            query=payload.message,
            selected_context=payload.selected_text
        )

        logger.info(f"Generated response with {len(result.sources)} sources")

        return ChatResponse(
            response=result.response,
            sources=result.sources,
            tokens_used=result.tokens_used
        )

    except Exception as e:
        logger.exception("Chat endpoint failed")
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )


@app.post("/index-document", response_model=DocumentIndexResponse)
async def index_document_endpoint(request: DocumentIndexRequest):
    """
    Endpoint to index a document for RAG retrieval
    """
    try:
        logger.info(f"Indexing document: {request.doc_title}")

        chunks = chunk_document(request.content)

        # Save document metadata to database
        db = SessionLocal()
        try:
            # Check if document already exists
            existing_doc = db.query(Document).filter(Document.doc_id == request.doc_id).first()

            if existing_doc:
                # Update existing document
                existing_doc.title = request.doc_title
                existing_doc.content = request.content
                existing_doc.section = request.doc_section or "unknown"
                existing_doc.is_indexed = True
            else:
                # Create new document
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

        # Store embeddings in Qdrant if service is connected
        if chunks and qdrant_service.connected:
            doc_ids = [request.doc_id] * len(chunks)
            metadata_list = [
                {"section": request.doc_section or "unknown", "title": request.doc_title}
                for _ in chunks
            ]

            vector_ids = await qdrant_service.store_embeddings(
                chunks,
                doc_ids,
                metadata_list
            )

            # Update document record with embedding reference
            db = SessionLocal()
            try:
                doc = db.query(Document).filter(Document.doc_id == request.doc_id).first()
                if doc:
                    doc.embedding_vector_id = ",".join(vector_ids)
                    db.commit()
            finally:
                db.close()

            logger.info(f"Indexed {len(chunks)} chunks with {len(vector_ids)} vectors")
        else:
            logger.warning(f"Skipped vector indexing for {request.doc_title} - Qdrant not connected or no chunks")
            vector_ids = []

        return DocumentIndexResponse(
            success=True,
            chunks_processed=len(chunks)
        )

    except Exception as e:
        logger.exception("Index document failed")
        raise HTTPException(
            status_code=500,
            detail=f"Document indexing failed: {str(e)}"
        )


@app.get("/docs")
async def get_documents():
    """
    Get list of indexed documents
    """
    try:
        db = SessionLocal()
        try:
            docs = db.query(Document).all()
            return [
                {
                    "doc_id": d.doc_id,
                    "title": d.title,
                    "section": d.section,
                    "created_at": d.created_at.isoformat(),
                    "updated_at": d.updated_at.isoformat() if d.updated_at else None,
                    "is_indexed": d.is_indexed,
                    "has_embeddings": bool(d.embedding_vector_id)
                }
                for d in docs
            ]
        finally:
            db.close()

    except Exception as e:
        logger.exception("Fetching documents failed")
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch documents: {str(e)}"
        )


@app.post("/index-book")
async def index_book():
    """
    Index the entire book from the frontend documentation
    """
    try:
        logger.info("Starting book indexing process...")

        # This would be a more complex endpoint that processes all docs
        # For now, returning a placeholder with instructions
        return {
            "status": "manual_process_required",
            "message": "Book indexing requires running the setup_book_index.py script",
            "instructions": [
                "1. Make sure you have book content in frontend/docs/",
                "2. Run: python setup_book_index.py",
                "3. Then you can use the chat endpoint"
            ],
            "qdrant_connected": qdrant_service.connected
        }
    except Exception as e:
        logger.error(f"Error in index book endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== UTIL =====================
def chunk_document(
    content: str,
    chunk_size: int = 1000,
    overlap: int = 100
) -> List[str]:
    """
    Split content into overlapping chunks for better context retention
    """
    if not content:
        return []

    chunks = []
    start = 0
    length = len(content)

    # Prevent infinite loops and memory issues
    max_chunks = len(content) // 100  # Reasonable upper limit
    chunk_count = 0

    while start < length and chunk_count < max_chunks:
        end = min(start + chunk_size, length)
        chunk = content[start:end]

        # Only add chunks that have meaningful content
        if chunk.strip():
            chunks.append(chunk)
            chunk_count += 1

        # Move start position with overlap
        start = end - overlap

        # Prevent infinite loops
        if start <= 0:  # Safety check to prevent infinite loops
            start += chunk_size

        # Handle the case where the remaining content is smaller than overlap
        if start >= length:
            break

    return chunks
