import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import json

from src.knowledge_base.document_processor import MedicalDocumentProcessor
from src.knowledge_base.embeddings import EmbeddingsEngine
from src.knowledge_base.vector_store import MedicalVectorStore

class TestMedicalDocumentProcessor:
    """Test cases for medical document processing following TDD approach."""
    
    @pytest.fixture
    def processor(self):
        """Create document processor instance for testing."""
        return MedicalDocumentProcessor()
    
    @pytest.fixture
    def sample_medical_documents(self):
        """Sample processed medical documents for testing."""
        return [
            {
                'title': 'Malaria Overview',
                'content': 'Malaria is a serious disease caused by parasites. Symptoms include fever, chills, and headache. High fever requires immediate medical attention.',
                'metadata': {
                    'source': 'medlineplus',
                    'date': '2023-12-01',
                    'source_url': 'https://medlineplus.gov/malaria.html'
                },
                'symptoms': ['fever', 'chills', 'headache'],
                'emergency_indicators': ['high fever'],
                'chunks': [
                    'Malaria is a serious disease caused by parasites.',
                    'Symptoms include fever, chills, and headache.',
                    'High fever requires immediate medical attention.'
                ]
            },
            {
                'title': 'Malaria Prevention',
                'content': 'Prevent malaria by using bed nets, repellents, and avoiding mosquito breeding areas. Seek medical care for persistent fever.',
                'metadata': {
                    'source': 'who',
                    'date': '2023-11-15',
                    'source_url': 'https://who.int/malaria/prevention'
                },
                'symptoms': ['persistent fever'],
                'emergency_indicators': [],
                'chunks': [
                    'Prevent malaria by using bed nets, repellents, and avoiding mosquito breeding areas.',
                    'Seek medical care for persistent fever.'
                ]
            }
        ]
    
    def test_processor_initialization(self, processor):
        """Test that document processor initializes correctly."""
        assert processor is not None
        assert hasattr(processor, 'create_medical_sections')
        assert hasattr(processor, 'enrich_with_metadata')
        assert hasattr(processor, 'create_searchable_documents')
    
    def test_create_medical_sections(self, processor):
        """Test creation of medical sections from processed documents."""
        documents = [
            {
                'title': 'Malaria Symptoms',
                'content': 'Fever is common. Emergency symptoms include seizures.',
                'symptoms': ['fever'],
                'emergency_indicators': ['seizures'],
                'chunks': ['Fever is common.', 'Emergency symptoms include seizures.']
            }
        ]
        
        sections = processor.create_medical_sections(documents)
        
        # Should create sections for different medical contexts
        assert len(sections) > 0
        
        # Check section structure
        for section in sections:
            assert 'id' in section
            assert 'content' in section
            assert 'metadata' in section
            assert 'section_type' in section
            
        # Should have different section types
        section_types = {s['section_type'] for s in sections}
        expected_types = {'symptoms', 'emergency', 'general'}
        assert len(section_types.intersection(expected_types)) > 0
    
    def test_create_symptom_sections(self, processor):
        """Test creation of symptom-specific sections."""
        document = {
            'title': 'Malaria Guide',
            'content': 'Common symptoms are fever and chills. Watch for high fever.',
            'symptoms': ['fever', 'chills', 'high fever'],
            'emergency_indicators': ['high fever'],
            'chunks': ['Common symptoms are fever and chills.', 'Watch for high fever.']
        }
        
        sections = processor.create_medical_sections([document])
        
        # Should have symptom sections
        symptom_sections = [s for s in sections if s['section_type'] == 'symptoms']
        assert len(symptom_sections) > 0
        
        # Check symptom section content
        symptom_section = symptom_sections[0]
        assert 'fever' in symptom_section['content'].lower()
        assert 'symptoms' in symptom_section['metadata']
        assert len(symptom_section['metadata']['symptoms']) > 0
    
    def test_create_emergency_sections(self, processor):
        """Test creation of emergency-specific sections."""
        document = {
            'title': 'Emergency Signs',
            'content': 'Unconsciousness and seizures require immediate care.',
            'symptoms': [],
            'emergency_indicators': ['unconsciousness', 'seizures'],
            'chunks': ['Unconsciousness and seizures require immediate care.']
        }
        
        sections = processor.create_medical_sections([document])
        
        # Should have emergency sections
        emergency_sections = [s for s in sections if s['section_type'] == 'emergency']
        assert len(emergency_sections) > 0
        
        # Check emergency section content
        emergency_section = emergency_sections[0]
        assert 'emergency' in emergency_section['content'].lower() or 'unconsciousness' in emergency_section['content'].lower()
        assert 'emergency_indicators' in emergency_section['metadata']
        assert len(emergency_section['metadata']['emergency_indicators']) > 0
    
    def test_enrich_with_metadata(self, processor):
        """Test metadata enrichment for searchability."""
        sections = [
            {
                'id': 'test_1',
                'content': 'Fever and chills are common malaria symptoms.',
                'metadata': {
                    'source': 'medlineplus',
                    'symptoms': ['fever', 'chills']
                },
                'section_type': 'symptoms'
            }
        ]
        
        enriched = processor.enrich_with_metadata(sections)
        
        # Should add search-related metadata
        assert len(enriched) == len(sections)
        
        enriched_section = enriched[0]
        assert 'keywords' in enriched_section['metadata']
        assert 'medical_context' in enriched_section['metadata']
        assert 'content_length' in enriched_section['metadata']
        
        # Keywords should include symptoms and key terms
        keywords = enriched_section['metadata']['keywords']
        assert 'fever' in keywords
        assert 'malaria' in keywords
    
    def test_create_searchable_documents(self, processor, sample_medical_documents):
        """Test complete pipeline to create searchable documents."""
        searchable_docs = processor.create_searchable_documents(sample_medical_documents)
        
        # Should return list of searchable documents
        assert isinstance(searchable_docs, list)
        assert len(searchable_docs) > 0
        
        # Each document should have required fields
        for doc in searchable_docs:
            assert 'id' in doc
            assert 'content' in doc
            assert 'metadata' in doc
            assert 'section_type' in doc
            
        # Should have multiple section types
        section_types = {doc['section_type'] for doc in searchable_docs}
        assert len(section_types) > 1
        
        # Should preserve original document information
        titles = [doc['metadata'].get('original_title', '') for doc in searchable_docs]
        assert 'Malaria Overview' in ' '.join(titles)
    
    def test_filter_by_medical_relevance(self, processor):
        """Test filtering of medically relevant content."""
        sections = [
            {
                'content': 'Malaria causes fever and requires treatment.',
                'metadata': {'symptoms': ['fever']},
                'section_type': 'symptoms'
            },
            {
                'content': 'The weather is nice today.',
                'metadata': {'symptoms': []},
                'section_type': 'general'
            }
        ]
        
        filtered = processor.filter_by_medical_relevance(sections)
        
        # Should keep medically relevant content
        assert len(filtered) >= 1
        
        # Should prioritize content with medical indicators
        medical_content = [s for s in filtered if 'malaria' in s['content'].lower() or len(s['metadata'].get('symptoms', [])) > 0]
        assert len(medical_content) > 0

class TestEmbeddingsEngine:
    """Test cases for embeddings engine following TDD approach."""
    
    @pytest.fixture
    def embeddings_engine(self):
        """Create embeddings engine instance for testing."""
        return EmbeddingsEngine()
    
    @pytest.fixture
    def sample_medical_texts(self):
        """Sample medical texts for embedding testing."""
        return [
            "Malaria symptoms include fever, chills, and headache.",
            "High fever requires immediate medical attention.",
            "Prevention includes using bed nets and repellents.",
            "बुखार और सिर दर्द मलेरिया के लक्षण हैं।"  # Hindi text
        ]
    
    def test_engine_initialization(self, embeddings_engine):
        """Test that embeddings engine initializes correctly."""
        assert embeddings_engine is not None
        assert hasattr(embeddings_engine, 'model')
        assert hasattr(embeddings_engine, 'embed_texts')
        assert hasattr(embeddings_engine, 'embed_query')
        
        # Should have expected dimensions
        assert embeddings_engine.embedding_dim == 384  # MiniLM-L6-v2 dimension
    
    @patch('sentence_transformers.SentenceTransformer')
    def test_embed_texts_basic(self, mock_sentence_transformer, embeddings_engine, sample_medical_texts):
        """Test basic text embedding functionality."""
        # Mock the sentence transformer
        mock_model = Mock()
        mock_embeddings = np.random.rand(len(sample_medical_texts), 384)
        mock_model.encode.return_value = mock_embeddings
        mock_sentence_transformer.return_value = mock_model
        
        # Reinitialize with mock
        embeddings_engine.model = mock_model
        
        embeddings = embeddings_engine.embed_texts(sample_medical_texts)
        
        # Should return numpy array
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (len(sample_medical_texts), 384)
        
        # Should call model.encode with correct parameters
        mock_model.encode.assert_called_once()
        call_args = mock_model.encode.call_args[0][0]
        assert len(call_args) == len(sample_medical_texts)
    
    @patch('sentence_transformers.SentenceTransformer')
    def test_embed_query_single(self, mock_sentence_transformer, embeddings_engine):
        """Test single query embedding."""
        # Mock the sentence transformer
        mock_model = Mock()
        mock_embedding = np.random.rand(1, 384)  # 2D array as expected by encode
        mock_model.encode.return_value = mock_embedding
        mock_sentence_transformer.return_value = mock_model
        
        # Reinitialize with mock
        embeddings_engine.model = mock_model
        
        query = "fever and headache symptoms"
        embedding = embeddings_engine.embed_query(query)
        
        # Should return 1D numpy array
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape == (384,)
        
        # Should call model.encode with processed query and parameters
        mock_model.encode.assert_called_once()
        call_args, call_kwargs = mock_model.encode.call_args
        assert len(call_args[0]) == 1  # Should be called with list of one item
        assert 'convert_to_numpy' in call_kwargs
        assert 'normalize_embeddings' in call_kwargs
    
    def test_batch_embedding_performance(self, embeddings_engine):
        """Test that batch embedding is more efficient than individual."""
        texts = ["fever", "headache", "chills", "nausea"] * 10  # 40 texts
        
        # This test would measure actual performance in a real scenario
        # For unit testing, we just verify the interface works
        with patch.object(embeddings_engine, 'model') as mock_model:
            mock_model.encode.return_value = np.random.rand(len(texts), 384)
            
            embeddings = embeddings_engine.embed_texts(texts)
            
            # Should process all texts in single call
            assert mock_model.encode.call_count == 1
            assert embeddings.shape[0] == len(texts)
    
    def test_multilingual_support(self, embeddings_engine):
        """Test support for Hindi and English medical terms."""
        mixed_texts = [
            "fever and chills",
            "बुखार और कंपकंपी",
            "high temperature",
            "तेज बुखार"
        ]
        
        with patch.object(embeddings_engine, 'model') as mock_model:
            mock_model.encode.return_value = np.random.rand(len(mixed_texts), 384)
            
            embeddings = embeddings_engine.embed_texts(mixed_texts)
            
            # Should handle mixed language content
            assert embeddings.shape[0] == len(mixed_texts)
            
            # Model should receive all texts
            call_args = mock_model.encode.call_args[0][0]
            assert len(call_args) == len(mixed_texts)
    
    def test_empty_input_handling(self, embeddings_engine):
        """Test handling of empty or invalid inputs."""
        # Empty list
        embeddings = embeddings_engine.embed_texts([])
        assert embeddings.shape == (0, 384)
        
        # Empty string
        with patch.object(embeddings_engine, 'model') as mock_model:
            mock_model.encode.return_value = np.random.rand(1, 384)
            
            embedding = embeddings_engine.embed_query("")
            assert embedding.shape == (384,)

class TestMedicalVectorStore:
    """Test cases for medical vector store following TDD approach."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)
    
    @pytest.fixture
    def vector_store(self, temp_dir):
        """Create vector store instance for testing."""
        return MedicalVectorStore(store_path=temp_dir / "test_store")
    
    @pytest.fixture
    def sample_documents(self):
        """Sample documents with embeddings for testing."""
        return [
            {
                'id': 'doc_1',
                'content': 'Malaria symptoms include fever and chills.',
                'metadata': {
                    'source': 'medlineplus',
                    'symptoms': ['fever', 'chills'],
                    'section_type': 'symptoms'
                }
            },
            {
                'id': 'doc_2', 
                'content': 'High fever requires immediate medical attention.',
                'metadata': {
                    'source': 'who',
                    'emergency_indicators': ['high fever'],
                    'section_type': 'emergency'
                }
            }
        ]
    
    @pytest.fixture
    def sample_embeddings(self):
        """Sample embeddings corresponding to documents."""
        return np.random.rand(2, 384).astype(np.float32)
    
    def test_vector_store_initialization(self, vector_store):
        """Test that vector store initializes correctly."""
        assert vector_store is not None
        assert hasattr(vector_store, 'store_path')
        assert hasattr(vector_store, 'build_index')
        assert hasattr(vector_store, 'search')
        assert hasattr(vector_store, 'add_documents')
    
    @patch('faiss.IndexFlatIP')
    def test_build_index_from_documents(self, mock_faiss_index, vector_store, sample_documents, sample_embeddings):
        """Test building FAISS index from documents and embeddings."""
        # Mock FAISS index
        mock_index = Mock()
        mock_faiss_index.return_value = mock_index
        
        # Mock embeddings engine
        with patch('src.knowledge_base.embeddings.EmbeddingsEngine') as mock_embeddings:
            mock_engine = Mock()
            mock_engine.embed_texts.return_value = sample_embeddings
            mock_embeddings.return_value = mock_engine
            
            vector_store.build_index(sample_documents)
            
            # Should create FAISS index
            mock_faiss_index.assert_called_once_with(384)
            
            # Should add embeddings to index
            mock_index.add.assert_called_once()
            added_embeddings = mock_index.add.call_args[0][0]
            assert added_embeddings.shape == sample_embeddings.shape
            
            # Should store document metadata
            assert len(vector_store.documents) == len(sample_documents)
    
    @patch('faiss.IndexFlatIP')
    def test_search_similar_documents(self, mock_faiss_index, vector_store, sample_documents, sample_embeddings):
        """Test searching for similar documents."""
        # Mock FAISS index
        mock_index = Mock()
        mock_index.ntotal = 2  # Number of vectors in index
        mock_faiss_index.return_value = mock_index
        
        # Mock search results
        distances = np.array([[0.9, 0.7]])  # High similarity scores
        indices = np.array([[0, 1]])
        mock_index.search.return_value = (distances, indices)
        
        # Build index first
        with patch('src.knowledge_base.embeddings.EmbeddingsEngine') as mock_embeddings:
            mock_engine = Mock()
            mock_engine.embed_texts.return_value = sample_embeddings
            mock_engine.embed_query.return_value = sample_embeddings[0]
            mock_engine.get_embedding_dimension.return_value = 384
            mock_embeddings.return_value = mock_engine
            
            vector_store.build_index(sample_documents)
            
            # Make sure embeddings_engine is properly mocked for search
            vector_store.embeddings_engine = mock_engine
            
            # Search for similar documents
            results = vector_store.search("fever and chills", top_k=2)
            
            # Should return search results
            assert len(results) == 2
            
            # Results should have correct structure
            for result in results:
                assert 'document' in result
                assert 'score' in result
                assert 'id' in result['document']
                assert 'content' in result['document']
            
            # Should be ordered by similarity score
            assert results[0]['score'] >= results[1]['score']
    
    def test_search_by_medical_context(self, vector_store, sample_documents):
        """Test searching with medical context filtering."""
        with patch.object(vector_store, 'index') as mock_index, \
             patch.object(vector_store, 'embeddings_engine') as mock_engine:
            
            # Setup mocks
            mock_engine.embed_query.return_value = np.random.rand(384)
            mock_index.search.return_value = (np.array([[0.9, 0.8]]), np.array([[0, 1]]))
            vector_store.documents = sample_documents
            
            # Test symptom-specific search
            results = vector_store.search("fever", medical_context="symptoms")
            
            # Should filter by medical context if implemented
            assert len(results) >= 1
    
    def test_add_documents_to_existing_index(self, vector_store, sample_documents):
        """Test adding new documents to existing index."""
        # Mock existing index
        with patch.object(vector_store, 'index') as mock_index, \
             patch.object(vector_store, 'embeddings_engine') as mock_engine:
            
            vector_store.documents = []  # Start with empty
            mock_engine.embed_texts.return_value = np.random.rand(len(sample_documents), 384)
            
            vector_store.add_documents(sample_documents)
            
            # Should add to index
            mock_index.add.assert_called_once()
            
            # Should update document store
            assert len(vector_store.documents) == len(sample_documents)
    
    def test_save_and_load_index(self, vector_store, sample_documents, temp_dir):
        """Test saving and loading vector store to/from disk."""
        with patch('faiss.write_index') as mock_write, \
             patch('faiss.read_index') as mock_read, \
             patch.object(vector_store, 'embeddings_engine') as mock_engine:
            
            # Build and save index
            mock_engine.embed_texts.return_value = np.random.rand(len(sample_documents), 384)
            vector_store.build_index(sample_documents)
            vector_store.save()
            
            # Should save FAISS index and metadata
            mock_write.assert_called_once()
            
            # Should save document metadata as JSON
            metadata_file = temp_dir / "test_store_metadata.json"
            
            # Load index
            mock_read.return_value = Mock()
            vector_store.load()
            
            # Should load FAISS index
            mock_read.assert_called_once()
    
    def test_search_empty_index(self, vector_store):
        """Test searching when index is empty."""
        # Search without building index
        results = vector_store.search("fever", top_k=5)
        
        # Should return empty results gracefully
        assert isinstance(results, list)
        assert len(results) == 0
    
    def test_medical_similarity_scoring(self, vector_store, sample_documents):
        """Test that medical similarity scoring prioritizes relevant content."""
        with patch.object(vector_store, 'index') as mock_index, \
             patch.object(vector_store, 'embeddings_engine') as mock_engine:
            
            # Mock search results with different scores
            distances = np.array([[0.95, 0.60, 0.80]])  # Different similarity levels
            indices = np.array([[0, 1, 0]])  # Mock indices
            mock_index.search.return_value = (distances, indices)
            
            # Add extra document for testing
            test_docs = sample_documents + [{
                'id': 'doc_3',
                'content': 'Weather information and general news.',
                'metadata': {'section_type': 'general'}
            }]
            vector_store.documents = test_docs
            
            mock_engine.embed_query.return_value = np.random.rand(384)
            
            results = vector_store.search("malaria fever symptoms", top_k=3)
            
            # Should return results ordered by relevance
            assert len(results) <= 3
            
            # Medical content should score higher than general content
            medical_results = [r for r in results if 'malaria' in r['document']['content'].lower()]
            if len(medical_results) > 1:
                # Should be in descending order of relevance
                scores = [r['score'] for r in medical_results]
                assert scores == sorted(scores, reverse=True)