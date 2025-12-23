import os
import requests
import json
from pathlib import Path

def index_book_content():
    """
    Index the book content from frontend/docs directory to the backend
    """
    backend_url = "http://localhost:8000"
    
    # Check if backend is running
    try:
        response = requests.get(f"{backend_url}/health")
        if response.status_code != 200:
            print("Backend server might not be running. Please start the backend server first.")
            print("Run: uvicorn main:app --reload")
            return
        print("Backend server is running...")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to backend server. Please start the backend server first.")
        print("Run: uvicorn main:app --reload")
        return
    
    # Get all markdown files from the docs directory
    docs_path = Path("../frontend/docs")  # Relative to backend directory
    
    if not docs_path.exists():
        print(f"Docs directory not found at {docs_path}")
        return
    
    markdown_files = list(docs_path.rglob("*.md"))
    
    if not markdown_files:
        print("No markdown files found in docs directory")
        return
    
    print(f"Found {len(markdown_files)} markdown files to index")
    
    for file_path in markdown_files:
        try:
            # Read the content of the markdown file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from the file content (look for title in frontmatter or first heading)
            title = file_path.stem.replace('_', ' ').title()  # Default to filename
            
            # Look for title in frontmatter (between ---)
            lines = content.split('\n')
            in_frontmatter = False
            title_from_frontmatter = None
            
            for line in lines:
                if line.strip() == '---':
                    if not in_frontmatter:
                        in_frontmatter = True
                    else:
                        break  # End of frontmatter
                elif in_frontmatter and line.startswith('title:'):
                    title_from_frontmatter = line.split(':', 1)[1].strip().strip('"\'')
                    break
            else:
                # If no frontmatter title found, look for first heading
                for line in lines:
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
            
            if title_from_frontmatter:
                title = title_from_frontmatter
            
            # Create document ID from file path
            doc_id = str(file_path.relative_to(docs_path)).replace(os.sep, '_').replace('.md', '')
            doc_id = doc_id.replace('..', '').replace('__', '_').strip('_')
            
            # Prepare the request payload
            payload = {
                "content": content,
                "doc_id": doc_id,
                "doc_title": title,
                "doc_section": str(file_path.parent.relative_to(docs_path)) if file_path.parent != docs_path else "main"
            }
            
            print(f"Indexing: {doc_id} - {title}")
            
            # Send the request to the backend
            response = requests.post(f"{backend_url}/index-document", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Successfully indexed: {doc_id} - {result['chunks_processed']} chunks processed")
            else:
                print(f"  ✗ Failed to index {doc_id}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")

    print("\nIndexing process completed!")
    print("Now you can access the book content in both English and Urdu.")

if __name__ == "__main__":
    index_book_content()