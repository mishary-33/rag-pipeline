"""
Configuration Module
Centralized configuration management for the RAG pipeline
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for RAG pipeline"""
    
    # API Keys (ONLY THIS FROM ENVIRONMENT)
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration (HARDCODED)
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large"
    LLM_MODEL: str = "gemini-3-flash-preview"
    EMBEDDING_DIMENSION: int = 1024
    
    # RAG Parameters (HARDCODED)
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 3
    
    # Generation Settings (HARDCODED)
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2048
    
    # Vector Store Settings (HARDCODED)
    VECTOR_STORE_PATH: str = "./vector_store"
    
    # Supported file types (HARDCODED)
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
            "embedding_dimension": cls.EMBEDDING_DIMENSION,
            "chunk_size": cls.CHUNK_SIZE,
            "chunk_overlap": cls.CHUNK_OVERLAP,
            "top_k": cls.TOP_K_RESULTS,
            "temperature": cls.TEMPERATURE,
        }


# Create a singleton instance
config = Config()