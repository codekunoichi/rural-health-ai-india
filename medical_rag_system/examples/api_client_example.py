"""
Example client for testing the Medical RAG System FastAPI endpoints.
Demonstrates how to interact with the API programmatically.
"""

import requests
import json
import time
from typing import Dict, Any

class MedicalRAGClient:
    """Client for interacting with Medical RAG System API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client with the API base URL."""
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API is healthy."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get detailed system status."""
        try:
            response = self.session.get(f"{self.base_url}/status")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def query_medical(self, query: str, language: str = "auto", 
                     include_sources: bool = True, max_results: int = 5) -> Dict[str, Any]:
        """Send a medical query to the API."""
        try:
            payload = {
                "query": query,
                "language": language,
                "include_sources": include_sources,
                "max_results": max_results
            }
            
            response = self.session.post(
                f"{self.base_url}/query",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def check_emergency(self, query: str) -> Dict[str, Any]:
        """Check if a query indicates a medical emergency."""
        try:
            payload = {"query": query}
            response = self.session.post(
                f"{self.base_url}/emergency-check",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def extract_symptoms(self, query: str) -> Dict[str, Any]:
        """Extract symptoms from a medical query."""
        try:
            response = self.session.get(
                f"{self.base_url}/symptoms/extract",
                params={"query": query}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

def demo_api_usage():
    """Demonstrate API usage with example queries."""
    print("🏥 Medical RAG System API Client Demo")
    print("=" * 50)
    
    # Initialize client
    client = MedicalRAGClient()
    
    # Test health check
    print("\n1. Health Check:")
    health = client.health_check()
    print(f"   Status: {health.get('status', 'unknown')}")
    
    if health.get('status') != 'healthy':
        print("❌ API is not healthy. Please check the server.")
        return
    
    # Test system status
    print("\n2. System Status:")
    status = client.get_system_status()
    if 'error' not in status:
        print(f"   System: {status.get('system_status', 'unknown')}")
        components = status.get('components', {})
        for comp, info in components.items():
            print(f"   {comp}: {info.get('status', 'unknown')}")
    
    # Test medical queries
    test_queries = [
        "I have fever and headache for 2 days",
        "Patient unconscious with high fever",
        "मुझे बुखार और सिर दर्द है",  # Hindi query
        "What are the symptoms of malaria?",
        "How to prevent mosquito bites?"
    ]
    
    print("\n3. Medical Query Processing:")
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Query {i}: '{query}'")
        
        # Process the query
        result = client.query_medical(query)
        
        if 'error' in result:
            print(f"   ❌ Error: {result['error']}")
            continue
        
        print(f"   Response Type: {result.get('response_type', 'unknown')}")
        print(f"   Confidence: {result.get('confidence', 0):.2f}")
        print(f"   Emergency: {'🚨 YES' if result.get('emergency_alert') else '✅ No'}")
        
        if result.get('symptoms'):
            print(f"   Symptoms: {', '.join(result['symptoms'])}")
        
        response_text = result.get('response_text', '')
        if len(response_text) > 100:
            response_text = response_text[:100] + "..."
        print(f"   Response: {response_text}")
        
        time.sleep(0.5)  # Brief pause between requests
    
    # Test emergency detection
    print("\n4. Emergency Detection:")
    emergency_queries = [
        "Patient unconscious",
        "Having seizures", 
        "I have mild headache"
    ]
    
    for query in emergency_queries:
        result = client.check_emergency(query)
        if 'error' not in result:
            emergency = result.get('emergency_detected', False)
            indicators = result.get('emergency_indicators', [])
            print(f"   '{query}' -> {'🚨 EMERGENCY' if emergency else '✅ Normal'}")
            if indicators:
                print(f"      Indicators: {', '.join(indicators)}")
    
    # Test symptom extraction
    print("\n5. Symptom Extraction:")
    symptom_queries = [
        "I have fever, chills, and body aches",
        "Patient experiencing nausea and vomiting"
    ]
    
    for query in symptom_queries:
        result = client.extract_symptoms(query)
        if 'error' not in result:
            symptoms = result.get('symptoms', [])
            print(f"   '{query}' -> {symptoms}")
    
    print("\n✅ Demo completed!")

def interactive_mode():
    """Interactive mode for testing queries."""
    print("\n🔄 Interactive Mode - Enter your medical queries:")
    print("Type 'quit' to exit, 'help' for commands")
    
    client = MedicalRAGClient()
    
    # Check if API is available
    health = client.health_check()
    if health.get('status') != 'healthy':
        print("❌ API is not available. Please start the server first.")
        return
    
    while True:
        try:
            query = input("\n💬 Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
            elif query.lower() == 'help':
                print("Commands:")
                print("  - Enter any medical query for full processing")
                print("  - 'emergency: <query>' for emergency check only")
                print("  - 'symptoms: <query>' for symptom extraction only")
                print("  - 'quit' to exit")
                continue
            elif not query:
                continue
            
            # Handle special commands
            if query.startswith('emergency:'):
                result = client.check_emergency(query[10:].strip())
                if 'error' not in result:
                    emergency = result.get('emergency_detected', False)
                    print(f"🚨 Emergency: {'YES' if emergency else 'NO'}")
                    if result.get('emergency_indicators'):
                        print(f"   Indicators: {', '.join(result['emergency_indicators'])}")
                else:
                    print(f"❌ Error: {result['error']}")
                continue
            
            elif query.startswith('symptoms:'):
                result = client.extract_symptoms(query[9:].strip())
                if 'error' not in result:
                    symptoms = result.get('symptoms', [])
                    print(f"🔍 Symptoms: {symptoms}")
                else:
                    print(f"❌ Error: {result['error']}")
                continue
            
            # Full query processing
            result = client.query_medical(query)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            print(f"\n📋 Response Type: {result.get('response_type', 'unknown')}")
            print(f"🎯 Confidence: {result.get('confidence', 0):.2f}")
            print(f"🚨 Emergency: {'YES' if result.get('emergency_alert') else 'NO'}")
            
            if result.get('symptoms'):
                print(f"🔍 Symptoms: {', '.join(result['symptoms'])}")
            
            print(f"\n💊 Medical Response:")
            print(f"   {result.get('response_text', 'No response generated')}")
            
            if result.get('recommendations'):
                print(f"\n📝 Recommendations:")
                for rec in result['recommendations']:
                    print(f"   • {rec}")
            
            if result.get('processing_time_ms'):
                print(f"\n⏱️  Processing time: {result['processing_time_ms']:.1f}ms")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        demo_api_usage()
        
        # Ask if user wants interactive mode
        try:
            response = input("\n🔄 Would you like to try interactive mode? (y/n): ").lower()
            if response in ['y', 'yes']:
                interactive_mode()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")