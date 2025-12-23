# Deploying Your RAG Chatbot Backend to Render

## Prerequisites
- A Render account (sign up at https://render.com)
- Your project files ready for deployment

## Deployment Steps

### 1. Prepare Your Repository
- Push your backend code to a Git repository (GitHub, GitLab, or Bitbucket)
- Make sure all necessary files are included:
  - main.py (your FastAPI application)
  - requirements.txt
  - Procfile
  - runtime.txt
  - All other Python files (database.py, rag.py, etc.)

### 2. Create a New Web Service on Render
1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Select the branch you want to deploy (usually main or master)

### 3. Configure the Web Service
- **Environment**: Choose "Python"
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: The Procfile already contains the start command: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Region**: Choose the region closest to your users

### 4. Set Environment Variables
In your Render dashboard, go to your service settings and add the following environment variables:

#### Required Environment Variables:
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `OPENROUTER_MODEL`: Model to use (e.g., "openai/gpt-3.5-turbo")
- `GOOGLE_API_KEY`: Your Google API key for Gemini
- `GEMINI_MODEL`: Model to use (e.g., "gemini-2.0-flash")
- `QDRANT_HOST`: Your Qdrant host URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `SECRET_KEY`: A secret key for your application
- `NEON_DB_URL`: Your PostgreSQL database URL (for production) - if not provided, will use SQLite

#### Optional Environment Variables:
- `MAX_SOURCES`: Maximum number of sources to retrieve (default: 5)
- `MAX_CONTEXT_LENGTH`: Maximum context length (default: 4096)

### 5. Deploy
- Click "Create Web Service"
- Render will automatically build and deploy your application
- Monitor the logs to ensure everything is working correctly

## Important Notes

1. **Database**: The application uses SQLite as a fallback (rag_chatbot.db) but is configured to use PostgreSQL in production via the NEON_DB_URL environment variable.

2. **Qdrant Vector Database**: Make sure your Qdrant instance is accessible from the internet since Render will need to connect to it.

3. **Health Checks**: The application has a health check endpoint at `/health` that returns the status of the service.

4. **API Endpoints**:
   - GET `/` - Root endpoint
   - GET `/health` - Health check
   - POST `/chat` - Chat functionality
   - POST `/translate` - Translation functionality
   - POST `/index-document` - Document indexing

5. **Security**: The current CORS settings allow all origins. In production, you should restrict this to your frontend domain only.

## Troubleshooting

- Check the Render logs if your application fails to start
- Ensure all required environment variables are set
- Verify that your Qdrant instance is accessible
- Confirm that your database connection string is correct

## Updating Your Deployment

After making changes to your code:
1. Commit and push your changes to the repository
2. Render will automatically detect the changes and deploy a new version