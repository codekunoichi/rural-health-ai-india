"""
Demo script to showcase FastAPI endpoints for Medical RAG System.
This script demonstrates the API functionality without requiring a running server.
"""

import json
from datetime import datetime
from typing import Dict, Any

# Import our models to test them
from src.api.models import (
    MedicalQueryRequest, 
    MedicalQueryResponse, 
    HealthCheckResponse,
    LanguageEnum
)

def demo_request_response_models():
    """Demonstrate request and response model functionality."""
    print("🏥 Medical RAG System FastAPI Demo")
    print("=" * 50)
    
    print("\n1. 📝 Request Model Validation:")
    
    # Test valid requests
    valid_requests = [
        {
            "query": "I have fever and headache for 2 days",
            "language": "english",
            "include_sources": True,
            "max_results": 5
        },
        {
            "query": "मुझे बुखार है",  # Hindi query
            "language": "hindi",
            "include_sources": False,
            "max_results": 3
        }
    ]
    
    for i, req_data in enumerate(valid_requests, 1):
        try:
            request = MedicalQueryRequest(**req_data)
            print(f"   ✅ Request {i}: '{request.query}' (lang: {request.language})")
        except Exception as e:
            print(f"   ❌ Request {i} failed: {e}")
    
    # Test validation errors
    print("\n   Testing validation errors:")
    invalid_requests = [
        {"query": ""},  # Empty query
        {"query": "test", "max_results": 15},  # Exceeds limit
        {"query": "test", "language": "invalid_lang"}  # Invalid language
    ]
    
    for i, req_data in enumerate(invalid_requests, 1):
        try:
            request = MedicalQueryRequest(**req_data)
            print(f"   ❌ Should have failed: {req_data}")
        except Exception as e:
            print(f"   ✅ Validation error {i}: {type(e).__name__}")
    
    print("\n2. 📤 Response Model Creation:")
    
    # Create sample responses
    sample_responses = [
        {
            "response_text": "Fever and headache are common symptoms. Please consult a healthcare provider for proper evaluation.",
            "response_type": "symptom_guidance",
            "confidence": 0.85,
            "emergency_alert": False,
            "symptoms": ["fever", "headache"],
            "recommendations": [
                "Consult with a healthcare provider",
                "Monitor your temperature regularly",
                "Stay hydrated"
            ],
            "disclaimers": [
                "This information is for educational purposes only",
                "Always consult with a healthcare provider for medical concerns"
            ],
            "sources": ["MedlinePlus (U.S. National Library of Medicine)"],
            "processing_time_ms": 150.5,
            "metadata": {
                "query_type": "symptom_inquiry",
                "symptoms_addressed": ["fever", "headache"],
                "documents_used": 3
            }
        },
        {
            "response_text": "🚨 MEDICAL EMERGENCY DETECTED 🚨\n\nThe symptoms 'unconscious, high fever' may indicate a serious medical emergency.\n\nIMMEDIATE ACTION REQUIRED:\n• Go to the nearest hospital immediately\n• Call emergency services (dial 108 in India)\n• Do not delay seeking medical care",
            "response_type": "emergency_alert",
            "confidence": 0.95,
            "emergency_alert": True,
            "symptoms": ["unconscious", "high fever"],
            "recommendations": [
                "Seek immediate emergency medical care",
                "Do not delay treatment",
                "Call emergency services if available"
            ],
            "disclaimers": [
                "⚠️ EMERGENCY: These symptoms may indicate a serious condition",
                "This information is for educational purposes only"
            ],
            "sources": ["World Health Organization"],
            "processing_time_ms": 89.2,
            "metadata": {
                "query_type": "emergency",
                "emergency_indicators": ["unconscious", "high fever"],
                "documents_used": 2
            }
        }
    ]
    
    for i, resp_data in enumerate(sample_responses, 1):
        try:
            response = MedicalQueryResponse(**resp_data)
            print(f"   ✅ Response {i}: {response.response_type} (confidence: {response.confidence:.2f})")
            if response.emergency_alert:
                print(f"      🚨 EMERGENCY: {len(response.symptoms)} symptoms detected")
            else:
                print(f"      📋 Symptoms: {', '.join(response.symptoms)}")
            print(f"      💡 Recommendations: {len(response.recommendations)} provided")
        except Exception as e:
            print(f"   ❌ Response {i} failed: {e}")
    
    print("\n3. 🔍 Health Check Response:")
    
    health_responses = [
        {
            "status": "healthy",
            "service_status": {
                "medical_service": "operational",
                "api": "operational",
                "vector_store": "operational"
            }
        },
        {
            "status": "unhealthy", 
            "service_status": {
                "medical_service": "error",
                "api": "operational",
                "vector_store": "degraded"
            }
        }
    ]
    
    for i, health_data in enumerate(health_responses, 1):
        try:
            health = HealthCheckResponse(**health_data)
            print(f"   ✅ Health {i}: {health.status} at {health.timestamp}")
            operational_services = sum(1 for status in health.service_status.values() if status == "operational")
            print(f"      📊 {operational_services}/{len(health.service_status)} services operational")
        except Exception as e:
            print(f"   ❌ Health response {i} failed: {e}")

def demo_api_endpoints():
    """Demonstrate what the API endpoints would do."""
    print("\n4. 🌐 API Endpoints Overview:")
    
    endpoints = [
        {
            "method": "GET",
            "path": "/",
            "description": "Root endpoint with API information",
            "example_response": {
                "name": "Medical RAG System API",
                "version": "1.0.0",
                "description": "AI-powered medical information system for rural healthcare",
                "docs": "/docs"
            }
        },
        {
            "method": "GET", 
            "path": "/health",
            "description": "Health check endpoint",
            "example_response": {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service_status": {
                    "medical_service": "operational",
                    "api": "operational"
                }
            }
        },
        {
            "method": "POST",
            "path": "/query",
            "description": "Process medical queries",
            "example_request": {
                "query": "I have fever and headache",
                "language": "english",
                "include_sources": True,
                "max_results": 5
            },
            "example_response": {
                "response_text": "Medical guidance about fever and headache...",
                "response_type": "symptom_guidance",
                "confidence": 0.85,
                "emergency_alert": False,
                "symptoms": ["fever", "headache"]
            }
        },
        {
            "method": "POST",
            "path": "/emergency-check", 
            "description": "Quick emergency detection",
            "example_request": {
                "query": "Patient unconscious"
            },
            "example_response": {
                "emergency_detected": True,
                "emergency_indicators": ["unconscious"],
                "confidence": 0.95,
                "recommendations": ["Seek immediate medical attention"]
            }
        },
        {
            "method": "GET",
            "path": "/symptoms/extract",
            "description": "Extract symptoms from text",
            "example_params": {
                "query": "I have fever, chills and body aches"
            },
            "example_response": {
                "symptoms": ["fever", "chills", "body aches"],
                "query": "I have fever, chills and body aches"
            }
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n   {endpoint['method']} {endpoint['path']}")
        print(f"   📖 {endpoint['description']}")
        
        if 'example_request' in endpoint:
            print(f"   📥 Request: {json.dumps(endpoint['example_request'], indent=6)}")
        elif 'example_params' in endpoint:
            print(f"   📥 Params: {json.dumps(endpoint['example_params'], indent=6)}")
            
        if 'example_response' in endpoint:
            response_preview = str(endpoint['example_response'])
            if len(response_preview) > 100:
                response_preview = response_preview[:100] + "..."
            print(f"   📤 Response: {response_preview}")

def demo_usage_scenarios():
    """Demonstrate typical usage scenarios."""
    print("\n5. 🎯 Usage Scenarios:")
    
    scenarios = [
        {
            "name": "Rural Health Worker Query",
            "description": "Health worker asks about patient symptoms",
            "query": "Patient has fever, chills, and severe headache for 3 days",
            "expected_flow": [
                "1. Query processed and symptoms extracted: fever, chills, headache",
                "2. Emergency detection: No immediate emergency",
                "3. Medical documents retrieved about malaria symptoms",
                "4. Response generated with medical guidance",
                "5. Disclaimers added with recommendation to see healthcare provider"
            ]
        },
        {
            "name": "Emergency Situation",
            "description": "Patient with severe symptoms needs immediate care",
            "query": "Patient unconscious with high fever and vomiting",
            "expected_flow": [
                "1. Emergency detection triggers immediately",
                "2. Emergency indicators identified: unconscious, high fever",
                "3. Emergency response template activated",
                "4. Immediate action recommendations provided",
                "5. Emergency disclaimers and warnings added"
            ]
        },
        {
            "name": "Hindi Language Query",
            "description": "Local patient asks in Hindi",
            "query": "मुझे तेज बुखार और सिर दर्द है",
            "expected_flow": [
                "1. Language detected as Hindi",
                "2. Hindi symptoms translated: fever, headache", 
                "3. English medical documents retrieved",
                "4. Response generated in appropriate format",
                "5. Medical guidance provided with cultural context"
            ]
        },
        {
            "name": "Prevention Inquiry",
            "description": "Community member asks about prevention",
            "query": "How can I prevent malaria in my village?",
            "expected_flow": [
                "1. Query classified as prevention inquiry",
                "2. Prevention-related documents retrieved",
                "3. Practical prevention advice generated",
                "4. Community-level recommendations provided",
                "5. Sources attributed for credibility"
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n   Scenario {i}: {scenario['name']}")
        print(f"   📝 {scenario['description']}")
        print(f"   💬 Query: \"{scenario['query']}\"")
        print(f"   🔄 Expected Flow:")
        for step in scenario['expected_flow']:
            print(f"      {step}")

def main():
    """Run the complete demo."""
    try:
        demo_request_response_models()
        demo_api_endpoints()
        demo_usage_scenarios()
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\n📚 Next Steps:")
        print("   • Run 'python3 run_api.py' to start the server")
        print("   • Visit http://localhost:8000/docs for interactive API docs")
        print("   • Use 'python3 examples/api_client_example.py' to test endpoints")
        print("   • Check http://localhost:8000/health for service status")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()