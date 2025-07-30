import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from typing import List, Dict, Any

from src.rag_system.query_processor import MedicalQueryProcessor
from src.rag_system.retrieval_engine import MedicalRetrievalEngine
from src.rag_system.response_generator import MedicalResponseGenerator

class TestMedicalQueryProcessor:
    """Test cases for medical query processing following TDD approach."""
    
    @pytest.fixture
    def query_processor(self):
        """Create query processor instance for testing."""
        return MedicalQueryProcessor()
    
    @pytest.fixture
    def sample_queries(self):
        """Sample medical queries for testing."""
        return {
            'basic_symptoms': "I have fever and headache for 2 days",
            'emergency': "Patient unconscious with high fever",
            'multiple_symptoms': "Fever, chills, sweating, weakness since 5 days", 
            'hindi_query': "मुझे बुखार और सिर दर्द है",
            'vague_query': "not feeling well",
            'non_medical': "What's the weather like today?"
        }
    
    def test_processor_initialization(self, query_processor):
        """Test that query processor initializes correctly."""
        assert query_processor is not None
        assert hasattr(query_processor, 'process_query')
        assert hasattr(query_processor, 'extract_symptoms')
        assert hasattr(query_processor, 'detect_emergency_intent')
        assert hasattr(query_processor, 'classify_query_type')
    
    def test_extract_symptoms_from_query(self, query_processor, sample_queries):
        """Test symptom extraction from user queries."""
        # Basic symptoms
        symptoms = query_processor.extract_symptoms(sample_queries['basic_symptoms'])
        assert 'fever' in symptoms
        assert 'headache' in symptoms
        
        # Multiple symptoms
        symptoms = query_processor.extract_symptoms(sample_queries['multiple_symptoms'])
        expected_symptoms = ['fever', 'chills', 'sweating', 'weakness']
        for symptom in expected_symptoms:
            assert any(symptom in s.lower() for s in symptoms)
    
    def test_extract_symptoms_hindi(self, query_processor, sample_queries):
        """Test symptom extraction from Hindi queries."""
        symptoms = query_processor.extract_symptoms(sample_queries['hindi_query'])
        
        # Should translate Hindi to English symptoms
        assert 'fever' in [s.lower() for s in symptoms]
        assert 'headache' in [s.lower() for s in symptoms]
    
    def test_detect_emergency_intent(self, query_processor, sample_queries):
        """Test detection of emergency medical situations."""
        # Emergency case
        is_emergency, emergency_indicators = query_processor.detect_emergency_intent(
            sample_queries['emergency']
        )
        assert is_emergency == True
        assert len(emergency_indicators) > 0
        assert any('unconscious' in indicator.lower() for indicator in emergency_indicators)
        
        # Non-emergency case
        is_emergency, emergency_indicators = query_processor.detect_emergency_intent(
            sample_queries['basic_symptoms']
        )
        assert is_emergency == False
    
    def test_classify_query_type(self, query_processor, sample_queries):
        """Test classification of different query types."""
        # Medical symptom query
        query_type = query_processor.classify_query_type(sample_queries['basic_symptoms'])
        assert query_type in ['symptom_inquiry', 'medical_question']
        
        # Emergency query
        query_type = query_processor.classify_query_type(sample_queries['emergency'])
        assert query_type == 'emergency'
        
        # Non-medical query
        query_type = query_processor.classify_query_type(sample_queries['non_medical'])
        assert query_type == 'non_medical'
    
    def test_process_query_complete_pipeline(self, query_processor, sample_queries):
        """Test complete query processing pipeline."""
        result = query_processor.process_query(sample_queries['basic_symptoms'])
        
        # Should return structured query analysis
        assert 'original_query' in result
        assert 'processed_query' in result
        assert 'symptoms' in result
        assert 'query_type' in result
        assert 'emergency_detected' in result
        assert 'confidence' in result
        assert 'metadata' in result
        
        # Verify processing quality
        assert result['symptoms']  # Should extract symptoms
        assert result['confidence'] > 0.0  # Should have confidence score
        assert result['query_type'] in ['symptom_inquiry', 'emergency', 'medical_question', 'non_medical']
    
    def test_process_emergency_query(self, query_processor, sample_queries):
        """Test processing of emergency medical queries."""
        result = query_processor.process_query(sample_queries['emergency'])
        
        assert result['emergency_detected'] == True
        assert result['query_type'] == 'emergency'
        assert len(result['emergency_indicators']) > 0
        assert result['confidence'] > 0.8  # High confidence for clear emergency
    
    def test_query_normalization(self, query_processor):
        """Test query text normalization."""
        messy_query = "  I HAVE   fever,, chills!!! And headache???  "
        result = query_processor.process_query(messy_query)
        
        # Should normalize the query
        normalized = result['processed_query']
        assert normalized != messy_query
        assert 'fever' in normalized.lower()
        assert 'chills' in normalized.lower()
        assert '!!!' not in normalized
        assert '???' not in normalized
    
    def test_medical_context_enhancement(self, query_processor):
        """Test enhancement of queries with medical context."""
        basic_query = "fever for 3 days"
        result = query_processor.process_query(basic_query)
        
        # Should add medical context
        metadata = result['metadata']
        assert 'duration' in metadata  # Should extract "3 days"
        assert 'severity_indicators' in metadata
        assert 'medical_keywords' in metadata

class TestMedicalRetrievalEngine:
    """Test cases for medical retrieval engine following TDD approach."""
    
    @pytest.fixture
    def retrieval_engine(self):
        """Create retrieval engine instance for testing."""
        with patch('src.knowledge_base.vector_store.MedicalVectorStore') as mock_store_class:
            mock_store_instance = Mock()
            mock_store_instance.search = Mock()
            mock_store_class.return_value = mock_store_instance
            engine = MedicalRetrievalEngine()
            engine.vector_store = mock_store_instance  # Explicitly set the mock
            return engine
    
    @pytest.fixture
    def sample_processed_query(self):
        """Sample processed query for testing."""
        return {
            'original_query': 'I have fever and headache',
            'processed_query': 'fever and headache symptoms',
            'symptoms': ['fever', 'headache'],
            'query_type': 'symptom_inquiry',
            'emergency_detected': False,
            'confidence': 0.85,
            'metadata': {
                'duration': None,
                'severity_indicators': [],
                'medical_keywords': ['fever', 'headache']
            }
        }
    
    @pytest.fixture
    def sample_search_results(self):
        """Sample search results from vector store."""
        return [
            {
                'document': {
                    'id': 'doc_1',
                    'content': 'Malaria symptoms include fever, chills, and headache. Early treatment is important.',
                    'metadata': {
                        'source': 'medlineplus',
                        'symptoms': ['fever', 'chills', 'headache'],
                        'section_type': 'symptoms'
                    }
                },
                'score': 0.92,
                'relevance_explanation': 'High semantic similarity; Contains emergency medical information'
            },
            {
                'document': {
                    'id': 'doc_2', 
                    'content': 'High fever requires immediate medical attention and may indicate serious infection.',
                    'metadata': {
                        'source': 'who',
                        'emergency_indicators': ['high fever'],
                        'section_type': 'emergency'
                    }
                },
                'score': 0.78,
                'relevance_explanation': 'Good semantic match; Focuses on symptom information'
            }
        ]
    
    def test_engine_initialization(self, retrieval_engine):
        """Test that retrieval engine initializes correctly."""
        assert retrieval_engine is not None
        assert hasattr(retrieval_engine, 'retrieve_relevant_documents')
        assert hasattr(retrieval_engine, 'rank_by_medical_relevance')
        assert hasattr(retrieval_engine, 'filter_by_context')
    
    def test_retrieve_relevant_documents(self, retrieval_engine, sample_processed_query, sample_search_results):
        """Test document retrieval based on processed query."""
        # Mock vector store search
        retrieval_engine.vector_store.search.return_value = sample_search_results
        
        results = retrieval_engine.retrieve_relevant_documents(
            sample_processed_query, 
            top_k=5
        )
        
        # Should return relevant documents
        assert len(results) > 0
        assert 'documents' in results
        assert 'retrieval_metadata' in results
        
        # Should call vector store with appropriate parameters
        retrieval_engine.vector_store.search.assert_called_once()
        call_args, call_kwargs = retrieval_engine.vector_store.search.call_args
        # Check if query was passed as first positional argument or as keyword argument
        if call_args:
            assert call_args[0] == sample_processed_query['processed_query']  # Query
        else:
            assert call_kwargs['query'] == sample_processed_query['processed_query']
        # Top k might be in kwargs
        if 'top_k' in call_kwargs:
            assert call_kwargs['top_k'] == 5
    
    def test_emergency_query_retrieval(self, retrieval_engine):
        """Test retrieval behavior for emergency queries."""
        emergency_query = {
            'processed_query': 'unconscious high fever emergency',
            'query_type': 'emergency',
            'emergency_detected': True,
            'symptoms': ['unconscious', 'high fever'],
            'emergency_indicators': ['unconscious', 'high fever']
        }
        
        # Mock emergency-focused results
        emergency_results = [
            {
                'document': {
                    'content': 'Unconsciousness requires immediate emergency care.',
                    'metadata': {'section_type': 'emergency'}
                },
                'score': 0.95
            }
        ]
        retrieval_engine.vector_store.search.return_value = emergency_results
        
        results = retrieval_engine.retrieve_relevant_documents(emergency_query)
        
        # Should prioritize emergency context
        call_args, call_kwargs = retrieval_engine.vector_store.search.call_args
        assert call_kwargs.get('medical_context') == 'emergency'
    
    def test_rank_by_medical_relevance(self, retrieval_engine, sample_search_results):
        """Test ranking of documents by medical relevance."""
        ranked_results = retrieval_engine.rank_by_medical_relevance(
            sample_search_results,
            query_symptoms=['fever', 'headache']
        )
        
        # Should return ranked documents
        assert len(ranked_results) == len(sample_search_results)
        
        # Should be ordered by relevance (highest first)
        scores = [doc['final_score'] for doc in ranked_results]
        assert scores == sorted(scores, reverse=True)
    
    def test_filter_by_context(self, retrieval_engine, sample_search_results):
        """Test filtering documents by medical context."""
        # Filter for symptom-related documents
        filtered = retrieval_engine.filter_by_context(
            sample_search_results,
            context_type='symptoms'
        )
        
        # Should only return symptom-related documents
        for result in filtered:
            doc_metadata = result['document']['metadata']
            assert (doc_metadata.get('section_type') == 'symptoms' or 
                   len(doc_metadata.get('symptoms', [])) > 0)
    
    def test_retrieval_with_insufficient_results(self, retrieval_engine, sample_processed_query):
        """Test handling when vector store returns insufficient results."""
        # Mock empty results
        retrieval_engine.vector_store.search.return_value = []
        
        results = retrieval_engine.retrieve_relevant_documents(sample_processed_query)
        
        # Should handle gracefully
        assert 'documents' in results
        assert results['documents'] == []
        assert 'retrieval_metadata' in results
        assert results['retrieval_metadata']['total_found'] == 0
    
    def test_multilingual_retrieval(self, retrieval_engine):
        """Test retrieval for Hindi/multilingual queries."""
        hindi_query = {
            'processed_query': 'बुखार सिर दर्द fever headache',
            'symptoms': ['fever', 'headache'],
            'query_type': 'symptom_inquiry',
            'metadata': {'language': 'mixed'}
        }
        
        # Mock results
        retrieval_engine.vector_store.search.return_value = []
        
        results = retrieval_engine.retrieve_relevant_documents(hindi_query)
        
        # Should handle multilingual queries
        assert 'documents' in results
        retrieval_engine.vector_store.search.assert_called_once()

class TestMedicalResponseGenerator:
    """Test cases for medical response generation following TDD approach."""
    
    @pytest.fixture
    def response_generator(self):
        """Create response generator instance for testing."""
        return MedicalResponseGenerator()
    
    @pytest.fixture
    def sample_retrieval_context(self):
        """Sample retrieval context for response generation."""
        return {
            'query': {
                'original_query': 'I have fever and headache for 2 days',
                'symptoms': ['fever', 'headache'],
                'query_type': 'symptom_inquiry',
                'emergency_detected': False
            },
            'documents': [
                {
                    'document': {
                        'content': 'Fever and headache are common symptoms of malaria. Seek medical attention if symptoms persist.',
                        'metadata': {
                            'source': 'medlineplus',
                            'symptoms': ['fever', 'headache'],
                            'section_type': 'symptoms'
                        }
                    },
                    'final_score': 0.92
                }
            ],
            'retrieval_metadata': {
                'total_found': 1,
                'confidence': 0.85
            }
        }
    
    @pytest.fixture 
    def emergency_context(self):
        """Emergency situation context for testing."""
        return {
            'query': {
                'original_query': 'Patient unconscious with high fever',
                'symptoms': ['unconscious', 'high fever'],
                'query_type': 'emergency',
                'emergency_detected': True,
                'emergency_indicators': ['unconscious', 'high fever']
            },
            'documents': [
                {
                    'document': {
                        'content': 'Unconsciousness with fever is a medical emergency requiring immediate hospital care.',
                        'metadata': {
                            'section_type': 'emergency',
                            'emergency_indicators': ['unconscious']
                        }
                    },
                    'final_score': 0.98
                }
            ]
        }
    
    def test_generator_initialization(self, response_generator):
        """Test that response generator initializes correctly."""
        assert response_generator is not None
        assert hasattr(response_generator, 'generate_response')
        assert hasattr(response_generator, 'generate_emergency_response')
        assert hasattr(response_generator, 'generate_symptom_response')
        assert hasattr(response_generator, 'add_medical_disclaimers')
    
    def test_generate_symptom_response(self, response_generator, sample_retrieval_context):
        """Test generation of symptom-based medical responses."""
        response = response_generator.generate_response(sample_retrieval_context)
        
        # Should generate structured response
        assert 'response_text' in response
        assert 'response_type' in response
        assert 'confidence' in response
        assert 'sources' in response
        assert 'disclaimers' in response
        assert 'recommendations' in response
        
        # Content quality checks
        assert 'fever' in response['response_text'].lower()
        assert 'headache' in response['response_text'].lower()
        assert len(response['response_text']) > 50  # Substantial response
        assert response['response_type'] == 'symptom_guidance'
    
    def test_generate_emergency_response(self, response_generator, emergency_context):
        """Test generation of emergency medical responses."""
        response = response_generator.generate_response(emergency_context)
        
        # Emergency response characteristics
        assert response['response_type'] == 'emergency_alert'
        assert response['emergency_alert'] == True
        assert 'immediate' in response['response_text'].lower()
        assert 'emergency' in response['response_text'].lower()
        
        # Should have reasonable confidence for clear emergency
        assert response['confidence'] > 0.2
        
        # Should include emergency actions
        assert 'recommendations' in response
        recommendations = response['recommendations']
        assert any('hospital' in rec.lower() or 'emergency' in rec.lower() 
                  for rec in recommendations)
    
    def test_add_medical_disclaimers(self, response_generator, sample_retrieval_context):
        """Test addition of appropriate medical disclaimers."""
        response = response_generator.generate_response(sample_retrieval_context)
        
        disclaimers = response['disclaimers']
        assert len(disclaimers) > 0
        
        # Should include standard medical disclaimer
        general_disclaimer = any('not replace professional medical advice' in d.lower() 
                               for d in disclaimers)
        assert general_disclaimer
    
    def test_source_attribution(self, response_generator, sample_retrieval_context):
        """Test proper attribution of medical sources."""
        response = response_generator.generate_response(sample_retrieval_context)
        
        sources = response['sources']
        assert len(sources) > 0
        assert any('medlineplus' in s.lower() for s in sources)
    
    def test_response_with_no_relevant_documents(self, response_generator):
        """Test response generation when no relevant documents found."""
        empty_context = {
            'query': {
                'original_query': 'random non-medical question',
                'query_type': 'non_medical'
            },
            'documents': [],
            'retrieval_metadata': {'total_found': 0}
        }
        
        response = response_generator.generate_response(empty_context)
        
        # Should handle gracefully
        assert response['response_type'] == 'insufficient_information'
        assert 'unable to provide' in response['response_text'].lower()
        assert len(response['disclaimers']) > 0
    
    def test_confidence_scoring(self, response_generator, sample_retrieval_context):
        """Test confidence scoring in generated responses."""
        response = response_generator.generate_response(sample_retrieval_context)
        
        confidence = response['confidence']
        assert 0.0 <= confidence <= 1.0
        
        # Good retrieval confidence should lead to reasonable response confidence
        assert confidence > 0.4  # Should be confident with good retrieval
    
    def test_response_length_limits(self, response_generator, sample_retrieval_context):
        """Test that responses respect length limits."""
        response = response_generator.generate_response(sample_retrieval_context)
        
        response_text = response['response_text']
        assert len(response_text) <= 500  # Configured max length
        assert len(response_text) >= 20   # Minimum meaningful length
    
    def test_multilingual_response_support(self, response_generator):
        """Test support for multilingual responses."""
        hindi_context = {
            'query': {
                'original_query': 'मुझे बुखार है',
                'symptoms': ['fever'],
                'query_type': 'symptom_inquiry',
                'metadata': {'language': 'hindi'}
            },
            'documents': [
                {
                    'document': {
                        'content': 'Fever is a common symptom that requires medical attention.',
                        'metadata': {'source': 'medlineplus'}
                    },
                    'final_score': 0.8
                }
            ]
        }
        
        response = response_generator.generate_response(hindi_context)
        
        # Should generate appropriate response
        assert 'response_text' in response
        assert len(response['response_text']) > 0
    
    def test_pregnancy_context_handling(self, response_generator):
        """Test special handling for pregnancy-related queries."""
        pregnancy_context = {
            'query': {
                'original_query': 'pregnant woman with fever',
                'symptoms': ['fever'],
                'query_type': 'symptom_inquiry',
                'metadata': {'special_populations': ['pregnancy']}
            },
            'documents': [
                {
                    'document': {
                        'content': 'Fever during pregnancy requires immediate medical evaluation.',
                        'metadata': {'source': 'who'}
                    },
                    'final_score': 0.9
                }
            ]
        }
        
        response = response_generator.generate_response(pregnancy_context)
        
        # Should include pregnancy-specific guidance
        assert 'pregnancy' in response['response_text'].lower()
        
        # Should have pregnancy disclaimer
        pregnancy_disclaimer = any('pregnancy' in d.lower() for d in response['disclaimers'])
        assert pregnancy_disclaimer