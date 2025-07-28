import uuid
import re
from typing import List, Dict, Any, Set
from datetime import datetime
import logging
from config.medical_constants import MalariaConstants

logger = logging.getLogger(__name__)

class MedicalDocumentProcessor:
    """
    Process medical documents into searchable sections optimized for RAG retrieval.
    Creates specialized sections for symptoms, emergency situations, and general medical information.
    """
    
    def __init__(self):
        """Initialize the medical document processor."""
        self.malaria_constants = MalariaConstants()
        
        # Medical keywords for relevance scoring
        self.medical_keywords = {
            'symptoms', 'treatment', 'diagnosis', 'prevention', 'causes',
            'medicine', 'doctor', 'hospital', 'patient', 'disease',
            'infection', 'fever', 'malaria', 'parasite', 'mosquito',
            'health', 'medical', 'clinical', 'emergency', 'care'
        }
        
        # Hindi medical keywords
        self.hindi_medical_keywords = {
            'लक्षण', 'इलाज', 'उपचार', 'बचाव', 'रोग', 'बीमारी',
            'बुखार', 'मलेरिया', 'डॉक्टर', 'अस्पताल', 'दवा'
        }
    
    def create_searchable_documents(self, processed_documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create searchable documents from processed medical content.
        
        Args:
            processed_documents: List of documents from data processor
            
        Returns:
            List of searchable document sections with metadata
        """
        logger.info(f"Creating searchable documents from {len(processed_documents)} processed documents")
        
        # Create medical sections
        medical_sections = self.create_medical_sections(processed_documents)
        
        # Enrich with metadata for better searchability
        enriched_sections = self.enrich_with_metadata(medical_sections)
        
        # Filter by medical relevance
        relevant_sections = self.filter_by_medical_relevance(enriched_sections)
        
        logger.info(f"Created {len(relevant_sections)} searchable document sections")
        return relevant_sections
    
    def create_medical_sections(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create specialized medical sections from documents.
        
        Args:
            documents: Processed medical documents
            
        Returns:
            List of medical sections with different contexts
        """
        all_sections = []
        
        for doc in documents:
            # Create symptom-focused sections
            symptom_sections = self._create_symptom_sections(doc)
            all_sections.extend(symptom_sections)
            
            # Create emergency-focused sections  
            emergency_sections = self._create_emergency_sections(doc)
            all_sections.extend(emergency_sections)
            
            # Create general medical sections
            general_sections = self._create_general_sections(doc)
            all_sections.extend(general_sections)
        
        return all_sections
    
    def _create_symptom_sections(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create sections focused on symptom information."""
        sections = []
        
        if not document.get('symptoms'):
            return sections
        
        symptoms = document['symptoms']
        relevant_chunks = []
        
        # Find chunks that mention symptoms
        for chunk in document.get('chunks', []):
            chunk_lower = chunk.lower()
            if any(symptom.lower() in chunk_lower for symptom in symptoms):
                relevant_chunks.append(chunk)
        
        if relevant_chunks:
            section_content = ' '.join(relevant_chunks)
            
            section = {
                'id': f"symptom_{uuid.uuid4().hex[:8]}",
                'content': section_content,
                'section_type': 'symptoms',
                'metadata': {
                    'original_title': document.get('title', ''),
                    'source': document.get('metadata', {}).get('source', ''),
                    'symptoms': symptoms,
                    'emergency_indicators': document.get('emergency_indicators', []),
                    'relevance_type': 'symptom_focused'
                }
            }
            sections.append(section)
        
        return sections
    
    def _create_emergency_sections(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create sections focused on emergency medical information."""
        sections = []
        
        emergency_indicators = document.get('emergency_indicators', [])
        if not emergency_indicators:
            return sections
        
        relevant_chunks = []
        
        # Find chunks that mention emergency indicators
        for chunk in document.get('chunks', []):
            chunk_lower = chunk.lower()
            if any(indicator.lower() in chunk_lower for indicator in emergency_indicators):
                relevant_chunks.append(chunk)
        
        # Also include chunks with emergency keywords
        emergency_keywords = ['emergency', 'immediate', 'urgent', 'serious', 'critical', 'danger']
        for chunk in document.get('chunks', []):
            chunk_lower = chunk.lower()
            if any(keyword in chunk_lower for keyword in emergency_keywords):
                if chunk not in relevant_chunks:
                    relevant_chunks.append(chunk)
        
        if relevant_chunks:
            section_content = ' '.join(relevant_chunks)
            
            section = {
                'id': f"emergency_{uuid.uuid4().hex[:8]}",
                'content': section_content,
                'section_type': 'emergency',
                'metadata': {
                    'original_title': document.get('title', ''),
                    'source': document.get('metadata', {}).get('source', ''),
                    'emergency_indicators': emergency_indicators,
                    'symptoms': document.get('symptoms', []),
                    'relevance_type': 'emergency_focused',
                    'priority': 'high'
                }
            }
            sections.append(section)
        
        return sections
    
    def _create_general_sections(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create general medical information sections."""
        sections = []
        
        chunks = document.get('chunks', [])
        if not chunks:
            return sections
        
        # Group chunks for better context (2-3 chunks per section)
        chunk_groups = []
        for i in range(0, len(chunks), 2):
            chunk_group = chunks[i:i+3]  # Take 2-3 chunks
            chunk_groups.append(chunk_group)
        
        for i, chunk_group in enumerate(chunk_groups):
            section_content = ' '.join(chunk_group)
            
            section = {
                'id': f"general_{uuid.uuid4().hex[:8]}",
                'content': section_content,
                'section_type': 'general',
                'metadata': {
                    'original_title': document.get('title', ''),
                    'source': document.get('metadata', {}).get('source', ''),
                    'symptoms': document.get('symptoms', []),
                    'emergency_indicators': document.get('emergency_indicators', []),
                    'relevance_type': 'general_medical',
                    'section_index': i
                }
            }
            sections.append(section)
        
        return sections
    
    def enrich_with_metadata(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich sections with metadata for better searchability.
        
        Args:
            sections: List of medical sections
            
        Returns:
            Enriched sections with additional metadata
        """
        enriched_sections = []
        
        for section in sections:
            content = section['content']
            
            # Extract keywords
            keywords = self._extract_keywords(content)
            
            # Determine medical context
            medical_context = self._determine_medical_context(content, section.get('metadata', {}))
            
            # Add enrichment metadata
            section['metadata'].update({
                'keywords': keywords,
                'medical_context': medical_context,
                'content_length': len(content),
                'processed_at': datetime.now().isoformat(),
                'language': self._detect_language(content)
            })
            
            enriched_sections.append(section)
        
        return enriched_sections
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords from content."""
        content_lower = content.lower()
        
        # Extract medical keywords
        found_keywords = []
        
        # Check English medical keywords
        for keyword in self.medical_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        # Check Hindi medical keywords
        for keyword in self.hindi_medical_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        # Extract symptom names
        for symptom in self.malaria_constants.EARLY_SYMPTOMS | self.malaria_constants.SEVERE_SYMPTOMS | self.malaria_constants.EMERGENCY_SYMPTOMS:
            if symptom.lower() in content_lower:
                found_keywords.append(symptom)
        
        # Extract key medical terms using regex
        medical_patterns = [
            r'\b(?:fever|temperature)\s*(?:of\s*)?(?:\d+)?\s*(?:degrees?|°)?[CF]?\b',
            r'\b(?:blood\s*pressure|bp)\s*(?:\d+\/\d+)?\b',
            r'\b(?:heart\s*rate|pulse)\s*(?:\d+)?\s*(?:bpm)?\b'
        ]
        
        for pattern in medical_patterns:
            matches = re.findall(pattern, content_lower)
            found_keywords.extend(matches)
        
        return list(set(found_keywords))  # Remove duplicates
    
    def _determine_medical_context(self, content: str, metadata: Dict[str, Any]) -> List[str]:
        """Determine the medical context of content."""
        contexts = []
        
        content_lower = content.lower()
        
        # Symptom context
        if metadata.get('symptoms') or any(s in content_lower for s in ['symptom', 'sign', 'feel', 'experience']):
            contexts.append('symptoms')
        
        # Emergency context
        if metadata.get('emergency_indicators') or any(e in content_lower for e in ['emergency', 'urgent', 'immediate', 'critical']):
            contexts.append('emergency')
        
        # Prevention context
        if any(p in content_lower for p in ['prevent', 'avoid', 'protection', 'precaution']):
            contexts.append('prevention')
        
        # Treatment context
        if any(t in content_lower for t in ['treatment', 'therapy', 'medicine', 'drug', 'medication']):
            contexts.append('treatment')
        
        # Diagnosis context
        if any(d in content_lower for d in ['diagnosis', 'test', 'examination', 'check']):
            contexts.append('diagnosis')
        
        return contexts if contexts else ['general']
    
    def _detect_language(self, content: str) -> str:
        """Simple language detection for English/Hindi."""
        # Count Hindi characters (Devanagari script)
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', content))
        total_chars = len(content.replace(' ', ''))
        
        if total_chars == 0:
            return 'unknown'
        
        hindi_ratio = hindi_chars / total_chars
        
        if hindi_ratio > 0.3:
            return 'hindi'
        elif hindi_ratio > 0.1:
            return 'mixed'
        else:
            return 'english'
    
    def filter_by_medical_relevance(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter sections by medical relevance.
        
        Args:
            sections: List of enriched sections
            
        Returns:
            Filtered list of medically relevant sections
        """
        relevant_sections = []
        
        for section in sections:
            relevance_score = self._calculate_medical_relevance(section)
            
            # Keep sections with sufficient medical relevance
            if relevance_score >= 0.3:  # Configurable threshold
                section['metadata']['relevance_score'] = relevance_score
                relevant_sections.append(section)
            else:
                logger.debug(f"Filtered out section with low relevance: {relevance_score}")
        
        # Sort by relevance score (highest first)
        relevant_sections.sort(key=lambda x: x['metadata']['relevance_score'], reverse=True)
        
        return relevant_sections
    
    def _calculate_medical_relevance(self, section: Dict[str, Any]) -> float:
        """Calculate medical relevance score for a section."""
        content = section['content'].lower()
        metadata = section['metadata']
        
        score = 0.0
        
        # Base score for section type
        section_type = section.get('section_type', 'general')
        if section_type == 'emergency':
            score += 0.5
        elif section_type == 'symptoms':
            score += 0.4
        elif section_type == 'general':
            score += 0.2
        
        # Score for medical keywords
        keywords = metadata.get('keywords', [])
        medical_keyword_count = sum(1 for k in keywords if k in self.medical_keywords or k in self.hindi_medical_keywords)
        score += min(medical_keyword_count * 0.1, 0.3)
        
        # Score for symptoms
        symptom_count = len(metadata.get('symptoms', []))
        score += min(symptom_count * 0.05, 0.2)
        
        # Score for emergency indicators
        emergency_count = len(metadata.get('emergency_indicators', []))
        score += min(emergency_count * 0.1, 0.3)
        
        # Score for medical contexts
        contexts = metadata.get('medical_context', [])
        context_score = len([c for c in contexts if c != 'general']) * 0.05
        score += min(context_score, 0.15)
        
        # Penalty for very short content
        content_length = len(content)
        if content_length < 50:
            score *= 0.7
        elif content_length < 20:
            score *= 0.5
        
        # Bonus for malaria-specific content
        if 'malaria' in content:
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0