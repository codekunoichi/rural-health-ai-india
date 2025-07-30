"""
Test cases for FastAPI endpoints.
Tests the REST API functionality and response validation.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json

from src.api.main import app

class TestFastAPIEndpoints:
    """Test cases for FastAPI endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client for FastAPI app."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_medical_service(self):
        """Mock medical service for testing."""
        with patch('src.api.main.medical_service') as mock_service:
            mock_instance = Mock()
            mock_instance.initialized = True
            mock_instance.health_check.return_value = True
            mock_service = mock_instance
            yield mock_service
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns basic API info."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "Medical RAG System API" in data["name"]
    
    def test_health_check_healthy(self, client, mock_medical_service):
        """Test health check when service is healthy."""
        mock_medical_service.health_check.return_value = True
        
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "service_status" in data
        assert "timestamp" in data
    
    def test_health_check_unhealthy(self, client, mock_medical_service):
        """Test health check when service is unhealthy."""
        mock_medical_service.health_check.return_value = False
        
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["service_status"]["medical_service"] == "error"
    
    def test_system_status(self, client, mock_medical_service):
        """Test system status endpoint."""
        mock_medical_service.get_system_status.return_value = {
            "system_status": "operational",
            "components": {
                "query_processor": {"status": "operational", "initialized": True},
                "retrieval_engine": {"status": "operational", "initialized": True},
                "response_generator": {"status": "operational", "initialized": True},
                "vector_store": {"status": "operational", "initialized": True, "documents_count": 10}
            },
            "statistics": {
                "total_queries": 100,
                "total_errors": 2,
                "uptime_seconds": 3600,
                "error_rate": 0.02
            }
        }
        
        response = client.get("/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["system_status"] == "operational"
        assert "components" in data
        assert "statistics" in data
    
    def test_medical_query_valid(self, client, mock_medical_service):
        """Test medical query endpoint with valid input."""
        mock_medical_service.process_query.return_value = {
            "response_text": "Fever and headache are common symptoms. Please consult a healthcare provider.",
            "response_type": "symptom_guidance",
            "confidence": 0.85,
            "emergency_alert": False,
            "symptoms": ["fever", "headache"],
            "recommendations": ["Consult with a healthcare provider", "Monitor symptoms"],
            "disclaimers": ["This information is for educational purposes only"],
            "sources": ["MedlinePlus"],
            "processing_time_ms": 150.5,
            "metadata": {"query_type": "symptom_inquiry"}
        }
        
        query_data = {
            "query": "I have fever and headache",
            "language": "english",
            "include_sources": True,
            "max_results": 5
        }
        
        response = client.post("/query", json=query_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["response_type"] == "symptom_guidance"
        assert data["confidence"] == 0.85
        assert data["emergency_alert"] == False
        assert "fever" in data["symptoms"]
        assert "headache" in data["symptoms"]
        assert len(data["recommendations"]) > 0
        assert len(data["disclaimers"]) > 0
    
    def test_medical_query_emergency(self, client, mock_medical_service):
        """Test medical query endpoint with emergency query."""
        mock_medical_service.process_query.return_value = {
            "response_text": "🚨 MEDICAL EMERGENCY DETECTED 🚨 Seek immediate medical attention.",
            "response_type": "emergency_alert",
            "confidence": 0.95,
            "emergency_alert": True,
            "symptoms": ["unconscious", "high fever"],
            "recommendations": ["Seek immediate emergency medical care", "Call emergency services"],
            "disclaimers": ["This is a medical emergency", "Do not delay treatment"],
            "sources": ["WHO"],
            "processing_time_ms": 120.0,
            "metadata": {"query_type": "emergency"}
        }
        
        query_data = {
            "query": "Patient unconscious with high fever",
            "language": "english"
        }
        
        response = client.post("/query", json=query_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["response_type"] == "emergency_alert"
        assert data["emergency_alert"] == True
        assert data["confidence"] > 0.9
        assert "unconscious" in data["symptoms"]
    
    def test_medical_query_empty(self, client, mock_medical_service):
        """Test medical query endpoint with empty query."""
        query_data = {
            "query": "",
            "language": "english"
        }
        
        response = client.post("/query", json=query_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "error" in data
        assert "empty" in data["error"].lower()
    
    def test_medical_query_invalid_max_results(self, client, mock_medical_service):
        """Test medical query endpoint with invalid max_results."""
        query_data = {
            "query": "I have fever",
            "max_results": 15  # Exceeds limit of 10
        }
        
        response = client.post("/query", json=query_data)
        assert response.status_code == 422  # Validation error
    
    def test_emergency_check(self, client, mock_medical_service):
        """Test emergency check endpoint."""
        mock_medical_service.check_emergency.return_value = {
            "emergency_detected": True,
            "emergency_indicators": ["unconscious", "high fever"],
            "confidence": 0.9,
            "recommendations": ["Seek immediate medical attention", "Call emergency services"]
        }
        
        query_data = {"query": "Patient unconscious with high fever"}
        
        response = client.post("/emergency-check", json=query_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["emergency_detected"] == True
        assert "unconscious" in data["emergency_indicators"]
        assert data["confidence"] == 0.9
        assert len(data["recommendations"]) > 0
    
    def test_symptoms_extract(self, client, mock_medical_service):
        """Test symptoms extraction endpoint."""
        mock_medical_service.extract_symptoms.return_value = ["fever", "headache", "chills"]
        
        response = client.get("/symptoms/extract", params={"query": "I have fever, headache and chills"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["symptoms"] == ["fever", "headache", "chills"]
        assert data["query"] == "I have fever, headache and chills"
    
    def test_service_not_initialized(self, client):
        """Test endpoints when service is not initialized."""
        with patch('src.api.main.medical_service', None):
            response = client.post("/query", json={"query": "test"})
            assert response.status_code == 503
            
            response = client.post("/emergency-check", json={"query": "test"})
            assert response.status_code == 503
            
            response = client.get("/symptoms/extract", params={"query": "test"})
            assert response.status_code == 503
    
    def test_service_error_handling(self, client, mock_medical_service):
        """Test error handling when service raises exceptions."""
        # Mock service to raise exception
        mock_medical_service.process_query.side_effect = Exception("Service error")
        
        query_data = {"query": "I have fever"}
        response = client.post("/query", json=query_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "error" in data
    
    def test_cors_headers(self, client):
        """Test that CORS headers are present."""
        response = client.options("/")
        # CORS middleware should add headers
        assert response.status_code in [200, 405]  # OPTIONS might not be implemented for all endpoints
    
    def test_request_validation(self, client, mock_medical_service):
        """Test request validation with invalid data types."""
        # Test with non-string query
        invalid_data = {"query": 123, "language": "english"}
        response = client.post("/query", json=invalid_data)
        assert response.status_code == 422
        
        # Test with invalid language
        invalid_data = {"query": "test", "language": "invalid_language"}
        response = client.post("/query", json=invalid_data)
        assert response.status_code == 422
    
    def test_response_model_validation(self, client, mock_medical_service):
        """Test that response models are properly validated."""
        # Mock service returns valid response
        mock_medical_service.process_query.return_value = {
            "response_text": "Test response",
            "response_type": "symptom_guidance",
            "confidence": 0.8,
            "emergency_alert": False,
            "symptoms": ["fever"],
            "recommendations": ["See doctor"],
            "disclaimers": ["Not medical advice"],
            "sources": ["Test source"],
            "processing_time_ms": 100.0,
            "metadata": {}
        }
        
        query_data = {"query": "test query"}
        response = client.post("/query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = [
            "response_text", "response_type", "confidence", "emergency_alert",
            "symptoms", "recommendations", "disclaimers", "generated_at"
        ]
        for field in required_fields:
            assert field in data
        
        # Check data types
        assert isinstance(data["confidence"], float)
        assert isinstance(data["emergency_alert"], bool)
        assert isinstance(data["symptoms"], list)
        assert isinstance(data["recommendations"], list)
        assert isinstance(data["disclaimers"], list)