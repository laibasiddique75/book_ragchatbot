# RAG Chatbot Backend

This is the backend for a RAG (Retrieval-Augmented Generation) chatbot that allows users to chat with book content using AI models.

## Features

- FastAPI-based REST API
- Integration with OpenRouter and Google Gemini for AI responses
- Qdrant vector database for document similarity search
- Document indexing and retrieval capabilities
- Multi-language support with translation
- Support for PostgreSQL (with fallback to SQLite)

## API Endpoints

- `GET /` - Root endpoint with status information
- `GET /health` - Health check endpoint
- `POST /chat` - Chat with the RAG system
- `POST /translate` - Translate text between languages
- `POST /index-document` - Index documents for RAG search

## Deployment to Render

### Prerequisites

- Git repository with your code
- Render account

### Steps

1. Push your code to a Git repository
2. Create a new Web Service on Render
3. Select your repository
4. Set the runtime to Python
5. Set the build command: `pip install -r requirements.txt`
6. The start command is automatically detected from the `Procfile`
7. Add the required environment variables in the Render dashboard

### Required Environment Variables

- `OPENROUTER_API_KEY` - Your OpenRouter API key
- `OPENROUTER_MODEL` - Model to use (e.g., "openai/gpt-3.5-turbo")
- `GOOGLE_API_KEY` - Your Google API key for Gemini
- `GEMINI_MODEL` - Model to use (e.g., "gemini-2.0-flash")
- `QDRANT_HOST` - Your Qdrant host URL
- `QDRANT_API_KEY` - Your Qdrant API key
- `SECRET_KEY` - A secret key for your application
- `NEON_DB_URL` - Your PostgreSQL database URL (optional, falls back to SQLite)

### Optional Environment Variables

- `MAX_SOURCES` - Maximum number of sources to retrieve (default: 5)
- `MAX_CONTEXT_LENGTH` - Maximum context length (default: 4096)

## Local Development

To run locally for development:

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in a `.env` file
3. Run the application: `python main.py` or `uvicorn main:app --reload`

## Architecture

The backend consists of:

- **FastAPI** - Web framework
- **SQLAlchemy** - Database ORM (PostgreSQL with SQLite fallback)
- **Qdrant** - Vector database for similarity search
- **OpenRouter/Gemini** - Language models for responses
- **Custom RAG Service** - Logic for retrieval-augmented generation