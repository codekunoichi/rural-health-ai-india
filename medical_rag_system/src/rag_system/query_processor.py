import re
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import logging

from config.medical_constants import MalariaConstants
from src.data_collection.data_processor import DataProcessor

logger = logging.getLogger(__name__)

class MedicalQueryProcessor:
    """
    Process and analyze medical queries from users.
    Extracts symptoms, detects emergencies, and prepares queries for retrieval.
    """
    
    def __init__(self):
        """Initialize the medical query processor."""
        self.malaria_constants = MalariaConstants()
        self.data_processor = DataProcessor()  # Reuse existing symptom extraction
        
        # Query classification patterns
        self.emergency_patterns = [
            r'\b(unconscious|unconsciousness|coma|collapse)\b',
            r'\b(seizure|seizures|convulsion|convulsions)\b',
            r'\b(difficulty breathing|shortness of breath|can\'?t breathe)\b',
            r'\b(severe|extreme|unbearable)\s+(pain|headache|vomiting)\b',
            r'\b(emergency|urgent|immediate|help|serious)\b',
            r'\b(blood\s+in\s+vomit|bloody\s+vomit|black\s+vomit)\b'
        ]
        
        self.symptom_patterns = [
            r'\b(have|having|feel|feeling|experience|experiencing)\s+(\w+)\b',
            r'\b(symptoms?|signs?)\b',
            r'\b(pain|ache|aching|hurt|hurting)\b',
            r'\b(sick|ill|unwell|not\s+feeling\s+well)\b'
        ]
        
        self.duration_patterns = [
            r'\b(\d+)\s+(day|days|week|weeks|month|months|hour|hours)\b',
            r'\b(since|for)\s+(\d+)\s+(day|days|week|weeks)\b',
            r'\b(yesterday|today|last\s+night)\b'
        ]
        
        # Compile patterns for efficiency
        self.compiled_emergency_patterns = [re.compile(p, re.IGNORECASE) for p in self.emergency_patterns]
        self.compiled_symptom_patterns = [re.compile(p, re.IGNORECASE) for p in self.symptom_patterns]
        self.compiled_duration_patterns = [re.compile(p, re.IGNORECASE) for p in self.duration_patterns]
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a complete medical query through the full pipeline.
        
        Args:
            query: Raw user query string
            
        Returns:
            Processed query with extracted information and metadata
        """
        logger.info(f"Processing medical query: '{query[:50]}...'")
        
        if not query or not query.strip():
            return self._empty_query_result(query)
        
        try:
            # Normalize and clean the query
            processed_query = self._normalize_query(query)
            
            # Extract symptoms
            symptoms = self.extract_symptoms(processed_query)
            
            # Detect emergency intent
            emergency_detected, emergency_indicators = self.detect_emergency_intent(processed_query)
            
            # Classify query type
            query_type = self.classify_query_type(processed_query, symptoms, emergency_detected)
            
            # Extract additional metadata
            metadata = self._extract_metadata(processed_query)
            
            # Calculate confidence score
            confidence = self._calculate_query_confidence(
                processed_query, symptoms, emergency_detected, query_type
            )
            
            result = {
                'original_query': query,
                'processed_query': processed_query,
                'symptoms': symptoms,
                'query_type': query_type,
                'emergency_detected': emergency_detected,
                'emergency_indicators': emergency_indicators,
                'confidence': confidence,
                'metadata': metadata,
                'processed_at': datetime.now().isoformat()
            }
            
            logger.info(f"Query processed successfully. Type: {query_type}, "
                       f"Symptoms: {len(symptoms)}, Emergency: {emergency_detected}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            return self._error_query_result(query, str(e))
    
    def extract_symptoms(self, query: str) -> List[str]:
        """
        Extract symptoms from the query text.
        
        Args:
            query: Query text to analyze
            
        Returns:
            List of identified symptoms
        """
        if not query:
            return []
        
        # Use existing data processor for symptom extraction
        symptoms = self.data_processor.extract_symptoms(query)
        
        # Additional query-specific symptom extraction
        query_lower = query.lower()
        additional_symptoms = []
        
        # Look for symptom descriptions
        symptom_phrases = [
            'feel sick', 'feeling unwell', 'not feeling well',
            'body aches', 'muscle pain', 'joint pain',
            'loss of appetite', 'difficulty sleeping'
        ]
        
        for phrase in symptom_phrases:
            if phrase in query_lower:
                additional_symptoms.append(phrase.replace(' ', '_'))
        
        # Combine and deduplicate
        all_symptoms = list(set(symptoms + additional_symptoms))
        
        # Filter out very generic terms
        filtered_symptoms = [s for s in all_symptoms if len(s) > 2 and s != 'pain']
        
        logger.debug(f"Extracted {len(filtered_symptoms)} symptoms: {filtered_symptoms}")
        return filtered_symptoms
    
    def detect_emergency_intent(self, query: str) -> Tuple[bool, List[str]]:
        """
        Detect if the query indicates a medical emergency.
        
        Args:
            query: Query text to analyze
            
        Returns:
            Tuple of (is_emergency, list_of_emergency_indicators)
        """
        if not query:
            return False, []
        
        emergency_indicators = []
        
        # Check for emergency patterns
        for pattern in self.compiled_emergency_patterns:
            matches = pattern.findall(query)
            emergency_indicators.extend(matches)
        
        # Use existing emergency detection
        existing_indicators = self.data_processor.detect_emergency_indicators(query)
        emergency_indicators.extend(existing_indicators)
        
        # Check for urgent temporal expressions
        urgent_temporal = [
            'right now', 'immediately', 'as soon as possible',
            'can\'t wait', 'getting worse', 'rapidly'
        ]
        
        query_lower = query.lower()
        for temporal in urgent_temporal:
            if temporal in query_lower:
                emergency_indicators.append(temporal)
        
        # Remove duplicates and empty strings
        emergency_indicators = list(set([ind for ind in emergency_indicators if ind.strip()]))
        
        is_emergency = len(emergency_indicators) > 0
        
        if is_emergency:
            logger.warning(f"Emergency detected in query. Indicators: {emergency_indicators}")
        
        return is_emergency, emergency_indicators
    
    def classify_query_type(self, query: str, symptoms: List[str] = None, 
                           emergency_detected: bool = None) -> str:
        """
        Classify the type of medical query.
        
        Args:
            query: Query text
            symptoms: Extracted symptoms (optional)
            emergency_detected: Whether emergency was detected (None = auto-detect)
            
        Returns:
            Query type classification
        """
        # Auto-detect emergency if not explicitly provided
        if emergency_detected is None:
            emergency_detected, _ = self.detect_emergency_intent(query)
        
        if emergency_detected:
            return 'emergency'
        
        query_lower = query.lower()
        
        # Check for medical keywords
        medical_keywords = {
            'symptom', 'symptoms', 'disease', 'illness', 'condition',
            'treatment', 'medicine', 'doctor', 'hospital', 'health',
            'fever', 'pain', 'ache', 'sick', 'unwell'
        }
        
        medical_keyword_count = sum(1 for word in medical_keywords if word in query_lower)
        
        # Non-medical query detection
        non_medical_indicators = {
            'weather', 'temperature outside', 'forecast',
            'recipe', 'cooking', 'food',
            'news', 'sports', 'politics',
            'time', 'date', 'calendar'
        }
        
        if any(indicator in query_lower for indicator in non_medical_indicators):
            return 'non_medical'
        
        # Symptom inquiry
        if symptoms and len(symptoms) > 0:
            return 'symptom_inquiry'
        
        # General medical question
        if medical_keyword_count > 0:
            return 'medical_question'
        
        # Prevention/information seeking
        prevention_keywords = ['prevent', 'avoid', 'protection', 'vaccine', 'immunization']
        if any(keyword in query_lower for keyword in prevention_keywords):
            return 'prevention_inquiry'
        
        # Default to general medical if uncertain
        return 'medical_question' if medical_keyword_count > 0 else 'non_medical'
    
    def _normalize_query(self, query: str) -> str:
        """
        Normalize and clean the query text.
        
        Args:
            query: Raw query text
            
        Returns:
            Normalized query text
        """
        if not query:
            return ""
        
        # Use existing text cleaning
        normalized = self.data_processor.clean_text(query)
        
        # Clean up repeated punctuation
        normalized = re.sub(r'[!]{2,}', '', normalized)  # Remove repeated !
        normalized = re.sub(r'[?]{2,}', '', normalized)  # Remove repeated ?
        normalized = re.sub(r'[,]{2,}', ',', normalized)  # Replace repeated commas with single
        normalized = re.sub(r'[.]{2,}', '.', normalized)  # Replace repeated periods with single
        
        # Additional query-specific normalizations
        # Fix common typos and variations
        typo_corrections = {
            r'\bfever\s+and\s+cold\b': 'fever and chills',
            r'\bhead\s+ache\b': 'headache',
            r'\bstomach\s+ache\b': 'stomach pain',
            r'\bbody\s+pain\b': 'body aches',
            r'\bcan\'?t\s+sleep\b': 'difficulty sleeping',
            r'\bvery\s+tired\b': 'fatigue'
        }
        
        for pattern, replacement in typo_corrections.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        return normalized.strip()
    
    def _extract_metadata(self, query: str) -> Dict[str, Any]:
        """
        Extract additional metadata from the query.
        
        Args:
            query: Processed query text
            
        Returns:
            Dictionary of extracted metadata
        """
        metadata = {
            'duration': None,
            'severity_indicators': [],
            'medical_keywords': [],
            'temporal_expressions': [],
            'special_populations': []
        }
        
        # Extract duration information
        for pattern in self.compiled_duration_patterns:
            matches = pattern.findall(query)
            if matches:
                metadata['duration'] = matches[0] if isinstance(matches[0], str) else ' '.join(matches[0])
                break
        
        # Extract severity indicators
        severity_words = ['severe', 'extreme', 'unbearable', 'intense', 'terrible', 'awful']
        query_lower = query.lower()
        metadata['severity_indicators'] = [word for word in severity_words if word in query_lower]
        
        # Extract medical keywords
        medical_terms = self.malaria_constants.EARLY_SYMPTOMS | self.malaria_constants.SEVERE_SYMPTOMS | self.malaria_constants.EMERGENCY_SYMPTOMS
        metadata['medical_keywords'] = [term for term in medical_terms if term.lower() in query_lower]
        
        # Detect special populations
        if 'pregnant' in query_lower or 'pregnancy' in query_lower:
            metadata['special_populations'].append('pregnancy')
        if 'child' in query_lower or 'baby' in query_lower or 'infant' in query_lower:
            metadata['special_populations'].append('pediatric')
        if 'elderly' in query_lower or 'old person' in query_lower:
            metadata['special_populations'].append('elderly')
        
        # Language detection
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', query))
        bengali_chars = len(re.findall(r'[\u0980-\u09FF]', query))
        total_chars = len(query.replace(' ', ''))
        
        if total_chars > 0:
            hindi_ratio = hindi_chars / total_chars
            bengali_ratio = bengali_chars / total_chars
            
            # Check for mixed language content
            if (hindi_ratio > 0.1 or bengali_ratio > 0.1) and (hindi_ratio + bengali_ratio) < 0.7:
                # Has substantial non-Indic content alongside Indic characters
                metadata['language'] = 'mixed'
            elif bengali_ratio > 0.3:
                metadata['language'] = 'bengali'
            elif hindi_ratio > 0.3:
                metadata['language'] = 'hindi'
            elif (hindi_ratio + bengali_ratio) > 0.1:
                # Predominantly Indic but below individual thresholds
                metadata['language'] = 'mixed'
            else:
                metadata['language'] = 'english'
        
        return metadata
    
    def _calculate_query_confidence(self, query: str, symptoms: List[str], 
                                   emergency_detected: bool, query_type: str) -> float:
        """
        Calculate confidence score for the processed query.
        
        Args:
            query: Processed query text
            symptoms: Extracted symptoms
            emergency_detected: Emergency detection result
            query_type: Classified query type
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.0
        
        # Base confidence from query length and content
        if len(query) > 10:
            confidence += 0.2
        if len(query) > 30:
            confidence += 0.1
        
        # Confidence from symptom extraction
        if symptoms:
            confidence += min(len(symptoms) * 0.15, 0.4)
        
        # Higher confidence for clear medical queries
        if query_type in ['symptom_inquiry', 'emergency']:
            confidence += 0.3
        elif query_type == 'medical_question':
            confidence += 0.2
        
        # Emergency queries get high confidence
        if emergency_detected:
            confidence += 0.2
        
        # Confidence from medical keyword density
        medical_words = ['fever', 'pain', 'ache', 'symptoms', 'sick', 'illness', 'disease']
        word_count = len(query.split())
        medical_word_count = sum(1 for word in medical_words if word in query.lower())
        
        if word_count > 0:
            medical_density = medical_word_count / word_count
            confidence += medical_density * 0.2
        
        # Cap confidence at 1.0
        return min(confidence, 1.0)
    
    def _empty_query_result(self, query: str) -> Dict[str, Any]:
        """Generate result for empty query."""
        return {
            'original_query': query,
            'processed_query': '',
            'symptoms': [],
            'query_type': 'invalid',
            'emergency_detected': False,
            'emergency_indicators': [],
            'confidence': 0.0,
            'metadata': {},
            'processed_at': datetime.now().isoformat(),
            'error': 'Empty query provided'
        }
    
    def _error_query_result(self, query: str, error_msg: str) -> Dict[str, Any]:
        """Generate result for query processing error."""
        return {
            'original_query': query,
            'processed_query': query,
            'symptoms': [],
            'query_type': 'error',
            'emergency_detected': False,
            'emergency_indicators': [],
            'confidence': 0.0,
            'metadata': {},
            'processed_at': datetime.now().isoformat(),
            'error': error_msg
        }