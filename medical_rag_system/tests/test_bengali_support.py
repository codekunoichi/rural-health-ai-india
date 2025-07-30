"""
Test Bengali language support across the Medical RAG System.
Tests symptom extraction, emergency detection, and response generation in Bengali.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection.data_processor import DataProcessor
from src.rag_system.query_processor import MedicalQueryProcessor
from src.rag_system.response_generator import MedicalResponseGenerator
from config.medical_constants import MalariaConstants


class TestBengaliLanguageSupport(unittest.TestCase):
    """Test Bengali language support in the Medical RAG System."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_processor = DataProcessor()
        self.query_processor = MedicalQueryProcessor()
        self.response_generator = MedicalResponseGenerator()
        self.constants = MalariaConstants()
    
    def test_bengali_symptom_extraction(self):
        """Test extraction of Bengali symptoms."""
        # Test basic Bengali symptoms
        bengali_query = "আমার জ্বর এবং মাথাব্যথা আছে"
        symptoms = self.data_processor.extract_symptoms(bengali_query)
        
        # Should extract fever and headache
        self.assertIn("fever", symptoms)
        self.assertIn("headache", symptoms)
        self.assertEqual(len(symptoms), 2)
    
    def test_bengali_emergency_detection(self):
        """Test emergency detection with Bengali symptoms."""
        # Test emergency symptoms in Bengali
        emergency_query = "আমার অজ্ঞান হওয়ার মতো অবস্থা এবং শ্বাসকষ্ট"
        emergency_indicators = self.data_processor.detect_emergency_indicators(emergency_query)
        
        # Should detect emergency indicators (Bengali terms are returned)
        self.assertTrue(len(emergency_indicators) > 0)
        self.assertIn("অজ্ঞান", emergency_indicators)
        self.assertIn("শ্বাসকষ্ট", emergency_indicators)
    
    def test_bengali_query_processing(self):
        """Test complete Bengali query processing."""
        bengali_query = "আমার তিন দিন ধরে জ্বর এবং কাঁপুনি হচ্ছে"
        result = self.query_processor.process_query(bengali_query)
        
        # Check basic processing
        self.assertEqual(result['original_query'], bengali_query)
        self.assertFalse(result['emergency_detected'])
        self.assertEqual(result['query_type'], 'symptom_inquiry')
        
        # Check symptom extraction
        self.assertIn("fever", result['symptoms'])
        self.assertIn("chills", result['symptoms'])
        
        # Check language detection
        self.assertEqual(result['metadata']['language'], 'bengali')
    
    def test_bengali_language_detection(self):
        """Test Bengali language detection in queries."""
        test_cases = [
            ("আমার জ্বর আছে", "bengali"),
            ("I have fever", "english"),
            ("मुझे बुखार है", "hindi"),
            ("আমার fever আছে", "mixed"),  # Mixed Bengali-English
        ]
        
        for query, expected_lang in test_cases:
            result = self.query_processor.process_query(query)
            detected_lang = result['metadata']['language']
            self.assertEqual(detected_lang, expected_lang, 
                           f"Failed for query: {query}, expected: {expected_lang}, got: {detected_lang}")
    
    def test_bengali_complex_symptoms(self):
        """Test complex Bengali symptom descriptions."""
        complex_query = "আমার শরীর খুব খারাপ লাগছে, পেট ব্যথা, বমি বমি ভাব এবং দুর্বলতা অনুভব করছি"
        symptoms = self.data_processor.extract_symptoms(complex_query)
        
        expected_symptoms = ["feeling unwell", "stomach pain", "nausea", "weakness"]
        for expected in expected_symptoms:
            self.assertIn(expected, symptoms, 
                         f"Expected symptom '{expected}' not found in extracted symptoms: {symptoms}")
    
    def test_bengali_emergency_query_processing(self):
        """Test emergency query processing in Bengali."""
        emergency_query = "রোগীর অচেতন অবস্থা এবং খিঁচুনি হচ্ছে, অবিলম্বে সাহায্য প্রয়োজন"
        result = self.query_processor.process_query(emergency_query)
        
        # Should detect emergency
        self.assertTrue(result['emergency_detected'])
        self.assertEqual(result['query_type'], 'emergency')
        self.assertTrue(len(result['emergency_indicators']) > 0)
        
        # Check for emergency symptoms (Bengali terms are returned)
        self.assertIn("অচেতন অবস্থা", result['emergency_indicators'])
        self.assertIn("খিঁচুনি", result['emergency_indicators'])
    
    @patch('src.rag_system.response_generator.MedicalResponseGenerator._extract_sources')
    @patch('src.rag_system.response_generator.MedicalResponseGenerator._calculate_response_confidence')
    def test_bengali_disclaimer_selection(self, mock_confidence, mock_sources):
        """Test that Bengali disclaimers are selected for Bengali queries."""
        mock_confidence.return_value = 0.8
        mock_sources.return_value = ["WHO", "CDC"]
        
        # Create query info with Bengali language detected
        query_info = {
            'symptoms': ['fever', 'headache'],
            'query_type': 'symptom_inquiry',
            'emergency_detected': False,
            'metadata': {'language': 'bengali'}
        }
        
        # Mock retrieval context
        retrieval_context = {
            'query': query_info,
            'documents': [{'document': {'content': 'test content', 'metadata': {}}}],
            'retrieval_metadata': {'confidence': 0.7}
        }
        
        response = self.response_generator.generate_response(retrieval_context)
        
        # Check that Bengali disclaimers are used
        disclaimers = response['disclaimers']
        self.assertTrue(len(disclaimers) > 0)
        
        # Should contain Bengali text
        bengali_disclaimer = disclaimers[0]
        self.assertIn("এই তথ্য শুধুমাত্র শিক্ষামূলক", bengali_disclaimer)
    
    def test_bengali_symptom_constants(self):
        """Test that Bengali symptom constants are properly defined."""
        # Check that key symptoms are present
        key_symptoms = [
            "জ্বর",      # fever
            "মাথাব্যথা",   # headache
            "কাঁপুনি",    # chills
            "অজ্ঞান",    # unconsciousness
            "শ্বাসকষ্ট"   # difficulty breathing
        ]
        
        for symptom in key_symptoms:
            self.assertIn(symptom, self.constants.BENGALI_SYMPTOMS,
                         f"Bengali symptom '{symptom}' not found in constants")
        
        # Check that translations are correct
        self.assertEqual(self.constants.BENGALI_SYMPTOMS["জ্বর"], "fever")
        self.assertEqual(self.constants.BENGALI_SYMPTOMS["মাথাব্যথা"], "headache")
        self.assertEqual(self.constants.BENGALI_SYMPTOMS["অজ্ঞান"], "unconsciousness")
    
    def test_bengali_disclaimer_constants(self):
        """Test that Bengali disclaimer constants are properly defined."""
        required_disclaimers = ['general', 'emergency', 'pregnancy']
        
        for disclaimer_type in required_disclaimers:
            self.assertIn(disclaimer_type, self.constants.BENGALI_DISCLAIMERS,
                         f"Bengali disclaimer '{disclaimer_type}' not found")
            
            disclaimer_text = self.constants.BENGALI_DISCLAIMERS[disclaimer_type]
            self.assertTrue(len(disclaimer_text) > 50,
                          f"Bengali disclaimer '{disclaimer_type}' seems too short")
            
            # Should contain Bengali characters
            bengali_char_found = any('\u0980' <= char <= '\u09FF' for char in disclaimer_text)
            self.assertTrue(bengali_char_found,
                          f"Bengali disclaimer '{disclaimer_type}' doesn't contain Bengali characters")
    
    def test_mixed_language_handling(self):
        """Test handling of mixed Bengali-English queries."""
        mixed_query = "আমার fever এবং headache আছে"
        symptoms = self.data_processor.extract_symptoms(mixed_query)
        
        # Should extract both English and Bengali symptoms
        self.assertIn("fever", symptoms)
        
        # Test query processing
        result = self.query_processor.process_query(mixed_query)
        self.assertEqual(result['metadata']['language'], 'mixed')
    
    def test_bengali_text_cleaning(self):
        """Test text cleaning preserves Bengali characters."""
        bengali_text = "আমার জ্বর আছে!!! কী করব???"
        cleaned = self.data_processor.clean_text(bengali_text)
        
        # Should preserve Bengali characters
        self.assertIn("আমার", cleaned)
        self.assertIn("জ্বর", cleaned)
        self.assertIn("আছে", cleaned)
        
        # Should clean excessive punctuation
        self.assertNotIn("!!!", cleaned)
        self.assertNotIn("???", cleaned)
    
    def test_bengali_unicode_range_detection(self):
        """Test Unicode range detection for Bengali characters."""
        # Test pure Bengali
        bengali_only = "আমার জ্বর আছে"
        result = self.query_processor._extract_metadata(bengali_only)
        self.assertEqual(result['language'], 'bengali')
        
        # Test with some Bengali characters (less than 30% threshold)
        mostly_english = "I have জ্বর today"
        result = self.query_processor._extract_metadata(mostly_english)
        self.assertNotEqual(result['language'], 'bengali')


class TestBengaliIntegration(unittest.TestCase):
    """Integration tests for Bengali language support."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.query_processor = MedicalQueryProcessor()
        self.response_generator = MedicalResponseGenerator()
    
    @patch('src.rag_system.response_generator.MedicalResponseGenerator._extract_sources')
    @patch('src.rag_system.response_generator.MedicalResponseGenerator._calculate_response_confidence')
    def test_end_to_end_bengali_query(self, mock_confidence, mock_sources):
        """Test end-to-end processing of a Bengali medical query."""
        mock_confidence.return_value = 0.75
        mock_sources.return_value = ["WHO"]
        
        # Bengali query: "I have had fever and body aches for 3 days"
        bengali_query = "আমার তিন দিন ধরে জ্বর এবং শরীর ব্যথা আছে"
        
        # Process query
        query_result = self.query_processor.process_query(bengali_query)
        
        # Verify query processing
        self.assertEqual(query_result['metadata']['language'], 'bengali')
        self.assertIn('fever', query_result['symptoms'])
        self.assertIn('body aches', query_result['symptoms'])
        
        # Mock document retrieval
        mock_documents = [{
            'document': {
                'content': 'Fever and body aches can be symptoms of various conditions including malaria.',
                'metadata': {'source': 'who'}
            },
            'final_score': 0.8
        }]
        
        # Generate response
        retrieval_context = {
            'query': query_result,
            'documents': mock_documents,
            'retrieval_metadata': {'confidence': 0.7}
        }
        
        response = self.response_generator.generate_response(retrieval_context)
        
        # Verify response contains Bengali disclaimers
        self.assertTrue(any('শিক্ষামূলক' in disclaimer for disclaimer in response['disclaimers']))
        self.assertEqual(response['response_type'], 'symptom_guidance')
        self.assertFalse(response['emergency_alert'])


if __name__ == '__main__':
    unittest.main()