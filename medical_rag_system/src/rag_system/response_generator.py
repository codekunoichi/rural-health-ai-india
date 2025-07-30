from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from config.medical_constants import MalariaConstants, ResponseTemplates
from config.settings import Settings

logger = logging.getLogger(__name__)

class MedicalResponseGenerator:
    """
    Generate medical responses based on retrieved documents and query context.
    Includes safety measures, disclaimers, and context-appropriate formatting.
    """
    
    def __init__(self):
        """Initialize the medical response generator."""
        self.malaria_constants = MalariaConstants()
        self.response_templates = ResponseTemplates()
        self.max_response_length = Settings.RESPONSE_MAX_LENGTH
        
        logger.info("MedicalResponseGenerator initialized")
    
    def generate_response(self, retrieval_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete medical response based on retrieval context.
        
        Args:
            retrieval_context: Context from retrieval engine with query and documents
            
        Returns:
            Complete response with text, metadata, and safety information
        """
        logger.info("Generating medical response")
        
        try:
            query_info = retrieval_context.get('query', {})
            documents = retrieval_context.get('documents', [])
            retrieval_metadata = retrieval_context.get('retrieval_metadata', {})
            
            # Determine response type and strategy
            response_type = self._determine_response_type(query_info, documents)
            
            # Generate appropriate response
            if response_type == 'emergency_alert':
                response_content = self.generate_emergency_response(query_info, documents)
            elif response_type == 'symptom_guidance':
                response_content = self.generate_symptom_response(query_info, documents)
            elif response_type == 'insufficient_information':
                response_content = self._generate_insufficient_info_response(query_info)
            else:
                response_content = self._generate_general_response(query_info, documents)
            
            # Add medical disclaimers
            disclaimers = self.add_medical_disclaimers(query_info, response_type)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(query_info, documents, response_type)
            
            # Extract sources
            sources = self._extract_sources(documents)
            
            # Calculate response confidence
            confidence = self._calculate_response_confidence(
                query_info, documents, retrieval_metadata, response_type
            )
            
            # Build complete response
            complete_response = {
                'response_text': response_content,
                'response_type': response_type,
                'confidence': confidence,
                'sources': sources,
                'disclaimers': disclaimers,
                'recommendations': recommendations,
                'emergency_alert': response_type == 'emergency_alert',
                'generated_at': datetime.now().isoformat(),
                'metadata': {
                    'query_type': query_info.get('query_type'),
                    'symptoms_addressed': query_info.get('symptoms', []),
                    'documents_used': len(documents),
                    'response_length': len(response_content)
                }
            }
            
            logger.info(f"Generated {response_type} response with confidence {confidence:.2f}")
            return complete_response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return self._generate_error_response(str(e))
    
    def generate_emergency_response(self, query_info: Dict[str, Any], 
                                   documents: List[Dict[str, Any]]) -> str:
        """
        Generate emergency medical response.
        
        Args:
            query_info: Processed query information
            documents: Retrieved relevant documents
            
        Returns:
            Emergency response text
        """
        emergency_indicators = query_info.get('emergency_indicators', [])
        symptoms = query_info.get('symptoms', [])
        
        # Build emergency response
        response_parts = []
        
        response_parts.append("🚨 MEDICAL EMERGENCY DETECTED 🚨")
        response_parts.append("")
        
        # Describe the emergency situation
        if emergency_indicators:
            indicators_text = ', '.join(emergency_indicators[:3])  # Limit to avoid too long
            response_parts.append(f"The symptoms '{indicators_text}' may indicate a serious medical emergency.")
        else:
            response_parts.append("The described symptoms may indicate a serious medical emergency.")
        
        # Immediate actions
        response_parts.append("")
        response_parts.append("IMMEDIATE ACTION REQUIRED:")
        response_parts.append("• Go to the nearest hospital or emergency medical facility immediately")
        response_parts.append("• Call emergency services if available (dial 108 in India)")
        response_parts.append("• Do not delay seeking medical care")
        response_parts.append("• If possible, have someone accompany the patient")
        
        # Add relevant medical information from documents
        if documents:
            medical_info = self._extract_emergency_info(documents)
            if medical_info:
                response_parts.append("")
                response_parts.append("IMPORTANT MEDICAL INFORMATION:")
                response_parts.append(medical_info)
        
        return '\n'.join(response_parts)
    
    def generate_symptom_response(self, query_info: Dict[str, Any], 
                                 documents: List[Dict[str, Any]]) -> str:
        """
        Generate symptom-based medical guidance response.
        
        Args:
            query_info: Processed query information
            documents: Retrieved relevant documents
            
        Returns:
            Symptom guidance response text
        """
        symptoms = query_info.get('symptoms', [])
        
        # Build symptom response
        response_parts = []
        
        # Symptom acknowledgment
        if symptoms:
            if len(symptoms) == 1:
                response_parts.append(f"Based on your symptom of {symptoms[0]}, here's what you should know:")
            else:
                symptoms_text = ', '.join(symptoms[:-1])
                response_parts.append(f"Based on your symptoms of {symptoms_text} and {symptoms[-1]}, here's what you should know:")
        else:
            response_parts.append("Based on your health concern, here's relevant medical information:")
        
        response_parts.append("")
        
        # Extract and summarize medical information
        medical_summary = self._extract_medical_summary(documents, symptoms)
        if medical_summary:
            response_parts.append(medical_summary)
            response_parts.append("")
        
        # Add malaria-specific information if relevant
        if self._is_malaria_related(symptoms, documents):
            malaria_info = self._generate_malaria_guidance(symptoms)
            if malaria_info:
                response_parts.append("MALARIA INFORMATION:")
                response_parts.append(malaria_info)
                response_parts.append("")
        
        # Duration and severity context
        duration = query_info.get('metadata', {}).get('duration')
        if duration:
            response_parts.append(f"Since you've had these symptoms for {duration}, it's important to seek medical evaluation.")
            response_parts.append("")
        
        return '\n'.join(response_parts)
    
    def add_medical_disclaimers(self, query_info: Dict[str, Any], 
                               response_type: str) -> List[str]:
        """
        Add appropriate medical disclaimers based on context and language.
        
        Args:
            query_info: Query information
            response_type: Type of response being generated
            
        Returns:
            List of disclaimer strings
        """
        disclaimers = []
        
        # Detect query language from metadata
        query_language = query_info.get('metadata', {}).get('language', 'english')
        
        # Select appropriate disclaimer set based on language
        if query_language == 'bengali':
            disclaimer_set = self.malaria_constants.BENGALI_DISCLAIMERS
        elif query_language == 'hindi':
            disclaimer_set = self.malaria_constants.HINDI_DISCLAIMERS
        else:
            # Default to English for 'english', 'mixed', or undetected languages
            disclaimer_set = self.malaria_constants.DISCLAIMERS
        
        # Always include general disclaimer
        disclaimers.append(disclaimer_set['general'])
        
        # Emergency-specific disclaimer
        if response_type == 'emergency_alert':
            disclaimers.append(disclaimer_set['emergency'])
        
        # Pregnancy-specific disclaimer
        special_populations = query_info.get('metadata', {}).get('special_populations', [])
        if 'pregnancy' in special_populations:
            disclaimers.append(disclaimer_set['pregnancy'])
        
        return disclaimers
    
    def _determine_response_type(self, query_info: Dict[str, Any], 
                                documents: List[Dict[str, Any]]) -> str:
        """
        Determine the type of response to generate.
        
        Args:
            query_info: Query information
            documents: Retrieved documents
            
        Returns:
            Response type string
        """
        # Emergency takes priority
        if query_info.get('emergency_detected', False):
            return 'emergency_alert'
        
        # Check if we have sufficient information
        if not documents or len(documents) == 0:
            return 'insufficient_information'
        
        # Symptom-based response
        if query_info.get('query_type') == 'symptom_inquiry':
            return 'symptom_guidance'
        
        # Prevention inquiry
        if query_info.get('query_type') == 'prevention_inquiry':
            return 'prevention_guidance'
        
        # Default to general medical response
        return 'general_medical'
    
    def _generate_recommendations(self, query_info: Dict[str, Any], 
                                 documents: List[Dict[str, Any]], 
                                 response_type: str) -> List[str]:
        """
        Generate medical recommendations based on context.
        
        Args:
            query_info: Query information
            documents: Retrieved documents
            response_type: Type of response
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if response_type == 'emergency_alert':
            recommendations.extend([
                "Seek immediate emergency medical care",
                "Do not delay treatment",
                "Call emergency services if available"
            ])
        
        elif response_type == 'symptom_guidance':
            symptoms = query_info.get('symptoms', [])
            
            # General medical care recommendation
            recommendations.append("Consult with a healthcare provider for proper evaluation")
            
            # Symptom-specific recommendations
            if any(symptom in ['fever', 'high fever'] for symptom in symptoms):
                recommendations.extend([
                    "Monitor your temperature regularly",
                    "Stay hydrated with plenty of fluids",
                    "Get medical testing if fever persists beyond 2-3 days"
                ])
            
            # Malaria-specific recommendations
            if self._is_malaria_related(symptoms, documents):
                recommendations.extend([
                    "Get tested for malaria with a blood test",
                    "Avoid self-medication",
                    "Seek medical attention within 24 hours if in a malaria-endemic area"
                ])
            
            # General symptom management
            recommendations.append("Monitor symptoms and seek care if they worsen")
        
        else:
            # Default recommendations
            recommendations.extend([
                "Consult with a qualified healthcare provider",
                "Follow professional medical advice",
                "Seek care if symptoms persist or worsen"
            ])
        
        return recommendations
    
    def _extract_sources(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Extract and format source attributions.
        
        Args:
            documents: Retrieved documents
            
        Returns:
            List of formatted source strings
        """
        sources = set()
        
        for doc_result in documents:
            document = doc_result.get('document', {})
            metadata = document.get('metadata', {})
            source = metadata.get('source', '')
            
            if source:
                # Use friendly source names
                source_names = self.malaria_constants.DATA_SOURCES
                friendly_name = source_names.get(source, source.title())
                sources.add(friendly_name)
        
        return list(sources)
    
    def _calculate_response_confidence(self, query_info: Dict[str, Any],
                                      documents: List[Dict[str, Any]],
                                      retrieval_metadata: Dict[str, Any],
                                      response_type: str) -> float:
        """
        Calculate confidence in the generated response.
        
        Args:
            query_info: Query information
            documents: Retrieved documents
            retrieval_metadata: Retrieval metadata
            response_type: Response type
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.0
        
        # Base confidence from query processing
        query_confidence = query_info.get('confidence', 0.0)
        confidence += query_confidence * 0.3
        
        # Confidence from retrieval quality
        retrieval_confidence = retrieval_metadata.get('confidence', 0.0)
        confidence += retrieval_confidence * 0.4
        
        # Confidence from document quality
        if documents:
            doc_scores = [doc.get('final_score', 0.0) for doc in documents]
            avg_doc_score = sum(doc_scores) / len(doc_scores)
            confidence += avg_doc_score * 0.2
        
        # Response type confidence
        if response_type == 'emergency_alert':
            confidence += 0.1  # High confidence for clear emergencies
        elif response_type == 'insufficient_information':
            confidence = max(confidence * 0.5, 0.1)  # Lower confidence
        
        return min(confidence, 1.0)
    
    def _extract_emergency_info(self, documents: List[Dict[str, Any]]) -> str:
        """
        Extract emergency-relevant information from documents.
        
        Args:
            documents: Retrieved documents
            
        Returns:
            Emergency information text
        """
        emergency_info = []
        
        for doc_result in documents[:2]:  # Use top 2 documents
            document = doc_result.get('document', {})
            content = document.get('content', '')
            
            # Extract sentences mentioning emergency terms
            sentences = content.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if any(term in sentence.lower() for term in ['emergency', 'immediate', 'urgent', 'serious']):
                    if len(sentence) < 150:  # Reasonable length
                        emergency_info.append(sentence + '.')
                        break
        
        return ' '.join(emergency_info[:2])  # Limit to avoid too long response
    
    def _extract_medical_summary(self, documents: List[Dict[str, Any]], 
                                symptoms: List[str]) -> str:
        """
        Extract and summarize medical information from documents.
        
        Args:
            documents: Retrieved documents
            symptoms: Query symptoms
            
        Returns:
            Medical summary text
        """
        if not documents:
            return ""
        
        # Take content from top documents
        content_pieces = []
        
        for doc_result in documents[:3]:  # Use top 3 documents
            document = doc_result.get('document', {})
            content = document.get('content', '')
            
            # Extract most relevant sentences
            sentences = content.split('.')
            relevant_sentences = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 20:  # Skip very short sentences
                    continue
                
                # Prioritize sentences mentioning query symptoms
                if symptoms and any(symptom.lower() in sentence.lower() for symptom in symptoms):
                    relevant_sentences.append(sentence + '.')
                elif len(relevant_sentences) < 1:  # Include at least one sentence
                    relevant_sentences.append(sentence + '.')
            
            content_pieces.extend(relevant_sentences[:2])  # Max 2 sentences per document
        
        # Combine and limit length
        summary = ' '.join(content_pieces)
        
        # Truncate if too long
        if len(summary) > 300:
            summary = summary[:297] + '...'
        
        return summary
    
    def _is_malaria_related(self, symptoms: List[str], documents: List[Dict[str, Any]]) -> bool:
        """
        Check if the query/response is malaria-related.
        
        Args:
            symptoms: Query symptoms
            documents: Retrieved documents
            
        Returns:
            True if malaria-related
        """
        # Check symptoms
        malaria_symptoms = {'fever', 'chills', 'headache', 'muscle aches', 'nausea', 'vomiting'}
        query_symptoms_lower = {s.lower() for s in symptoms}
        
        if len(query_symptoms_lower & malaria_symptoms) >= 2:
            return True
        
        # Check document content
        for doc_result in documents[:2]:
            document = doc_result.get('document', {})
            content = document.get('content', '').lower()
            if 'malaria' in content:
                return True
        
        return False
    
    def _generate_malaria_guidance(self, symptoms: List[str]) -> str:
        """
        Generate malaria-specific guidance.
        
        Args:
            symptoms: Query symptoms
            
        Returns:
            Malaria guidance text
        """
        guidance_parts = []
        
        # Basic malaria information
        guidance_parts.append("Malaria is a serious disease transmitted by infected mosquitoes.")
        
        # Symptom-specific guidance
        symptom_set = {s.lower() for s in symptoms}
        
        if 'fever' in symptom_set:
            guidance_parts.append("Fever is the most common malaria symptom and requires prompt medical attention.")
        
        if symptom_set & {'chills', 'sweating'}:
            guidance_parts.append("Chills and sweating cycles are characteristic of malaria.")
        
        # General malaria advice
        guidance_parts.append("Early diagnosis and treatment are crucial for preventing complications.")
        
        return ' '.join(guidance_parts)
    
    def _generate_insufficient_info_response(self, query_info: Dict[str, Any]) -> str:
        """
        Generate response when insufficient information is available.
        
        Args:
            query_info: Query information
            
        Returns:
            Insufficient information response text
        """
        response_parts = []
        
        response_parts.append("I'm unable to provide specific medical information for your query.")
        response_parts.append("")
        response_parts.append("This could be because:")
        response_parts.append("• The query is not medical in nature")
        response_parts.append("• Insufficient medical information is available")
        response_parts.append("• The symptoms described are too general")
        response_parts.append("")
        response_parts.append("For any health concerns, please consult with a qualified healthcare provider who can properly evaluate your situation.")
        
        return '\n'.join(response_parts)
    
    def _generate_general_response(self, query_info: Dict[str, Any], 
                                  documents: List[Dict[str, Any]]) -> str:
        """
        Generate general medical response.
        
        Args:
            query_info: Query information
            documents: Retrieved documents
            
        Returns:
            General response text
        """
        if not documents:
            return self._generate_insufficient_info_response(query_info)
        
        # Extract information from documents
        medical_info = self._extract_medical_summary(documents, query_info.get('symptoms', []))
        
        response_parts = []
        response_parts.append("Based on available medical information:")
        response_parts.append("")
        
        if medical_info:
            response_parts.append(medical_info)
            response_parts.append("")
        
        response_parts.append("For personalized medical advice and proper evaluation, please consult with a healthcare professional.")
        
        return '\n'.join(response_parts)
    
    def _generate_error_response(self, error_msg: str) -> Dict[str, Any]:
        """
        Generate error response when response generation fails.
        
        Args:
            error_msg: Error message
            
        Returns:
            Error response structure
        """
        return {
            'response_text': "I apologize, but I'm unable to generate a response at this time due to a technical issue. Please consult with a healthcare provider for your medical concerns.",
            'response_type': 'error',
            'confidence': 0.0,
            'sources': [],
            'disclaimers': [self.malaria_constants.DISCLAIMERS['general']],
            'recommendations': ["Consult with a qualified healthcare provider"],
            'emergency_alert': False,
            'generated_at': datetime.now().isoformat(),
            'metadata': {
                'error': error_msg
            }
        }