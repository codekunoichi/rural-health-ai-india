from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from src.knowledge_base.vector_store import MedicalVectorStore
from config.settings import Settings

logger = logging.getLogger(__name__)

class MedicalRetrievalEngine:
    """
    Retrieval engine for medical documents with context-aware ranking.
    Optimized for medical queries with symptom and emergency prioritization.
    """
    
    def __init__(self, vector_store_path: Optional[str] = None):
        """
        Initialize the medical retrieval engine.
        
        Args:
            vector_store_path: Optional path to vector store
        """
        self.vector_store = MedicalVectorStore(vector_store_path)
        self.max_retrieved_docs = Settings.MAX_RETRIEVED_DOCS
        self.similarity_threshold = Settings.SIMILARITY_THRESHOLD
        
        logger.info("MedicalRetrievalEngine initialized")
    
    def retrieve_relevant_documents(self, processed_query: Dict[str, Any], 
                                   top_k: int = None) -> Dict[str, Any]:
        """
        Retrieve relevant medical documents for a processed query.
        
        Args:
            processed_query: Output from MedicalQueryProcessor
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary with retrieved documents and metadata
        """
        top_k = top_k or self.max_retrieved_docs
        
        logger.info(f"Retrieving documents for query type: {processed_query.get('query_type')}")
        
        try:
            # Determine search strategy based on query type
            search_params = self._determine_search_params(processed_query)
            
            # Perform vector search
            search_results = self._perform_vector_search(
                processed_query['processed_query'],
                top_k,
                search_params
            )
            
            # Rank by medical relevance
            ranked_results = self.rank_by_medical_relevance(
                search_results,
                query_symptoms=processed_query.get('symptoms', []),
                query_type=processed_query.get('query_type'),
                emergency_detected=processed_query.get('emergency_detected', False)
            )
            
            # Apply additional filtering if needed
            filtered_results = self._apply_quality_filters(ranked_results)
            
            # Build retrieval metadata
            retrieval_metadata = self._build_retrieval_metadata(
                processed_query, search_results, filtered_results
            )
            
            result = {
                'documents': filtered_results,
                'retrieval_metadata': retrieval_metadata,
                'query_context': processed_query,
                'retrieved_at': datetime.now().isoformat()
            }
            
            logger.info(f"Retrieved {len(filtered_results)} relevant documents")
            return result
            
        except Exception as e:
            logger.error(f"Document retrieval failed: {e}")
            return self._empty_retrieval_result(processed_query, str(e))
    
    def rank_by_medical_relevance(self, search_results: List[Dict[str, Any]], 
                                 query_symptoms: List[str] = None,
                                 query_type: str = None,
                                 emergency_detected: bool = False) -> List[Dict[str, Any]]:
        """
        Rank documents by medical relevance to the query.
        
        Args:
            search_results: Raw search results from vector store
            query_symptoms: Symptoms extracted from query
            query_type: Type of medical query
            emergency_detected: Whether emergency was detected
            
        Returns:
            List of documents ranked by medical relevance
        """
        if not search_results:
            return []
        
        query_symptoms = query_symptoms or []
        
        # Calculate enhanced relevance scores
        for result in search_results:
            base_score = result.get('score', 0.0)
            relevance_boost = self._calculate_relevance_boost(
                result['document'], query_symptoms, query_type, emergency_detected
            )
            
            result['final_score'] = base_score + relevance_boost
            result['relevance_factors'] = self._explain_relevance_factors(
                result['document'], query_symptoms, query_type, emergency_detected
            )
        
        # Sort by final score (highest first)
        ranked_results = sorted(search_results, key=lambda x: x['final_score'], reverse=True)
        
        logger.debug(f"Ranked {len(ranked_results)} documents by medical relevance")
        return ranked_results
    
    def filter_by_context(self, search_results: List[Dict[str, Any]], 
                         context_type: str) -> List[Dict[str, Any]]:
        """
        Filter documents by specific medical context.
        
        Args:
            search_results: Search results to filter
            context_type: Type of medical context to filter for
            
        Returns:
            Filtered list of documents
        """
        if not search_results:
            return []
        
        filtered_results = []
        
        for result in search_results:
            document = result['document']
            doc_metadata = document.get('metadata', {})
            
            # Apply context-specific filters
            if self._matches_context(document, context_type):
                filtered_results.append(result)
        
        logger.debug(f"Filtered to {len(filtered_results)} documents for context: {context_type}")
        return filtered_results
    
    def _determine_search_params(self, processed_query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine search parameters based on query characteristics.
        
        Args:
            processed_query: Processed query information
            
        Returns:
            Dictionary of search parameters
        """
        params = {
            'medical_context': None,
            'min_score': self.similarity_threshold
        }
        
        query_type = processed_query.get('query_type')
        emergency_detected = processed_query.get('emergency_detected', False)
        
        # Set medical context for focused search
        if emergency_detected:
            params['medical_context'] = 'emergency'
            params['min_score'] = 0.6  # Lower threshold for emergency
        elif query_type == 'symptom_inquiry':
            params['medical_context'] = 'symptoms'
        elif query_type == 'prevention_inquiry':
            params['medical_context'] = 'prevention'
        
        # Adjust parameters for special populations
        special_populations = processed_query.get('metadata', {}).get('special_populations', [])
        if 'pregnancy' in special_populations:
            params['pregnancy_context'] = True
        
        return params
    
    def _perform_vector_search(self, query_text: str, top_k: int, 
                              search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search.
        
        Args:
            query_text: Processed query text
            top_k: Number of results to retrieve
            search_params: Search parameters
            
        Returns:
            List of search results
        """
        try:
            # Use vector store search with medical context
            results = self.vector_store.search(
                query=query_text,
                top_k=top_k,
                medical_context=search_params.get('medical_context'),
                min_score=search_params.get('min_score', 0.0)
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    def _calculate_relevance_boost(self, document: Dict[str, Any], 
                                  query_symptoms: List[str],
                                  query_type: str,
                                  emergency_detected: bool) -> float:
        """
        Calculate relevance boost based on medical factors.
        
        Args:
            document: Document to evaluate
            query_symptoms: Symptoms from query
            query_type: Type of query
            emergency_detected: Emergency detection flag
            
        Returns:
            Relevance boost score
        """
        boost = 0.0
        doc_metadata = document.get('metadata', {})
        
        # Emergency matching boost
        if emergency_detected:
            if doc_metadata.get('section_type') == 'emergency':
                boost += 0.3
            
            emergency_indicators = doc_metadata.get('emergency_indicators', [])
            if emergency_indicators:
                boost += 0.2
        
        # Symptom matching boost
        if query_symptoms:
            doc_symptoms = doc_metadata.get('symptoms', [])
            
            # Calculate symptom overlap
            query_symptoms_lower = [s.lower() for s in query_symptoms]
            doc_symptoms_lower = [s.lower() for s in doc_symptoms]
            
            overlap = set(query_symptoms_lower) & set(doc_symptoms_lower)
            overlap_ratio = len(overlap) / len(query_symptoms_lower) if query_symptoms_lower else 0
            
            boost += overlap_ratio * 0.25
        
        # Source authority boost
        source = doc_metadata.get('source', '')
        authority_scores = {
            'medlineplus': 0.1,
            'who': 0.15,
            'cdc': 0.12,
            'icmr': 0.08
        }
        boost += authority_scores.get(source, 0.0)
        
        # Section type relevance
        section_type = doc_metadata.get('section_type')
        if query_type == 'symptom_inquiry' and section_type == 'symptoms':
            boost += 0.1
        elif query_type == 'emergency' and section_type == 'emergency':
            boost += 0.15
        
        return boost
    
    def _explain_relevance_factors(self, document: Dict[str, Any],
                                  query_symptoms: List[str],
                                  query_type: str,
                                  emergency_detected: bool) -> List[str]:
        """
        Generate explanations for relevance scoring factors.
        
        Args:
            document: Document being evaluated
            query_symptoms: Query symptoms
            query_type: Query type
            emergency_detected: Emergency detection flag
            
        Returns:
            List of relevance factor explanations
        """
        factors = []
        doc_metadata = document.get('metadata', {})
        
        # Emergency factors
        if emergency_detected and doc_metadata.get('section_type') == 'emergency':
            factors.append("Emergency medical content")
        
        # Symptom matching
        if query_symptoms:
            doc_symptoms = doc_metadata.get('symptoms', [])
            overlap = set([s.lower() for s in query_symptoms]) & set([s.lower() for s in doc_symptoms])
            if overlap:
                factors.append(f"Matches symptoms: {', '.join(overlap)}")
        
        # Source authority
        source = doc_metadata.get('source', '')
        if source in ['medlineplus', 'who', 'cdc']:
            factors.append(f"Authoritative source: {source}")
        
        # Content type
        section_type = doc_metadata.get('section_type')
        if section_type:
            factors.append(f"Relevant content type: {section_type}")
        
        return factors if factors else ["General medical relevance"]
    
    def _matches_context(self, document: Dict[str, Any], context_type: str) -> bool:
        """
        Check if document matches specified medical context.
        
        Args:
            document: Document to check
            context_type: Context type to match
            
        Returns:
            True if document matches context
        """
        doc_metadata = document.get('metadata', {})
        
        if context_type == 'symptoms':
            return (doc_metadata.get('section_type') == 'symptoms' or
                   len(doc_metadata.get('symptoms', [])) > 0)
        
        elif context_type == 'emergency':
            return (doc_metadata.get('section_type') == 'emergency' or
                   len(doc_metadata.get('emergency_indicators', [])) > 0)
        
        elif context_type == 'prevention':
            medical_contexts = doc_metadata.get('medical_context', [])
            return 'prevention' in medical_contexts
        
        elif context_type == 'treatment':
            medical_contexts = doc_metadata.get('medical_context', [])
            return 'treatment' in medical_contexts
        
        return True  # Default: include document
    
    def _apply_quality_filters(self, ranked_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply quality filters to ranked results.
        
        Args:
            ranked_results: Results ranked by relevance
            
        Returns:
            Quality-filtered results
        """
        if not ranked_results:
            return []
        
        filtered_results = []
        
        for result in ranked_results:
            document = result['document']
            
            # Filter by minimum score
            if result['final_score'] < self.similarity_threshold:
                continue
            
            # Filter by content length (avoid very short snippets)
            content_length = len(document.get('content', ''))
            if content_length < 20:
                continue
            
            # Filter duplicate or near-duplicate content
            if not self._is_duplicate_content(document, filtered_results):
                filtered_results.append(result)
            
            # Limit total results
            if len(filtered_results) >= self.max_retrieved_docs:
                break
        
        return filtered_results
    
    def _is_duplicate_content(self, document: Dict[str, Any], 
                             existing_results: List[Dict[str, Any]]) -> bool:
        """
        Check if document content is duplicate or very similar to existing results.
        
        Args:
            document: Document to check
            existing_results: Already selected results
            
        Returns:
            True if content appears to be duplicate
        """
        if not existing_results:
            return False
        
        content = document.get('content', '').lower()
        
        for existing in existing_results:
            existing_content = existing['document'].get('content', '').lower()
            
            # Simple similarity check based on content overlap
            if len(content) > 0 and len(existing_content) > 0:
                # Calculate Jaccard similarity of words
                content_words = set(content.split())
                existing_words = set(existing_content.split())
                
                if content_words and existing_words:
                    intersection = len(content_words & existing_words)
                    union = len(content_words | existing_words)
                    similarity = intersection / union if union > 0 else 0
                    
                    if similarity > 0.8:  # High similarity threshold
                        return True
        
        return False
    
    def _build_retrieval_metadata(self, processed_query: Dict[str, Any],
                                 search_results: List[Dict[str, Any]],
                                 filtered_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build metadata about the retrieval process.
        
        Args:
            processed_query: Original processed query
            search_results: Raw search results
            filtered_results: Final filtered results
            
        Returns:
            Retrieval metadata dictionary
        """
        metadata = {
            'query_type': processed_query.get('query_type'),
            'emergency_detected': processed_query.get('emergency_detected', False),
            'total_found': len(search_results),
            'after_filtering': len(filtered_results),
            'confidence': self._calculate_retrieval_confidence(filtered_results),
            'search_strategy': 'vector_similarity',
            'ranking_factors': ['semantic_similarity', 'medical_relevance', 'source_authority']
        }
        
        # Add score statistics
        if filtered_results:
            scores = [result['final_score'] for result in filtered_results]
            metadata['score_stats'] = {
                'max_score': max(scores),
                'min_score': min(scores),
                'avg_score': sum(scores) / len(scores)
            }
        
        return metadata
    
    def _calculate_retrieval_confidence(self, results: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence in retrieval results.
        
        Args:
            results: Retrieved and filtered results
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not results:
            return 0.0
        
        # Base confidence from number of results
        result_count_confidence = min(len(results) / 3.0, 1.0)  # Optimal around 3 results
        
        # Confidence from score quality
        scores = [result['final_score'] for result in results]
        avg_score = sum(scores) / len(scores)
        score_confidence = min(avg_score, 1.0)
        
        # Weighted combination
        overall_confidence = (result_count_confidence * 0.3) + (score_confidence * 0.7)
        
        return min(overall_confidence, 1.0)
    
    def _empty_retrieval_result(self, processed_query: Dict[str, Any], 
                               error_msg: str = None) -> Dict[str, Any]:
        """
        Generate empty retrieval result.
        
        Args:
            processed_query: Original query
            error_msg: Optional error message
            
        Returns:
            Empty retrieval result structure
        """
        return {
            'documents': [],
            'retrieval_metadata': {
                'total_found': 0,
                'after_filtering': 0,
                'confidence': 0.0,
                'error': error_msg
            },
            'query_context': processed_query,
            'retrieved_at': datetime.now().isoformat()
        }