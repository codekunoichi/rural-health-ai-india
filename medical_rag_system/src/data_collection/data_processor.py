import re
from typing import List, Dict, Set, Any
from datetime import datetime
import logging
from config.settings import Settings
from config.medical_constants import MalariaConstants

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Process and clean medical data for the RAG system.
    Handles text cleaning, symptom extraction, and emergency detection.
    """
    
    def __init__(self):
        """Initialize the data processor with medical constants."""
        self.chunk_size = Settings.CHUNK_SIZE
        self.chunk_overlap = Settings.CHUNK_OVERLAP
        
        # Load medical knowledge from constants
        self.emergency_keywords = MalariaConstants.EMERGENCY_SYMPTOMS
        self.severe_keywords = MalariaConstants.SEVERE_SYMPTOMS
        self.early_keywords = MalariaConstants.EARLY_SYMPTOMS
        self.hindi_symptoms = MalariaConstants.HINDI_SYMPTOMS
        self.bengali_symptoms = MalariaConstants.BENGALI_SYMPTOMS
        
        # Compile regex patterns for efficiency
        self._compile_symptom_patterns()
    
    def _compile_symptom_patterns(self):
        """Compile regex patterns for symptom detection."""
        # Create pattern for all symptoms (English, Hindi, and Bengali)
        all_symptoms = (
            self.emergency_keywords | 
            self.severe_keywords | 
            self.early_keywords | 
            set(self.hindi_symptoms.keys()) |
            set(self.hindi_symptoms.values()) |
            set(self.bengali_symptoms.keys()) |
            set(self.bengali_symptoms.values())
        )
        
        # Sort by length (longest first) to match longer phrases first
        sorted_symptoms = sorted(all_symptoms, key=len, reverse=True)
        
        # Escape special regex characters and create pattern
        escaped_symptoms = [re.escape(symptom) for symptom in sorted_symptoms]
        # Use flexible boundaries that work with Unicode characters
        # Match symptoms even when they appear within larger phrases
        self.symptom_pattern = re.compile(
            r'(' + '|'.join(escaped_symptoms) + r')', 
            re.IGNORECASE | re.UNICODE
        )
        
        # Pattern for emergency indicators (include Bengali and Hindi emergency terms)
        emergency_terms = set(self.emergency_keywords)
        
        # Add Bengali emergency terms
        for bengali_term, english_term in self.bengali_symptoms.items():
            if english_term in self.emergency_keywords:
                emergency_terms.add(bengali_term)
        
        # Add Hindi emergency terms  
        for hindi_term, english_term in self.hindi_symptoms.items():
            if english_term in self.emergency_keywords:
                emergency_terms.add(hindi_term)
        
        emergency_escaped = [re.escape(symptom) for symptom in sorted(emergency_terms, key=len, reverse=True)]
        self.emergency_pattern = re.compile(
            r'(' + '|'.join(emergency_escaped) + r')', 
            re.IGNORECASE | re.UNICODE
        )
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize medical text.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned and normalized text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove excessive whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Clean excessive punctuation first
        text = re.sub(r'[!]{2,}', '', text)  # Remove repeated !
        text = re.sub(r'[?]{2,}', '', text)  # Remove repeated ?
        text = re.sub(r'[.]{3,}', '...', text)  # Replace many dots with ellipsis
        
        # Remove special characters but keep medical punctuation and Unicode letters
        # Keep Hindi characters (Devanagari range: \u0900-\u097F) and Bengali characters (Bengali range: \u0980-\u09FF)
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\%\°\/\u0900-\u097F\u0980-\u09FF]', '', text)
        
        # Normalize temperature mentions
        text = re.sub(r'(\d+)\s*degrees?\s*[Ff]ahrenheit', r'\1°F', text)
        text = re.sub(r'(\d+)\s*degrees?\s*[Cc]elsius', r'\1°C', text)
        
        # Normalize common medical abbreviations
        text = re.sub(r'\btemp\b', 'temperature', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsymptoms?\b', 'symptoms', text, flags=re.IGNORECASE)
        
        return text
    
    def extract_symptoms(self, text: str) -> List[str]:
        """
        Extract symptoms mentioned in medical text.
        
        Args:
            text: Medical text to analyze
            
        Returns:
            List of symptoms found in the text
        """
        if not text:
            return []
        
        # Clean text first
        cleaned_text = self.clean_text(text)
        
        # Find all symptom matches
        matches = self.symptom_pattern.findall(cleaned_text)
        
        # Convert to lowercase and deduplicate
        symptoms = list(set(match.lower() for match in matches))
        
        # Translate Hindi and Bengali symptoms to English
        translated_symptoms = []
        for symptom in symptoms:
            if symptom in self.hindi_symptoms:
                translated_symptoms.append(self.hindi_symptoms[symptom])
            elif symptom in self.bengali_symptoms:
                translated_symptoms.append(self.bengali_symptoms[symptom])
            else:
                translated_symptoms.append(symptom)
        
        # Remove duplicates after translation
        unique_symptoms = list(set(translated_symptoms))
        
        logger.debug(f"Extracted {len(unique_symptoms)} symptoms from text")
        return unique_symptoms
    
    def detect_emergency_indicators(self, text: str) -> List[str]:
        """
        Detect emergency symptoms that require immediate medical attention.
        
        Args:
            text: Medical text to analyze
            
        Returns:
            List of emergency indicators found
        """
        if not text:
            return []
        
        cleaned_text = self.clean_text(text)
        
        # Find emergency symptom matches
        matches = self.emergency_pattern.findall(cleaned_text)
        
        # Convert to lowercase and deduplicate
        emergency_indicators = list(set(match.lower() for match in matches))
        
        # Check for temperature-based emergencies
        temp_matches = re.findall(r'(\d+)°?[FC]?', cleaned_text)
        for temp_str in temp_matches:
            try:
                temp = float(temp_str)
                # High fever indicators (assuming Fahrenheit if no unit specified and >50)
                if temp > 50:  # Likely Fahrenheit
                    if temp >= 104:  # 104°F = 40°C
                        emergency_indicators.append("high fever")
                elif temp >= 40:  # Celsius
                    emergency_indicators.append("high fever")
            except ValueError:
                continue
        
        if emergency_indicators:
            logger.warning(f"Emergency indicators detected: {emergency_indicators}")
        
        return emergency_indicators
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks for vector storage.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks with overlap
        """
        if not text:
            return []
        
        # Split into sentences first
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) + 1 <= self.chunk_size:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
            else:
                # Save current chunk if it has content
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Start new chunk with current sentence
                current_chunk = sentence
        
        # Add the last chunk if it has content
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Apply overlap between chunks if we have multiple chunks
        if len(chunks) > 1:
            overlapped_chunks = []
            
            for i, chunk in enumerate(chunks):
                if i == 0:
                    overlapped_chunks.append(chunk)
                else:
                    # Get last few words from previous chunk for overlap
                    prev_chunk = chunks[i-1]
                    prev_words = prev_chunk.split()
                    
                    # Take last N words for overlap (up to chunk_overlap characters)
                    overlap_words = []
                    overlap_length = 0
                    
                    for word in reversed(prev_words):
                        if overlap_length + len(word) + 1 <= self.chunk_overlap:
                            overlap_words.insert(0, word)
                            overlap_length += len(word) + 1
                        else:
                            break
                    
                    if overlap_words:
                        overlapped_chunk = " ".join(overlap_words) + " " + chunk
                        overlapped_chunks.append(overlapped_chunk)
                    else:
                        overlapped_chunks.append(chunk)
            
            chunks = overlapped_chunks
        
        logger.debug(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a complete medical document through the full pipeline.
        
        Args:
            document: Raw document with title, content, url, date
            
        Returns:
            Processed document with extracted information and metadata
        """
        if not document or 'content' not in document:
            raise ValueError("Document must contain 'content' field")
        
        # Clean the content
        cleaned_content = self.clean_text(document['content'])
        
        if not cleaned_content:
            logger.warning("Document content is empty after cleaning")
            return {
                'title': document.get('title', ''),
                'content': '',
                'metadata': {},
                'symptoms': [],
                'emergency_indicators': [],
                'chunks': []
            }
        
        # Extract symptoms and emergency indicators
        symptoms = self.extract_symptoms(cleaned_content)
        emergency_indicators = self.detect_emergency_indicators(cleaned_content)
        
        # Create chunks
        chunks = self.chunk_text(cleaned_content)
        
        # Build metadata
        metadata = {
            'source_url': document.get('url', ''),
            'date': document.get('date', ''),
            'processed_at': datetime.now().isoformat(),
            'chunk_count': len(chunks),
            'symptom_count': len(symptoms),
            'has_emergency_indicators': len(emergency_indicators) > 0,
            'source': document.get('source', 'unknown')
        }
        
        processed_document = {
            'title': document.get('title', ''),
            'content': cleaned_content,
            'metadata': metadata,
            'symptoms': symptoms,
            'emergency_indicators': emergency_indicators,
            'chunks': chunks
        }
        
        logger.info(f"Processed document: {document.get('title', 'Untitled')} - "
                   f"{len(chunks)} chunks, {len(symptoms)} symptoms, "
                   f"{len(emergency_indicators)} emergency indicators")
        
        return processed_document
    
    def batch_process_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple documents in batch.
        
        Args:
            documents: List of raw documents to process
            
        Returns:
            List of processed documents
        """
        processed_documents = []
        
        for i, document in enumerate(documents):
            try:
                processed = self.process_document(document)
                processed_documents.append(processed)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(documents)} documents")
                    
            except Exception as e:
                logger.error(f"Failed to process document {i}: {e}")
                continue
        
        logger.info(f"Successfully processed {len(processed_documents)}/{len(documents)} documents")
        return processed_documents