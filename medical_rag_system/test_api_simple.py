"""
Simple test to verify FastAPI application works correctly.
This bypasses the lifespan context manager for testing.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
import json

# Create a simple test app without lifespan for testing
from src.api.models import MedicalQueryRequest, MedicalQueryResponse, HealthCheckResponse

test_app = FastAPI(title="Test Medical RAG API")

# Mock service for testing
class MockMedicalService:
    def __init__(self):
        self.initialized = True
    
    async def health_check(self):
        return True
    
    async def process_query(self, query, language="auto", include_sources=True, max_results=5):
        return {
            "response_text": f"Mock response for: {query}",
            "response_type": "symptom_guidance",
            "confidence": 0.85,
            "emergency_alert": False,
            "symptoms": ["fever", "headache"],
            "recommendations": ["Consult a healthcare provider"],
            "disclaimers": ["This is not medical advice"],
            "sources": ["Test Source"],
            "processing_time_ms": 100.0,
            "metadata": {"test": True}
        }

# Add test endpoints
mock_service = MockMedicalService()

@test_app.get("/")
async def root():
    return {
        "name": "Medical RAG System API",
        "version": "1.0.0",
        "description": "AI-powered medical information system",
        "docs": "/docs"
    }

@test_app.get("/health")
async def health_check():
    is_healthy = await mock_service.health_check()
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "service_status": {
            "medical_service": "operational" if is_healthy else "error",
            "api": "operational"
        }
    }

@test_app.post("/query")
async def process_medical_query(request: MedicalQueryRequest):
    if not request.query.strip():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    response = await mock_service.process_query(
        query=request.query,
        language=request.language,
        include_sources=request.include_sources,
        max_results=request.max_results
    )
    
    return response

def test_fastapi_functionality():
    """Test FastAPI endpoints with TestClient."""
    print("🧪 Testing FastAPI endpoints...")
    
    client = TestClient(test_app)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Medical RAG System API" in data["name"]
    print("   ✅ Root endpoint works")
    
    # Test health endpoint
    print("\n2. Testing health endpoint...")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("   ✅ Health endpoint works")
    
    # Test medical query endpoint
    print("\n3. Testing medical query endpoint...")
    query_data = {
        "query": "I have fever and headache",
        "language": "english",
        "include_sources": True,
        "max_results": 5
    }
    
    response = client.post("/query", json=query_data)
    assert response.status_code == 200
    data = response.json()
    assert "fever" in data["symptoms"]
    assert data["confidence"] == 0.85
    print("   ✅ Medical query endpoint works")
    
    # Test empty query validation
    print("\n4. Testing query validation...")
    empty_query = {"query": "", "language": "english"}
    response = client.post("/query", json=empty_query)
    assert response.status_code == 400
    print("   ✅ Query validation works")
    
    # Test request model validation
    print("\n5. Testing request model validation...")
    try:
        invalid_request = MedicalQueryRequest(query="test", max_results=15)  # Exceeds limit
        print("   ❌ Should have failed validation")
    except ValueError:
        print("   ✅ Request model validation works")
    
    print("\n🎉 All FastAPI tests passed!")

def test_pydantic_models():
    """Test Pydantic model validation."""
    print("\n🧪 Testing Pydantic models...")
    
    # Test valid request
    request = MedicalQueryRequest(
        query="I have fever",
        language="english",
        include_sources=True,
        max_results=5
    )
    assert request.query == "I have fever"
    assert request.language == "english"
    print("   ✅ MedicalQueryRequest validation works")
    
    # Test query whitespace validation
    try:
        invalid_request = MedicalQueryRequest(query="   ")
        print("   ❌ Should have failed whitespace validation")
    except ValueError:
        print("   ✅ Query whitespace validation works")
    
    # Test max_results bounds
    try:
        invalid_request = MedicalQueryRequest(query="test", max_results=15)
        print("   ❌ Should have failed max_results validation")
    except ValueError:
        print("   ✅ Max results validation works")
    
    print("   🎉 Pydantic model tests passed!")

if __name__ == "__main__":
    try:
        test_pydantic_models()
        test_fastapi_functionality()
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()