#!/usr/bin/env python3
"""
Startup script for Medical RAG System FastAPI server.
"""

import uvicorn
import logging
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import Settings

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, Settings.LOG_LEVEL),
        format=Settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('medical_rag_api.log')
        ]
    )

def main():
    """Main function to start the FastAPI server."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Medical RAG System API...")
    logger.info(f"Debug mode: {Settings.DEBUG}")
    
    # Ensure required directories exist
    Settings.ensure_directories()
    
    # Start the server
    try:
        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=Settings.DEBUG,
            log_level=Settings.LOG_LEVEL.lower(),
            access_log=True,
            loop="asyncio"
        )
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()