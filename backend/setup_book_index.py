import asyncio
import os
from dotenv import load_dotenv
from vector_store import qdrant_service
from database import SessionLocal, Document
import uuid

# Load environment variables
load_dotenv()

async def index_sample_book_content():
    """
    Index sample book content about Physical AI & Humanoid Robotics
    """
    print("Starting to index book content...")

    # Sample content about Physical AI (this would normally come from your book files)
    sample_content = """
    Chapter 1: Introduction to Physical AI

    Physical AI represents a paradigm shift in artificial intelligence, where the traditional focus on purely computational intelligence is expanded to include the physical interaction and embodiment of intelligent systems. Unlike conventional AI that operates primarily in virtual environments or with abstract data, Physical AI encompasses systems that must understand and interact with the physical world in real-time.

    The concept of Physical AI is particularly relevant in the context of humanoid robotics, where robots must navigate complex physical environments, manipulate objects, and interact with humans in natural settings. This requires a fusion of perception, reasoning, and action that mirrors human capabilities.

    Why Physical AI?

    Physical AI is crucial for several reasons:

    1. Real-world interaction: Traditional AI systems operate on data that has already been processed and structured. Physical AI systems must operate on raw sensory input and produce real-time responses that affect the physical world.

    2. Embodied cognition: The physical form and interaction with the environment shape the intelligence of the system. This is particularly important for humanoid robots that need to understand spatial relationships, physics, and human interaction.

    3. Safety and reliability: Physical AI systems must be extremely reliable since their errors can have physical consequences. This requires robust perception, planning, and control systems.

    4. Human-robot interaction: For robots to work alongside humans effectively, they need to understand physical social cues, spatial relationships, and the physics of collaborative tasks.

    Chapter 2: Foundations of Humanoid Robotics

    Humanoid robotics is a field that combines multiple disciplines including mechanical engineering, electrical engineering, computer science, and cognitive science. The goal is to create robots that have human-like form and capabilities.

    The human form is chosen for several reasons:

    - Compatibility with human environments designed for humans
    - Natural interaction with humans
    - Understanding of human behavior through embodiment

    The challenges in humanoid robotics include:

    - Complex mechanical design for human-like movement
    - Real-time control of multiple degrees of freedom
    - Robust balance and locomotion
    - Human-like perception and cognition
    - Safe physical interaction with humans

    Chapter 3: Integration of Physical AI and Humanoid Systems

    The integration of Physical AI principles with humanoid robotics creates systems that can:

    - Learn from physical interaction
    - Adapt to changing environments
    - Develop understanding through embodiment
    - Perform complex manipulation tasks
    - Navigate human-centric spaces

    This integration requires advances in:

    - Sensor fusion and perception
    - Real-time decision making
    - Adaptive control systems
    - Learning from physical experience
    - Human-robot collaboration

    The future of Physical AI and humanoid robotics lies in creating systems that can learn, adapt, and interact in ways that are natural and beneficial for human society.

    Additional context on Why Physical AI:

    Physical AI is important because it bridges the gap between digital intelligence and physical action. While traditional AI excels at pattern recognition, data analysis, and virtual tasks, Physical AI systems must handle the complexity, uncertainty, and real-time constraints of the physical world.

    The physical world presents unique challenges:

    - Continuity: Physical systems must operate continuously, not in discrete steps
    - Real-time constraints: Delays in physical action can have immediate consequences
    - Uncertainty: Sensor readings are noisy and incomplete
    - Dynamics: Physical systems must understand and predict motion and forces
    - Safety: Physical actions must be safe for humans and the environment

    By developing Physical AI, we can create robots and intelligent systems that can work alongside humans, assist in daily tasks, perform dangerous operations, and ultimately create a more integrated human-AI society.
    """

    # Create document ID and metadata
    doc_id = f"physical_ai_book_{uuid.uuid4()}"
    doc_title = "Physical AI & Humanoid Robotics - Complete Book Content"
    doc_section = "Complete Book"

    # Chunk the content
    chunks = chunk_document(sample_content)

    print(f"Indexing {len(chunks)} chunks of book content...")

    # Store in database
    db = SessionLocal()
    try:
        # Create document record
        doc = Document(
            doc_id=doc_id,
            title=doc_title,
            content=sample_content,
            section=doc_section,
            is_indexed=True
        )
        db.add(doc)
        db.commit()
        print("Document saved to database")
    except Exception as e:
        print(f"Error saving document to database: {e}")
        db.rollback()
    finally:
        db.close()

    # Store embeddings in Qdrant
    if chunks and qdrant_service.connected:
        doc_ids = [doc_id] * len(chunks)
        metadata_list = [{"section": doc_section, "title": doc_title} for _ in chunks]

        vector_ids = await qdrant_service.store_embeddings(chunks, doc_ids, metadata_list)
        print(f"Stored {len(vector_ids)} vectors in Qdrant")

        # Update document record with embedding reference
        db = SessionLocal()
        try:
            doc = db.query(Document).filter(Document.doc_id == doc_id).first()
            if doc:
                doc.embedding_vector_id = ",".join(vector_ids)
                db.commit()
                print("Updated document with embedding references")
        finally:
            db.close()
    else:
        print("Could not store embeddings - Qdrant not connected or no chunks")

    print("Book indexing completed successfully!")
    return len(chunks)

def chunk_document(content: str, chunk_size: int = 800, overlap: int = 50) -> list:
    """
    Split content into overlapping chunks for better context retention
    """
    if not content:
        return []

    chunks = []
    start = 0
    length = len(content)

    # Prevent infinite loops and memory issues
    max_chunks = len(content) // 100  # Reasonable upper limit
    chunk_count = 0

    while start < length and chunk_count < max_chunks:
        end = min(start + chunk_size, length)
        chunk = content[start:end]

        # Only add chunks that have meaningful content
        if chunk.strip():
            chunks.append(chunk)
            chunk_count += 1

        # Move start position with overlap
        start = end - overlap

        # Prevent infinite loops
        if start <= start:  # Safety check to prevent infinite loops
            start += chunk_size

        # Handle the case where the remaining content is smaller than overlap
        if start >= length:
            break

    return chunks

if __name__ == "__main__":
    print("Setting up book indexing...")
    asyncio.run(index_sample_book_content())