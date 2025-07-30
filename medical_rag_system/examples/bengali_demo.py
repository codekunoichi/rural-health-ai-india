#!/usr/bin/env python3
"""
Bengali Language Support Demo for Medical RAG System

This demo showcases the system's ability to process Bengali medical queries,
extract symptoms, detect emergencies, and provide appropriate responses
in Bengali language.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection.data_processor import DataProcessor
from src.rag_system.query_processor import MedicalQueryProcessor
from src.rag_system.response_generator import MedicalResponseGenerator
from config.medical_constants import MalariaConstants


def print_banner():
    """Print demo banner."""
    print("=" * 80)
    print("     Medical RAG System - Bengali Language Support Demo")
    print("     বাংলা ভাষায় চিকিৎসা সহায়তা সিস্টেম")
    print("=" * 80)
    print()


def demo_symptom_extraction():
    """Demonstrate Bengali symptom extraction."""
    print("🔍 Bengali Symptom Extraction Demo")
    print("-" * 50)
    
    processor = DataProcessor()
    
    test_queries = [
        "আমার জ্বর এবং মাথাব্যথা আছে",
        "তিন দিন ধরে কাঁপুনি এবং শরীর ব্যথা হচ্ছে",
        "পেট ব্যথা, বমি বমি ভাব এবং দুর্বলতা অনুভব করছি",
        "শ্বাসকষ্ট এবং বুকে ব্যথা হচ্ছে",
        "গুরুতর মাথাব্যথা এবং জ্ঞান হারানোর মতো অবস্থা"
    ]
    
    for query in test_queries:
        print(f"\nQuery (Bengali): {query}")
        symptoms = processor.extract_symptoms(query)
        print(f"Extracted Symptoms: {symptoms}")
        
        # Check for emergency indicators
        emergency_indicators = processor.detect_emergency_indicators(query)
        if emergency_indicators:
            print(f"⚠️  Emergency Indicators: {emergency_indicators}")
    
    print("\n" + "="*80 + "\n")


def demo_query_processing():
    """Demonstrate Bengali query processing."""
    print("🧠 Bengali Query Processing Demo")
    print("-" * 50)
    
    processor = MedicalQueryProcessor()
    
    test_cases = [
        {
            "query": "আমার দুই দিন ধরে জ্বর এবং কাঁপুনি",
            "description": "Common fever symptoms"
        },
        {
            "query": "রোগীর অচেতন অবস্থা এবং খিঁচুনি হচ্ছে",
            "description": "Emergency situation"
        },
        {
            "query": "ম্যালেরিয়া থেকে কীভাবে বাঁচা যায়?",
            "description": "Prevention inquiry"
        },
        {
            "query": "গর্ভবতী মহিলার জ্বর হলে কী করতে হবে?",
            "description": "Pregnancy-related query"
        }
    ]
    
    for case in test_cases:
        print(f"\n📝 Test Case: {case['description']}")
        print(f"Query (Bengali): {case['query']}")
        
        result = processor.process_query(case['query'])
        
        print(f"   Language Detected: {result['metadata']['language']}")
        print(f"   Query Type: {result['query_type']}")
        print(f"   Symptoms Found: {result['symptoms']}")
        print(f"   Emergency Detected: {result['emergency_detected']}")
        if result['emergency_detected']:
            print(f"   Emergency Indicators: {result['emergency_indicators']}")
        print(f"   Confidence Score: {result['confidence']:.2f}")
        
        # Check for special populations
        special_pops = result['metadata'].get('special_populations', [])
        if special_pops:
            print(f"   Special Populations: {special_pops}")
    
    print("\n" + "="*80 + "\n")


def demo_response_generation():
    """Demonstrate Bengali response generation with disclaimers."""
    print("💬 Bengali Response Generation Demo")
    print("-" * 50)
    
    response_generator = MedicalResponseGenerator()
    constants = MalariaConstants()
    
    # Test different response scenarios
    scenarios = [
        {
            "name": "Regular Symptom Query",
            "query_info": {
                'symptoms': ['fever', 'headache'],
                'query_type': 'symptom_inquiry',
                'emergency_detected': False,
                'metadata': {'language': 'bengali'}
            },
            "response_type": "symptom_guidance"
        },
        {
            "name": "Emergency Situation",
            "query_info": {
                'symptoms': ['unconsciousness', 'seizures'],
                'query_type': 'emergency',
                'emergency_detected': True,
                'emergency_indicators': ['unconsciousness', 'seizures'],
                'metadata': {'language': 'bengali'}
            },
            "response_type": "emergency_alert"
        },
        {
            "name": "Pregnancy-related Query",
            "query_info": {
                'symptoms': ['fever'],
                'query_type': 'symptom_inquiry',
                'emergency_detected': False,
                'metadata': {
                    'language': 'bengali',
                    'special_populations': ['pregnancy']
                }
            },
            "response_type": "symptom_guidance"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 Scenario: {scenario['name']}")
        print("-" * 30)
        
        disclaimers = response_generator.add_medical_disclaimers(
            scenario['query_info'], 
            scenario['response_type']
        )
        
        print("Bengali Disclaimers Generated:")
        for i, disclaimer in enumerate(disclaimers, 1):
            print(f"\n{i}. {disclaimer}")
    
    print("\n" + "="*80 + "\n")


def demo_language_comparison():
    """Compare responses across different languages."""
    print("🌐 Multi-Language Comparison Demo")
    print("-" * 50)
    
    response_generator = MedicalResponseGenerator()
    
    # Same medical scenario in different languages
    test_scenario = {
        'symptoms': ['fever', 'headache'],
        'query_type': 'symptom_inquiry',
        'emergency_detected': False
    }
    
    languages = [
        ('english', 'English'),
        ('hindi', 'हिंदी (Hindi)'),
        ('bengali', 'বাংলা (Bengali)')
    ]
    
    print("Comparing disclaimers for the same medical scenario:")
    print("Symptoms: fever, headache")
    print()
    
    for lang_code, lang_name in languages:
        print(f"📋 {lang_name} Disclaimer:")
        query_info = test_scenario.copy()
        query_info['metadata'] = {'language': lang_code}
        
        disclaimers = response_generator.add_medical_disclaimers(query_info, 'symptom_guidance')
        print(f"   {disclaimers[0]}")
        print()
    
    print("="*80 + "\n")


def demo_bengali_constants():
    """Display Bengali medical constants."""
    print("📚 Bengali Medical Constants Demo")
    print("-" * 50)
    
    constants = MalariaConstants()
    
    print("Sample Bengali Symptom Translations:")
    sample_symptoms = [
        "জ্বর", "মাথাব্যথা", "কাঁপুনি", "শ্বাসকষ্ট", 
        "অজ্ঞান", "বমি", "পেট ব্যথা", "দুর্বলতা"
    ]
    
    for bengali_symptom in sample_symptoms:
        if bengali_symptom in constants.BENGALI_SYMPTOMS:
            english_translation = constants.BENGALI_SYMPTOMS[bengali_symptom]
            print(f"   {bengali_symptom} → {english_translation}")
    
    print(f"\nTotal Bengali symptoms supported: {len(constants.BENGALI_SYMPTOMS)}")
    print(f"Total Bengali disclaimers available: {len(constants.BENGALI_DISCLAIMERS)}")
    
    print("\n" + "="*80 + "\n")


def interactive_demo():
    """Interactive Bengali query testing."""
    print("🎮 Interactive Bengali Query Demo")
    print("-" * 50)
    print("Enter Bengali medical queries to test the system.")
    print("Type 'quit' or 'বন্ধ' to exit.")
    print()
    
    processor = MedicalQueryProcessor()
    
    while True:
        try:
            query = input("বাংলা প্রশ্ন (Bengali Query): ").strip()
            
            if query.lower() in ['quit', 'exit', 'বন্ধ', '']:
                break
            
            print("\n📊 Analysis Results:")
            result = processor.process_query(query)
            
            print(f"   Original Query: {result['original_query']}")
            print(f"   Language: {result['metadata']['language']}")
            print(f"   Query Type: {result['query_type']}")
            print(f"   Symptoms: {result['symptoms']}")
            print(f"   Emergency: {result['emergency_detected']}")
            if result['emergency_detected']:
                print(f"   Emergency Indicators: {result['emergency_indicators']}")
            print(f"   Confidence: {result['confidence']:.2f}")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error processing query: {e}")
            print()
    
    print("Demo ended. ধন্যবাদ (Thank you)!")


def main():
    """Run the complete Bengali language support demo."""
    print_banner()
    
    demos = [
        ("Symptom Extraction", demo_symptom_extraction),
        ("Query Processing", demo_query_processing),
        ("Response Generation", demo_response_generation),
        ("Language Comparison", demo_language_comparison),
        ("Bengali Constants", demo_bengali_constants)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"Error in {demo_name} demo: {e}")
            continue
    
    # Ask if user wants interactive demo
    try:
        response = input("Would you like to try the interactive Bengali query demo? (y/n): ")
        if response.lower().startswith('y'):
            interactive_demo()
    except KeyboardInterrupt:
        pass
    
    print("\n🎉 Bengali Language Support Demo Complete!")
    print("The Medical RAG System now supports:")
    print("   ✅ Bengali symptom extraction")
    print("   ✅ Bengali emergency detection")
    print("   ✅ Bengali language identification")
    print("   ✅ Bengali medical disclaimers")
    print("   ✅ Multi-language support (English, Hindi, Bengali)")
    print("\nধন্যবাদ! (Thank you!)")


if __name__ == "__main__":
    main()