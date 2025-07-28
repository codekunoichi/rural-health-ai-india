import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union, Dict, Any
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)

class EmbeddingsEngine:
    """
    Generate embeddings for medical text using sentence transformers.
    Optimized for multilingual medical content (English and Hindi).
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the embeddings engine.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name or Settings.EMBEDDING_MODEL
        self.embedding_dim = Settings.EMBEDDING_DIMENSION
        
        logger.info(f"Initializing embeddings engine with model: {self.model_name}")
        
        try:
            # Load the sentence transformer model
            self.model = SentenceTransformer(self.model_name)
            
            # Verify embedding dimension
            test_embedding = self.model.encode(["test"])
            actual_dim = test_embedding.shape[1]
            
            if actual_dim != self.embedding_dim:
                logger.warning(f"Expected embedding dimension {self.embedding_dim}, got {actual_dim}")
                self.embedding_dim = actual_dim
            
            logger.info(f"Embeddings engine initialized successfully. Dimension: {self.embedding_dim}")
            
        except Exception as e:
            logger.error(f"Failed to initialize embeddings engine: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            Numpy array of embeddings with shape (len(texts), embedding_dim)
        """
        if not texts:
            logger.debug("Empty text list provided, returning empty embeddings")
            return np.empty((0, self.embedding_dim), dtype=np.float32)
        
        try:
            logger.debug(f"Generating embeddings for {len(texts)} texts")
            
            # Preprocess texts for better medical context
            processed_texts = self._preprocess_medical_texts(texts)
            
            # Generate embeddings
            embeddings = self.model.encode(
                processed_texts,
                show_progress_bar=len(processed_texts) > 100,
                batch_size=32,
                convert_to_numpy=True,
                normalize_embeddings=True  # L2 normalization for better similarity
            )
            
            # Ensure correct dtype
            embeddings = embeddings.astype(np.float32)
            
            logger.debug(f"Generated embeddings shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query string to embed
            
        Returns:
            1D numpy array representing the query embedding
        """
        if not query or not query.strip():
            logger.debug("Empty query provided, returning zero embedding")
            return np.zeros(self.embedding_dim, dtype=np.float32)
        
        try:
            logger.debug(f"Generating embedding for query: '{query[:50]}...'")
            
            # Preprocess query for medical context
            processed_query = self._preprocess_medical_query(query)
            
            # Generate embedding
            embedding = self.model.encode(
                [processed_query],
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            # Return as 1D array
            result = embedding[0].astype(np.float32)
            
            logger.debug(f"Generated query embedding shape: {result.shape}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            raise
    
    def _preprocess_medical_texts(self, texts: List[str]) -> List[str]:
        """
        Preprocess medical texts for better embedding quality.
        
        Args:
            texts: List of raw texts
            
        Returns:
            List of preprocessed texts
        """
        processed_texts = []
        
        for text in texts:
            processed_text = self._preprocess_single_text(text)
            processed_texts.append(processed_text)
        
        return processed_texts
    
    def _preprocess_medical_query(self, query: str) -> str:
        """
        Preprocess a medical query for better matching.
        
        Args:
            query: Raw query string
            
        Returns:
            Preprocessed query string
        """
        return self._preprocess_single_text(query, is_query=True)
    
    def _preprocess_single_text(self, text: str, is_query: bool = False) -> str:
        """
        Preprocess a single text for medical embeddings.
        
        Args:
            text: Raw text string
            is_query: Whether this is a query (affects preprocessing)
            
        Returns:
            Preprocessed text string
        """
        if not text:
            return ""
        
        # Basic cleaning
        processed = text.strip()
        
        # Normalize medical terminology
        processed = self._normalize_medical_terms(processed)
        
        # Add medical context markers for queries
        if is_query:
            processed = self._add_query_context(processed)
        
        return processed
    
    def _normalize_medical_terms(self, text: str) -> str:
        """
        Normalize common medical terms for consistency.
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized medical terms
        """
        # Common medical term normalizations
        normalizations = {
            # Temperature variations
            r'\b(\d+)\s*degrees?\s*fahrenheit\b': r'\1°F',
            r'\b(\d+)\s*degrees?\s*celsius\b': r'\1°C',
            r'\b(\d+)\s*degrees?\b': r'\1°',
            
            # Symptom normalizations
            r'\bhigh\s+temperature\b': 'high fever',
            r'\belevated\s+temperature\b': 'high fever',
            r'\bbody\s+temperature\b': 'fever',
            r'\bheadaches?\b': 'headache',
            r'\bchills?\s+and\s+fever\b': 'fever and chills',
            r'\bfever\s+and\s+chills?\b': 'fever and chills',
            
            # Emergency terms
            r'\bunconscious\b': 'unconsciousness',
            r'\bpassing\s+out\b': 'unconsciousness',
            r'\bfainting\b': 'unconsciousness',
            r'\bseizures?\b': 'seizure',
            r'\bconvulsions?\b': 'seizure',
            
            # Hindi to English common terms (basic)
            r'\bबुखार\b': 'fever',
            r'\bसिर\s*दर्द\b': 'headache',
            r'\bकंपकंपी\b': 'chills'
        }
        
        import re
        result = text
        for pattern, replacement in normalizations.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def _add_query_context(self, query: str) -> str:
        """
        Add medical context to queries for better retrieval.
        
        Args:
            query: Input query
            
        Returns:
            Query with added medical context
        """
        query_lower = query.lower()
        
        # Add context based on query type
        contexts = []
        
        # Symptom queries
        symptom_indicators = ['feel', 'have', 'experiencing', 'symptoms', 'pain', 'ache']
        if any(indicator in query_lower for indicator in symptom_indicators):
            contexts.append('medical symptoms')
        
        # Emergency queries
        emergency_indicators = ['urgent', 'emergency', 'serious', 'immediate', 'help']
        if any(indicator in query_lower for indicator in emergency_indicators):
            contexts.append('medical emergency')
        
        # Malaria-specific queries
        malaria_indicators = ['malaria', 'mosquito', 'parasite', 'tropical']
        if any(indicator in query_lower for indicator in malaria_indicators):
            contexts.append('malaria information')
        
        # Add contexts to query
        if contexts:
            context_str = ' '.join(contexts)
            return f"{query} {context_str}"
        
        return query
    
    def get_embedding_dimension(self) -> int:
        """
        Get the embedding dimension.
        
        Returns:
            Embedding dimension as integer
        """
        return self.embedding_dim
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between -1 and 1
        """
        try:
            # Ensure both embeddings are normalized
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Compute cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to compute similarity: {e}")
            return 0.0
    
    def batch_similarity(self, query_embedding: np.ndarray, document_embeddings: np.ndarray) -> np.ndarray:
        """
        Compute similarities between query and multiple documents efficiently.
        
        Args:
            query_embedding: Query embedding vector (1D)
            document_embeddings: Document embeddings matrix (2D)
            
        Returns:
            Array of similarity scores
        """
        try:
            if document_embeddings.size == 0:
                return np.array([])
            
            # Ensure query is 2D for matrix multiplication
            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            # Compute batch cosine similarity using matrix multiplication
            # Assuming embeddings are already normalized
            similarities = np.dot(document_embeddings, query_embedding.T).flatten()
            
            return similarities.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Failed to compute batch similarities: {e}")
            return np.zeros(len(document_embeddings), dtype=np.float32)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            'model_name': self.model_name,
            'embedding_dimension': self.embedding_dim,
            'max_sequence_length': getattr(self.model, 'max_seq_length', 'unknown'),
            'model_type': type(self.model).__name__
        }