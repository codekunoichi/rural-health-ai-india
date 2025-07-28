import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from src.data_collection.medlineplus_api import MedlinePlusAPI
from src.data_collection.data_processor import DataProcessor

class TestMedlinePlusAPI:
    """Test cases for MedlinePlus API client following TDD approach."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client instance for testing."""
        return MedlinePlusAPI()
    
    @pytest.fixture
    def mock_malaria_response(self):
        """Mock response for malaria search query."""
        return {
            "nlmSearchResult": {
                "list": {
                    "document": [
                        {
                            "content": {
                                "title": "Malaria",
                                "summary": "Malaria is a serious disease caused by parasites spread by mosquitoes.",
                                "url": "https://medlineplus.gov/malaria.html",
                                "date": "2023-12-01"
                            }
                        },
                        {
                            "content": {
                                "title": "Malaria Symptoms",
                                "summary": "Malaria symptoms include fever, chills, and headache.",
                                "url": "https://medlineplus.gov/malaria-symptoms.html",
                                "date": "2023-11-15"
                            }
                        }
                    ]
                },
                "count": 2
            }
        }
    
    def test_api_client_initialization(self, api_client):
        """Test that API client initializes with correct base URL."""
        assert api_client.base_url == "https://wsearch.nlm.nih.gov/ws/query"
        assert api_client.max_retries == 3
        assert api_client.timeout == 30
    
    def test_search_malaria_success(self, api_client, mock_malaria_response):
        """Test successful malaria information retrieval."""
        # Red: Write failing test first
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
<nlmSearchResult>
  <list>
    <document>
      <content>
        <title>Malaria</title>
        <summary>Malaria is a serious disease caused by parasites spread by mosquitoes.</summary>
        <url>https://medlineplus.gov/malaria.html</url>
        <date>2023-12-01</date>
      </content>
    </document>
    <document>
      <content>
        <title>Malaria Symptoms</title>
        <summary>Malaria symptoms include fever, chills, and headache.</summary>
        <url>https://medlineplus.gov/malaria-symptoms.html</url>
        <date>2023-11-15</date>
      </content>
    </document>
  </list>
  <count>2</count>
</nlmSearchResult>"""
        mock_response.raise_for_status.return_value = None
        
        # Mock the session.get method
        with patch.object(api_client.session, 'get', return_value=mock_response) as mock_session_get:
            result = api_client.search_medical_topic("malaria")
        
            # Assertions for expected behavior
            assert result is not None
            assert len(result) == 2
            assert result[0]["title"] == "Malaria"
            assert "fever" in result[1]["summary"].lower()
            
            # Verify API was called correctly
            mock_session_get.assert_called_once()
            call_args = mock_session_get.call_args
            assert "malaria" in call_args[1]["params"]["term"]
    
    @patch('src.data_collection.medlineplus_api.requests.get')
    def test_search_with_network_error(self, mock_get, api_client):
        """Test handling of network errors with retry logic."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        with pytest.raises(requests.exceptions.ConnectionError):
            api_client.search_medical_topic("malaria")
        
        # Should retry 3 times
        assert mock_get.call_count == 3
    
    @patch('src.data_collection.medlineplus_api.requests.get')
    def test_search_with_http_error(self, mock_get, api_client):
        """Test handling of HTTP errors (404, 500, etc.)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.exceptions.HTTPError):
            api_client.search_medical_topic("invalid_topic")
    
    @patch('src.data_collection.medlineplus_api.requests.get')
    def test_search_empty_results(self, mock_get, api_client):
        """Test handling of empty search results."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
<nlmSearchResult>
  <list></list>
  <count>0</count>
</nlmSearchResult>"""
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = api_client.search_medical_topic("nonexistent_disease")
        
        assert result == []
    
    def test_validate_search_term_valid(self, api_client):
        """Test validation of valid search terms."""
        valid_terms = ["malaria", "fever symptoms", "headache treatment"]
        
        for term in valid_terms:
            assert api_client._validate_search_term(term) == True
    
    def test_validate_search_term_invalid(self, api_client):
        """Test validation rejects invalid search terms."""
        invalid_terms = ["", "   ", "a", "x" * 101]  # empty, whitespace, too short, too long
        
        for term in invalid_terms:
            assert api_client._validate_search_term(term) == False
    
    @patch('src.data_collection.medlineplus_api.requests.get')
    def test_search_malaria_specific_fields(self, mock_get, api_client, mock_malaria_response):
        """Test that malaria search returns required fields."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
<nlmSearchResult>
  <list>
    <document>
      <content>
        <title>Malaria</title>
        <summary>Malaria is a serious disease caused by parasites spread by mosquitoes.</summary>
        <url>https://medlineplus.gov/malaria.html</url>
        <date>2023-12-01</date>
      </content>
    </document>
  </list>
  <count>1</count>
</nlmSearchResult>"""
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = api_client.search_medical_topic("malaria")
        
        # Each result should have required fields
        for doc in result:
            assert "title" in doc
            assert "summary" in doc
            assert "url" in doc
            assert "date" in doc
            assert "source" in doc
            assert doc["source"] == "medlineplus"

class TestDataProcessor:
    """Test cases for medical data processing following TDD approach."""
    
    @pytest.fixture
    def processor(self):
        """Create data processor instance for testing."""
        return DataProcessor()
    
    @pytest.fixture
    def sample_medical_text(self):
        """Sample medical text for processing tests."""
        return """
        Malaria is a serious disease caused by parasites that are spread to people 
        through the bites of infected Anopheles mosquitoes. Symptoms of malaria include:
        - Fever and chills
        - Headache
        - Muscle aches and tiredness
        - Nausea and vomiting
        
        Emergency symptoms that require immediate medical attention:
        - High fever (above 104°F/40°C)
        - Confusion or seizures
        - Difficulty breathing
        - Severe vomiting
        """
    
    def test_processor_initialization(self, processor):
        """Test that processor initializes correctly."""
        assert processor.chunk_size == 512
        assert processor.chunk_overlap == 50
        assert hasattr(processor, 'emergency_keywords')
    
    def test_clean_text_basic(self, processor):
        """Test basic text cleaning functionality."""
        dirty_text = "  This is a test.   \n\n  Extra   spaces.  \t"
        cleaned = processor.clean_text(dirty_text)
        
        assert cleaned == "This is a test. Extra spaces."
        assert "\n" not in cleaned
        assert "\t" not in cleaned
    
    def test_extract_symptoms_from_text(self, processor, sample_medical_text):
        """Test symptom extraction from medical text."""
        symptoms = processor.extract_symptoms(sample_medical_text)
        
        # Should find common malaria symptoms
        expected_symptoms = ["fever", "chills", "headache", "muscle aches", "nausea", "vomiting"]
        
        for symptom in expected_symptoms:
            assert any(symptom in s.lower() for s in symptoms), f"Should find symptom: {symptom}"
    
    def test_detect_emergency_indicators(self, processor, sample_medical_text):
        """Test detection of emergency symptoms in text."""
        emergency_indicators = processor.detect_emergency_indicators(sample_medical_text)
        
        # Should detect emergency symptoms
        expected_emergency = ["high fever", "confusion", "seizures", "difficulty breathing", "severe vomiting"]
        
        assert len(emergency_indicators) > 0
        for indicator in expected_emergency:
            assert any(indicator in e.lower() for e in emergency_indicators), f"Should detect: {indicator}"
    
    def test_chunk_text_proper_size(self, processor, sample_medical_text):
        """Test text chunking produces properly sized chunks."""
        chunks = processor.chunk_text(sample_medical_text)
        
        assert len(chunks) > 0
        for chunk in chunks:
            assert len(chunk) <= processor.chunk_size
            assert len(chunk.strip()) > 0  # No empty chunks
    
    def test_chunk_text_with_overlap(self, processor):
        """Test that text chunking maintains overlap between chunks."""
        long_text = "This is sentence one. " * 50  # Create long text
        chunks = processor.chunk_text(long_text)
        
        if len(chunks) > 1:
            # Check overlap between consecutive chunks
            overlap_found = False
            for i in range(len(chunks) - 1):
                current_chunk = chunks[i]
                next_chunk = chunks[i + 1]
                
                # Look for common words at the end of current and start of next
                current_words = current_chunk.split()[-10:]  # Last 10 words
                next_words = next_chunk.split()[:10]  # First 10 words
                
                common_words = set(current_words) & set(next_words)
                if common_words:
                    overlap_found = True
                    break
            
            assert overlap_found, "Should maintain overlap between chunks"
    
    def test_process_medical_document(self, processor):
        """Test complete document processing pipeline."""
        raw_document = {
            "title": "Malaria Information",
            "content": "  Malaria causes fever and chills. Emergency: high fever requires immediate care.  ",
            "url": "https://example.com/malaria",
            "date": "2023-12-01"
        }
        
        processed = processor.process_document(raw_document)
        
        # Check processed document structure
        assert "title" in processed
        assert "content" in processed
        assert "metadata" in processed
        assert "symptoms" in processed
        assert "emergency_indicators" in processed
        assert "chunks" in processed
        
        # Check content is cleaned
        assert processed["content"].strip()
        assert "  " not in processed["content"]  # Extra spaces removed
        
        # Check metadata
        assert processed["metadata"]["source_url"] == raw_document["url"]
        assert processed["metadata"]["date"] == raw_document["date"]
        
        # Check symptoms and emergency indicators extracted
        assert len(processed["symptoms"]) > 0
        assert len(processed["emergency_indicators"]) > 0
        assert len(processed["chunks"]) > 0