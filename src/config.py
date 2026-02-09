"""
Configuration Module
Centralized configuration management for the RAG pipeline
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for RAG pipeline"""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    
    # RAG Parameters
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))
    
    # Temperature for generation
    TEMPERATURE: float = 0.7
    
    # Max tokens for response
    MAX_TOKENS: int = 2048
    
    # Vector Store Settings
    VECTOR_STORE_PATH: str = "./vector_store"
    
    # Supported file types
    SUPPORTED_FILE_TYPES: list = [".pdf", ".docx", ".txt"]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        return True
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """Return a summary of current configuration"""
        return {
            "embedding_model": cls.EMBEDDING_MODEL,
            "llm_model": cls.LLM_MODEL,
            "chunk_size": cls.CHUNK_SIZE,
            "chunk_overlap": cls.CHUNK_OVERLAP,
            "top_k": cls.TOP_K_RESULTS,
            "temperature": cls.TEMPERATURE,
        }


# Create a singleton instance
config = Config()