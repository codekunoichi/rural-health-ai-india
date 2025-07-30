"""
FastAPI main application for Medical RAG System.
Provides REST API endpoints for medical query processing and response generation.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any
from contextlib import asynccontextmanager

from .models import (
    MedicalQueryRequest, 
    MedicalQueryResponse, 
    HealthCheckResponse,
    SystemStatusResponse
)
from .medical_service import MedicalRAGService
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global service instance
medical_service: MedicalRAGService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    global medical_service
    
    # Startup
    logger.info("Starting Medical RAG System API...")
    try:
        medical_service = MedicalRAGService()
        await medical_service.initialize()
        logger.info("Medical RAG Service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Medical RAG Service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Medical RAG System API...")
    if medical_service:
        await medical_service.cleanup()

# Create FastAPI application
app = FastAPI(
    title="Medical RAG System API",
    description="AI-powered medical information system for rural healthcare in India, specializing in malaria symptom analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with basic API information."""
    return {
        "name": "Medical RAG System API",
        "version": "1.0.0",
        "description": "AI-powered medical information system for rural healthcare",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    try:
        is_healthy = await medical_service.health_check() if medical_service else False
        
        return HealthCheckResponse(
            status="healthy" if is_healthy else "unhealthy",
            timestamp=None,  # Will be set by the model
            service_status={
                "medical_service": "operational" if is_healthy else "error",
                "api": "operational"
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=None,
            service_status={
                "medical_service": "error",
                "api": "operational"
            }
        )

@app.get("/status", response_model=SystemStatusResponse)
async def system_status():
    """Get detailed system status."""
    try:
        if not medical_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Medical service not initialized"
            )
        
        status_info = await medical_service.get_system_status()
        return SystemStatusResponse(**status_info)
        
    except Exception as e:
        logger.error(f"System status check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system status: {str(e)}"
        )

@app.post("/query", response_model=MedicalQueryResponse)
async def process_medical_query(request: MedicalQueryRequest):
    """
    Process a medical query and return AI-generated medical information.
    
    This endpoint:
    1. Processes and analyzes the medical query
    2. Extracts symptoms and detects emergencies
    3. Retrieves relevant medical documents
    4. Generates contextual medical responses with safety measures
    """
    try:
        if not medical_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Medical service not initialized"
            )
        
        # Validate query
        if not request.query or not request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )
        
        # Process the medical query
        logger.info(f"Processing medical query: '{request.query[:50]}...'")
        response = await medical_service.process_query(
            query=request.query,
            language=request.language,
            include_sources=request.include_sources,
            max_results=request.max_results
        )
        
        return MedicalQueryResponse(**response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process medical query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/emergency-check")
async def emergency_check(request: MedicalQueryRequest):
    """
    Quick emergency detection endpoint.
    Returns only emergency status without full processing.
    """
    try:
        if not medical_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Medical service not initialized"
            )
        
        emergency_info = await medical_service.check_emergency(request.query)
        
        return {
            "emergency_detected": emergency_info["emergency_detected"],
            "emergency_indicators": emergency_info["emergency_indicators"],
            "confidence": emergency_info["confidence"],
            "recommendations": emergency_info.get("recommendations", [])
        }
        
    except Exception as e:
        logger.error(f"Emergency check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Emergency check failed: {str(e)}"
        )

@app.get("/symptoms/extract")
async def extract_symptoms_endpoint(query: str):
    """Extract symptoms from a medical query without full processing."""
    try:
        if not medical_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Medical service not initialized"
            )
        
        symptoms = await medical_service.extract_symptoms(query)
        
        return {
            "symptoms": symptoms,
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Symptom extraction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Symptom extraction failed: {str(e)}"
        )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions with proper logging."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "detail": str(exc) if Settings.DEBUG else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )