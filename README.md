# Physical AI & Humanoid Robotics RAG Chatbot

This project integrates a Retrieval-Augmented Generation (RAG) chatbot with the Physical AI & Humanoid Robotics book documentation. The chatbot can answer questions about the book content using a combination of vector search and language model generation.

## Features

- **Modern Blue-Themed UI**: Consistent blue color scheme throughout the site
- **Interactive Chatbot**: Ask questions about the Physical AI & Humanoid Robotics content
- **Context Selection**: Select text on any page to ask questions about specific content
- **Source Attribution**: Chatbot provides sources for its answers
- **Responsive Design**: Works well on both desktop and mobile devices

## Architecture

The system consists of:
- **Frontend**: Docusaurus documentation site with integrated chatbot UI and blue-themed design
- **Backend**: FastAPI application with RAG logic
- **Database**: PostgreSQL for metadata storage
- **Vector Store**: Qdrant for document embeddings
- **AI Models**: Qwen embeddings via OpenRouter for generation

## Prerequisites

- Python 3.8+
- Node.js 18+
- Access to OpenRouter API
- Qdrant Cloud account
- Neon Serverless Postgres account (optional for production)

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables by copying the `.env` file:
   ```bash
   cp .env .env.local
   ```

   Then edit `.env.local` with your API keys and configuration:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `QDRANT_API_KEY`: Your Qdrant Cloud API key
   - `QDRANT_HOST`: Your Qdrant Cloud URL
   - `NEON_DB_URL`: Your Neon Postgres connection string (optional)

4. Start the backend server:
   ```bash
   npm install  # Installs uvicorn via the package.json script
   npm run dev
   ```

   Or directly:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Docusaurus development server:
   ```bash
   npm start
   ```

## Indexing the Book Content

After starting the backend, you need to index the book content:

1. Make sure the backend server is running
2. Run the indexing script:
   ```bash
   python index_book_content.py
   ```

This will:
- Read all markdown files from the frontend documentation
- Chunk the content
- Generate embeddings using Qwen model
- Store embeddings in Qdrant
- Store document metadata in the database

## Using the Chatbot

1. Access the documentation site at `http://localhost:3000`
2. Navigate to the "Chat with Book" page from the navigation menu
3. Ask questions about the Physical AI & Humanoid Robotics content
4. You can also select text on any page and ask questions specifically about that content

## UI Design

- **Hero Section**: Blue gradient background with white text
- **Feature Cards**: Consistent blue-themed cards with hover effects
- **Chat Interface**: Modern chat UI with blue accents and smooth animations
- **Navigation**: Blue-themed header with consistent styling
- **Responsive**: Works on all device sizes with appropriate adjustments

## API Endpoints

- `GET /` - Health check
- `POST /chat` - Main chat endpoint
- `POST /index-document` - Index a single document
- `GET /docs` - Get indexed documents
- `POST /index-book` - Index the entire book (not fully implemented)

## Configuration

### OpenRouter Model
The default model is configured in `.env`. You can use Qwen or any other supported model:
- `OPENROUTER_MODEL=qwen/qwen-2-72b-instruct` (example)

### Qdrant Collection
- By default, the collection name is `book_embeddings`
- Vector size is 768 dimensions

## Testing

1. Check backend health: `GET http://localhost:8000/health`
2. Test chat endpoint with sample data
3. Verify the frontend chat interface connects to the backend

## Deployment

### Backend
Deploy the FastAPI application to any cloud provider that supports Python applications (e.g., Heroku, Railway, AWS, GCP).

### Frontend
The Docusaurus site can be deployed to:
- GitHub Pages
- Vercel
- Netlify
- Any static hosting service

Remember to update the `BACKEND_URL` in the frontend chat component with your deployed backend URL.

## Troubleshooting

- If the backend server won't start, check that all dependencies are installed
- If the chatbot doesn't respond, verify that your API keys are correct
- Check the browser console for frontend errors and the backend logs for server errors
- Make sure the book content is properly indexed before testing the chat functionality

## Security Notes

- Never commit API keys to version control
- Use environment variables for all sensitive configuration
- Implement rate limiting in production
- Validate and sanitize all user inputs