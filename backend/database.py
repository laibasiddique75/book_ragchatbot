# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime
# import os

# # Database setup
# DATABASE_URL = os.getenv("NEON_DB_URL", "sqlite:///./rag_chatbot.db")  # Fallback to SQLite for development

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# class Document(Base):
#     __tablename__ = "documents"

#     id = Column(Integer, primary_key=True, index=True)
#     doc_id = Column(String, unique=True, index=True)
#     title = Column(String, index=True)
#     content = Column(Text)
#     section = Column(String, index=True)  # e.g., "introduction", "ros2-fundamentals"
#     embedding_vector_id = Column(String)  # Reference to Qdrant vector ID
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     is_indexed = Column(Boolean, default=False)
#     metadata = Column(Text)  # JSON string for additional metadata

# class ChatSession(Base):
#     __tablename__ = "chat_sessions"

#     id = Column(Integer, primary_key=True, index=True)
#     session_id = Column(String, unique=True, index=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     is_active = Column(Boolean, default=True)

# class ChatMessage(Base):
#     __tablename__ = "chat_messages"

#     id = Column(Integer, primary_key=True, index=True)
#     session_id = Column(String, index=True)  # References chat_sessions.session_id
#     role = Column(String)  # 'user' or 'assistant'
#     content = Column(Text)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     sources = Column(Text)  # JSON string for source documents

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv(
    "NEON_DB_URL",
    "sqlite:///./rag_chatbot.db"  # Fallback to SQLite
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ===================== MODELS =====================

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    section = Column(String, index=True)  # e.g., introduction, ros2-fundamentals
    embedding_vector_id = Column(String)  # Qdrant vector ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_indexed = Column(Boolean, default=False)

    doc_metadata = Column(Text)  # ✅ FIXED (was metadata ❌)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user / assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sources = Column(Text)  # JSON string for source docs


# ===================== CREATE TABLES =====================
Base.metadata.create_all(bind=engine)
