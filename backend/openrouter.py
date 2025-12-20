import os
import logging
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatCompletionRequest(BaseModel):
    messages: List[Dict[str, str]]
    model: Optional[str] = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024

class ChatCompletionResponse(BaseModel):
    response: str
    tokens_used: int

class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY environment variable is not set. Some features may not work.")

        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = httpx.Timeout(30.0)  # 30 second timeout

    async def get_chat_completion(self, messages: List[Dict[str, str]],
                                  model: str = None,
                                  temperature: float = 0.7,
                                  max_tokens: int = 1024) -> ChatCompletionResponse:
        """
        Get chat completion from OpenRouter API
        """
        # Check if API key is available
        if not self.api_key:
            logger.warning("OpenRouter API key not set. Returning mock response.")
            # Return a mock response as fallback
            return ChatCompletionResponse(
                response="I'm the AI assistant. The OpenRouter API is not configured properly. Please check the API key.",
                tokens_used=0
            )

        try:
            if not model:
                model = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data
                )

                if response.status_code != 200:
                    logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                    # Return a mock response as fallback
                    return ChatCompletionResponse(
                        response="I'm the AI assistant. There was an issue with the OpenRouter API. Please try again later.",
                        tokens_used=0
                    )

                result = response.json()

                content = result["choices"][0]["message"]["content"]
                tokens_used = result.get("usage", {}).get("total_tokens", 0)

            logger.info(f"Chat completion generated, tokens used: {tokens_used}")
            return ChatCompletionResponse(
                response=content,
                tokens_used=tokens_used
            )

        except Exception as e:
            logger.error(f"Error in OpenRouter chat completion: {e}")
            # Return a mock response as fallback
            return ChatCompletionResponse(
                response="I'm the AI assistant. There was an issue with the OpenRouter API. Please try again later.",
                tokens_used=0
            )

# Singleton instance
openrouter_service = OpenRouterService()