import logging
from typing import Optional
from pydantic import BaseModel
import asyncio
import json

from gemini_service import gemini_service
from openrouter import openrouter_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"  # Default source language is English
    target_lang: str = "ur"  # Default target language is Urdu

class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str
    tokens_used: int = 0

class TranslationService:
    def __init__(self):
        self.supported_languages = {
            "en": "English",
            "ur": "Urdu"
        }

    async def translate(self, text: str, source_lang: str = "en", target_lang: str = "ur") -> TranslationResponse:
        """
        Translate text between English and Urdu using AI services
        """
        if source_lang not in self.supported_languages or target_lang not in self.supported_languages:
            raise ValueError(f"Unsupported languages. Supported languages: {list(self.supported_languages.keys())}")

        if source_lang == target_lang:
            # No translation needed
            return TranslationResponse(
                translated_text=text,
                source_lang=source_lang,
                target_lang=target_lang,
                tokens_used=0
            )

        try:
            # Create a prompt for translation
            if source_lang == "en" and target_lang == "ur":
                prompt = f"Translate the following English text to Urdu. Only respond with the translated text and nothing else:\n\n{text}"
            elif source_lang == "ur" and target_lang == "en":
                prompt = f"Translate the following Urdu text to English. Only respond with the translated text and nothing else:\n\n{text}"
            else:
                raise ValueError(f"Translation from {source_lang} to {target_lang} is not supported")

            # Prepare messages for the language model
            messages = [
                {
                    "role": "system",
                    "content": "You are a professional translator. Accurately translate between English and Urdu. Only return the translated text without any additional commentary."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            # Try Gemini service first (if available)
            if gemini_service.model:
                try:
                    response = await gemini_service.get_chat_completion(
                        messages=messages,
                        temperature=0.1,  # Low temperature for more accurate translations
                        max_tokens=2048
                    )

                    return TranslationResponse(
                        translated_text=response.response,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        tokens_used=response.tokens_used
                    )
                except Exception as e:
                    logger.warning(f"Gemini translation failed: {e}. Falling back to OpenRouter.")

            # Fall back to OpenRouter service
            try:
                response = await openrouter_service.get_chat_completion(
                    messages=messages,
                    temperature=0.1,  # Low temperature for more accurate translations
                    max_tokens=2048
                )

                return TranslationResponse(
                    translated_text=response.response,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    tokens_used=response.tokens_used
                )
            except Exception as e:
                logger.error(f"OpenRouter translation failed: {e}")

                # If both services fail, return a basic response
                fallback_text = f"[Translation unavailable: {text}]"
                return TranslationResponse(
                    translated_text=fallback_text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    tokens_used=0
                )

        except Exception as e:
            logger.error(f"Error in translation: {e}")
            # Return original text if translation fails
            return TranslationResponse(
                translated_text=text,
                source_lang=source_lang,
                target_lang=target_lang,
                tokens_used=0
            )

# Singleton instance
translation_service = TranslationService()