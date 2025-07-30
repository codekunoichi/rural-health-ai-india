"""
Pydantic models for FastAPI request and response validation.
Defines the data structures for medical RAG system API.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from enum import Enum

class LanguageEnum(str, Enum):
    """Supported languages for medical queries."""
    ENGLISH = "english"
    HINDI = "hindi"
    AUTO = "auto"

class MedicalQueryRequest(BaseModel):
    """Request model for medical query processing."""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Medical query or symptom description",
        example="I have fever and headache for 2 days"
    )
    
    language: LanguageEnum = Field(
        default=LanguageEnum.AUTO,
        description="Language of the query (auto-detected if not specified)"
    )
    
    include_sources: bool = Field(
        default=True,
        description="Whether to include source attributions in response"
    )
    
    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of relevant documents to retrieve"
    )
    
    user_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional user context (age, location, etc.)"
    )
    
    @validator('query')
    def validate_query(cls, v):
        """Validate that query is not just whitespace."""
        if not v.strip():
            raise ValueError('Query cannot be empty or just whitespace')
        return v.strip()

class MedicalQueryResponse(BaseModel):
    """Response model for medical query processing."""
    
    response_text: str = Field(
        ...,
        description="Generated medical response text"
    )
    
    response_type: str = Field(
        ...,
        description="Type of response (emergency_alert, symptom_guidance, etc.)"
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the response (0.0 to 1.0)"
    )
    
    emergency_alert: bool = Field(
        ...,
        description="Whether this is an emergency situation"
    )
    
    symptoms: List[str] = Field(
        default_factory=list,
        description="Extracted symptoms from the query"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Medical recommendations based on the query"
    )
    
    disclaimers: List[str] = Field(
        default_factory=list,
        description="Medical disclaimers and safety information"
    )
    
    sources: Optional[List[str]] = Field(
        default=None,
        description="Medical sources used for the response"
    )
    
    processing_time_ms: Optional[float] = Field(
        default=None,
        description="Time taken to process the query in milliseconds"
    )
    
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the response was generated"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata about the response"
    )

class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: Literal["healthy", "unhealthy"] = Field(
        ...,
        description="Overall system health status"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of the health check"
    )
    
    service_status: Dict[str, str] = Field(
        ...,
        description="Status of individual services"
    )

class SystemStatusResponse(BaseModel):
    """Response model for detailed system status."""
    
    system_status: str = Field(
        ...,
        description="Overall system status"
    )
    
    components: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Status of system components"
    )
    
    statistics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="System statistics and metrics"
    )
    
    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp"
    )

class EmergencyCheckRequest(BaseModel):
    """Request model for emergency check endpoint."""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Medical query to check for emergency indicators"
    )

class EmergencyCheckResponse(BaseModel):
    """Response model for emergency check endpoint."""
    
    emergency_detected: bool = Field(
        ...,
        description="Whether emergency indicators were detected"
    )
    
    emergency_indicators: List[str] = Field(
        default_factory=list,
        description="List of detected emergency indicators"
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in emergency detection"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Emergency recommendations if applicable"
    )

class SymptomExtractionRequest(BaseModel):
    """Request model for symptom extraction endpoint."""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Medical text to extract symptoms from"
    )
    
    language: LanguageEnum = Field(
        default=LanguageEnum.AUTO,
        description="Language of the query"
    )

class SymptomExtractionResponse(BaseModel):
    """Response model for symptom extraction endpoint."""
    
    symptoms: List[str] = Field(
        ...,
        description="Extracted symptoms"
    )
    
    query: str = Field(
        ...,
        description="Original query"
    )
    
    confidence_scores: Optional[Dict[str, float]] = Field(
        default=None,
        description="Confidence scores for each extracted symptom"
    )

class ErrorResponse(BaseModel):
    """Response model for API errors."""
    
    error: str = Field(
        ...,
        description="Error message"
    )
    
    status_code: int = Field(
        ...,
        description="HTTP status code"
    )
    
    detail: Optional[str] = Field(
        default=None,
        description="Detailed error information"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Error timestamp"
    )

# Configuration models
class APIConfig(BaseModel):
    """Configuration model for API settings."""
    
    title: str = "Medical RAG System API"
    description: str = "AI-powered medical information system for rural healthcare"
    version: str = "1.0.0"
    debug: bool = False
    cors_origins: List[str] = ["*"]
    max_query_length: int = 1000
    default_language: LanguageEnum = LanguageEnum.AUTO
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # seconds

class MedicalContext(BaseModel):
    """Model for medical context information."""
    
    age_group: Optional[str] = Field(
        default=None,
        description="Age group (child, adult, elderly)"
    )
    
    gender: Optional[str] = Field(
        default=None,
        description="Gender information if relevant"
    )
    
    location: Optional[str] = Field(
        default=None,
        description="Geographic location (for region-specific health info)"
    )
    
    special_conditions: Optional[List[str]] = Field(
        default=None,
        description="Special conditions (pregnancy, chronic diseases, etc.)"
    )
    
    duration: Optional[str] = Field(
        default=None,
        description="Duration of symptoms"
    )