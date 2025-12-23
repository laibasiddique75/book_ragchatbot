import asyncio
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from vector_store import qdrant_service
from openrouter import openrouter_service
from database import SessionLocal, Document
from translation_service import translation_service
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGRequest(BaseModel):
    query: str
    context: Optional[str] = None  # Optional context from selected text
    max_sources: Optional[int] = 5
    temperature: Optional[float] = 0.7

class RAGResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    tokens_used: int

class RAGService:
    def __init__(self):
        self.max_sources = int(os.getenv("MAX_SOURCES", "5"))
        self.max_context_length = int(os.getenv("MAX_CONTEXT_LENGTH", "4096"))  # Increased for better context

    async def retrieve_context(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from the vector store based on the query
        """
        if limit is None:
            limit = self.max_sources

        try:
            # Check if qdrant service is connected before attempting to search
            if not qdrant_service.connected:
                logger.warning("Qdrant not connected. Returning empty context.")
                return []

            # Search for similar documents in the vector store
            search_results = await qdrant_service.search_similar(query, limit=limit)

            logger.info(f"Retrieved {len(search_results)} context documents")

            # Sort results by score to prioritize most relevant content
            search_results.sort(key=lambda x: x.get('score', 0), reverse=True)
            return search_results

        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []  # Return empty context instead of raising error

    async def generate_response(self, query: str, context_docs: List[Dict[str, Any]],
                                selected_context: Optional[str] = None) -> RAGResponse:
        """
        Generate a response using the retrieved context and LLM
        """
        try:
            # Build the context for the LLM ensuring book content is prioritized
            context_str = ""

            # Calculate total length of retrieved context
            total_context_length = 0
            context_parts = []

            if selected_context:
                # If specific text was selected, prioritize it
                context_parts.append(f"EXPLICITLY SELECTED TEXT FROM BOOK:\n{selected_context}\n")
                total_context_length += len(selected_context)

            # Add retrieved documents from vector store
            for doc in context_docs:
                doc_text = doc['text'].strip()
                if doc_text:  # Only add non-empty documents
                    new_part = f"RELEVANT BOOK CONTENT:\n{doc_text}\n\n"
                    if total_context_length + len(new_part) <= self.max_context_length:
                        context_parts.append(new_part)
                        total_context_length += len(new_part)
                    else:
                        # If adding this part would exceed the limit, truncate it
                        remaining_space = self.max_context_length - total_context_length
                        if remaining_space > 0:
                            truncated_doc = doc_text[:remaining_space]
                            context_parts.append(f"RELEVANT BOOK CONTENT:\n{truncated_doc}\n\n")
                        break

            context_str = "".join(context_parts)

            # If no context was found, inform the user
            if not context_str.strip():
                context_str = "NO RELEVANT CONTENT FOUND IN THE BOOK FOR THIS QUESTION."

            # Prepare messages for the language model with strict instructions to use book content only
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an expert assistant for the 'Physical AI & Humanoid Robotics' book. "
                        "ANSWER ONLY BASED ON THE PROVIDED BOOK CONTENT. "
                        "If the provided context doesn't contain relevant information, explicitly state that the information is not available in the book. "
                        "NEVER provide information that is not contained in the provided context. "
                        "Cite specific sections and content from the book when answering. "
                        "Be precise and accurate based solely on the book content provided in the context."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"BOOK CONTENT CONTEXT:\n{context_str}\n\n"
                        f"USER QUESTION: {query}\n\n"
                        "Please provide a detailed answer based EXCLUSIVELY on the book content provided above. "
                        "If the book content does not contain the information needed to answer this question, "
                        "clearly state that the information is not available in the book. "
                        "Do not make up information or provide external knowledge."
                    )
                }
            ]

            # Get response from OpenRouter (as fallback to Gemini)
            completion_response = await openrouter_service.get_chat_completion(
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent, fact-based responses
                max_tokens=1024
            )

            logger.info(f"Generated response with {completion_response.tokens_used} tokens")
            return RAGResponse(
                response=completion_response.response,
                sources=context_docs,
                tokens_used=completion_response.tokens_used
            )

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # If there's an error generating the response, return a fallback response based on the context
            if context_docs:
                # If we have context but couldn't generate a response, return the most relevant context
                top_doc = context_docs[0] if context_docs else None
                fallback_response = f"Based on the book content, here's relevant information to your question '{query}':\n\n{top_doc['text'] if top_doc else 'No specific content found.'}\n\nNote: There was an issue processing your request with the AI model, so this is a direct extract from the book."
                return RAGResponse(
                    response=fallback_response,
                    sources=context_docs,
                    tokens_used=0
                )
            else:
                return RAGResponse(
                    response=f"Could not find relevant information in the book for your question: '{query}'. There was also an issue processing your request with the AI model.",
                    sources=[],
                    tokens_used=0
                )

    async def query(self, query: str, selected_context: Optional[str] = None, target_language: Optional[str] = "en") -> RAGResponse:
        """
        Main RAG query method - retrieves context and generates response
        """
        try:
            context_docs = []

            if selected_context:
                # If specific context is provided, primarily use that
                # but also retrieve additional context if the selected text is too short
                if len(selected_context) < 100:  # If the selected text is too short, retrieve more context
                    context_docs = await self.retrieve_context(query)
            else:
                # Retrieve context based on the query
                context_docs = await self.retrieve_context(query)

            # Generate response using the context
            response = await self.generate_response(query, context_docs, selected_context)

            # Translate response if requested and it's not already in the target language
            if target_language and target_language != "en":
                logger.info(f"Translating response from English to {target_language}")
                translated_response = await translation_service.translate(
                    text=response.response,
                    source_lang="en",
                    target_lang=target_language
                )
                response.response = translated_response.translated_text
                logger.info(f"Translation completed: {translated_response.translated_text[:100]}...")

            logger.info(f"RAG query completed successfully")
            return response

        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            raise

# Singleton instance
rag_service = RAGService()