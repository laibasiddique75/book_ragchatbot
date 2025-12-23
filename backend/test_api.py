import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import and test Gemini API
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")
    print(f"Model name: {model_name}")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        print("Testing API connection...")
        
        # Simple test
        response = model.generate_content("Hello, how are you?")
        print(f"Response: {response.text}")
        print("API test successful!")
    else:
        print("No API key found!")
        
except Exception as e:
    print(f"Error testing API: {e}")
    import traceback
    traceback.print_exc()