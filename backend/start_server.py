#!/usr/bin/env python3
"""
Start the RAG Chatbot API server
"""
import os
import sys
import subprocess
import time

def start_server():
    """
    Start the FastAPI server
    """
    print("Starting RAG Chatbot API server...")
    print("This will start the server on http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the server using uvicorn
    try:
        # Use the proper command to run uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"  # Auto-reload on file changes
        ]
        
        process = subprocess.Popen(cmd)
        
        print(f"Server started with PID {process.pid}")
        print("Server is now running at: http://127.0.0.1:8000")
        print("API Documentation available at: http://127.0.0.1:8000/docs")
        
        # Wait for the process to complete (or be interrupted)
        process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("Server stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    start_server()