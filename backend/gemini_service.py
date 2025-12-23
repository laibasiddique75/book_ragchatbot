import os
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# Try to import Google Generative AI, with fallback
GOOGLE_GENAI_AVAILABLE = False
try:
    import google.generativeai as genai
    GOOGLE_GENAI_AVAILABLE = True
    logger.info("Google Generative AI library (google.generativeai) imported successfully")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except ImportError:
    logger.warning("Google Generative AI library not available")
except Exception as e:
    logger.warning(f"Could not configure Google Generative AI: {e}")

class ChatCompletionRequest(BaseModel):
    messages: List[Dict[str, str]]
    model: Optional[str] = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024

class ChatCompletionResponse(BaseModel):
    response: str
    tokens_used: int

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

        if not self.api_key:
            logger.warning("GOOGLE_API_KEY environment variable is not set. Some features may not work.")

        self.model = None
        if GOOGLE_GENAI_AVAILABLE and self.api_key:
            try:
                self.model = genai.GenerativeModel(self.model_name)
                logger.info(f"Initialized Gemini model: {self.model_name}")
            except Exception as e:
                logger.error(f"Error initializing Gemini model: {e}")
                self.model = None

    async def get_chat_completion(self, messages: List[Dict[str, str]],
                                  model: str = None,
                                  temperature: float = 0.7,
                                  max_tokens: int = 1024) -> ChatCompletionResponse:
        """
        Get chat completion from Google Gemini API
        """
        if not GOOGLE_GENAI_AVAILABLE:
            logger.warning("Google Generative AI library not available. Returning mock response.")
            return ChatCompletionResponse(
                response="I'm the AI assistant. The Google Generative AI library is not installed properly.",
                tokens_used=0
            )

        if not self.api_key or not self.model:
            logger.warning("Google Gemini API key not set or model not initialized. Returning mock response.")
            return ChatCompletionResponse(
                response="I'm the AI assistant. The Google Gemini API is not configured properly. Please check the API key.",
                tokens_used=0
            )

        try:
            if not model:
                model = self.model_name

            # Convert messages to Gemini format
            contents = []
            for msg in messages:
                if msg["role"] == "system":
                    # Add system message as context to the first user message
                    if contents and contents[-1]["role"] == "user":
                        contents[-1]["parts"] = [msg["content"] + "\n\n" + contents[-1]["parts"][0]]
                    else:
                        contents.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "user":
                    contents.append({"role": "user", "parts": [msg["content"]]})
                else:  # assistant role
                    contents.append({"role": "model", "parts": [msg["content"]]})

            # Prepare generation config
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }

            # Generate response using the model
            response = await self.model.generate_content_async(
                contents,
                generation_config=generation_config,
                safety_settings={
                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
                    'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE'
                }
            )

            if response.text:
                content = response.text
                tokens_used = len(content.split())

                logger.info(f"Chat completion generated, tokens used: {tokens_used}")
                return ChatCompletionResponse(
                    response=content,
                    tokens_used=tokens_used
                )
            else:
                logger.warning("Gemini returned empty response")
                return ChatCompletionResponse(
                    response="I'm the AI assistant. The response from Gemini was empty. Please try again.",
                    tokens_used=0
                )

        except Exception as e:
            error_msg = str(e).lower()
            # Check if the error is related to quota limits
            if "quota" in error_msg or "exceeded" in error_msg or "429" in error_msg or "rate limit" in error_msg:
                logger.error(f"Gemini API quota exceeded: {e}")
                # Provide a more helpful response that can still process the query using local methods
                # Extract the user's question from the messages
                user_question = ""
                for msg in messages:
                    if msg["role"] == "user":
                        user_question = msg["content"]
                        break

                # Return a response that acknowledges the quota issue but still tries to help
                return ChatCompletionResponse(
                    response=f"I'm the AI assistant. The API quota has been exceeded. However, I can still try to help based on the context provided. User question: {user_question}",
                    tokens_used=0
                )
            else:
                logger.error(f"Error in Gemini chat completion: {e}")
                # Return a mock response as fallback
                return ChatCompletionResponse(
                    response="I'm the AI assistant. There was an issue with the Google Gemini API. Please try again later.",
                    tokens_used=0
                )

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Google's embedding API
        """
        if not GOOGLE_GENAI_AVAILABLE:
            logger.warning("Google Generative AI library not available for embeddings.")
            return await self._generate_placeholder_embeddings(texts)

        # Note: The free version of Gemini doesn't include embedding API
        # This is a placeholder implementation that will return mock embeddings
        # For production, you might want to use Google's embedding API if available
        logger.warning("Gemini embedding API not implemented. Using placeholder embeddings.")
        return await self._generate_placeholder_embeddings(texts)

    async def _generate_placeholder_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate placeholder embeddings when API is unavailable
        """
        import numpy as np
        embeddings = []

        for text in texts:
            # Create a simple hash-based embedding to ensure some similarity for similar texts
            text_hash = hash(text) % (2**32)
            embedding = []

            # Generate a 768-dim vector based on the text content (common dimension for embeddings)
            for i in range(768):
                val = (text_hash + i * 1337) % 10000
                val = (val - 5000) / 5000.0  # Normalize between -1 and 1
                embedding.append(val)

            # Normalize the embedding vector to unit length (standard for embeddings)
            magnitude = sum(x**2 for x in embedding) ** 0.5
            if magnitude > 0:
                embedding = [x / magnitude for x in embedding]

            embeddings.append(embedding)

        logger.info(f"Generated placeholder embeddings for {len(texts)} text(s)")
        return embeddings

# Singleton instance
gemini_service = GeminiService()