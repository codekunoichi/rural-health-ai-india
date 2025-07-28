import os
from typing import Dict, List
from pathlib import Path

class Settings:
    """Configuration settings for the Medical RAG System."""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    VECTOR_STORE_DIR = DATA_DIR / "vector_stores"
    
    # API Configuration
    MEDLINEPLUS_API_URL = "https://wsearch.nlm.nih.gov/ws/query"
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 30
    
    # RAG System Configuration
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    MAX_RETRIEVED_DOCS = 5
    SIMILARITY_THRESHOLD = 0.7
    
    # Embedding Configuration
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION = 384
    
    # Safety Configuration
    EMERGENCY_CONFIDENCE_THRESHOLD = 0.8
    RESPONSE_MAX_LENGTH = 500
    RESPONSE_TIMEOUT = 3.0  # seconds
    
    # Flask Configuration
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 5000
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        for dir_path in [cls.RAW_DATA_DIR, cls.PROCESSED_DATA_DIR, cls.VECTOR_STORE_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)