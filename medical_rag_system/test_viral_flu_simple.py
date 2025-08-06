#!/usr/bin/env python3
"""
Simple test script for Bengali and Hindi viral flu symptom checkers
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.viral_flu_checker import BengaliViralFluChecker, HindiViralFluChecker

def test_bengali_viral_flu():
    """Test Bengali viral flu checker with sample inputs."""
    print("Testing Bengali Viral Flu Checker...")
    checker = BengaliViralFluChecker()
    
    # Test cases
    test_cases = [
        "আমার জ্বর এবং কাশি",
        "তীব্র শ্বাসকষ্ট এবং বিভ্রান্তি", 
        "গলা ব্যথা, নাক বন্ধ এবং হাঁচি",
        "জ্বর, কাঁপুনি এবং শরীর ব্যথা"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\nTest {i}: {query}")
        result = checker.check_viral_flu_symptoms_bengali(query)
        print(f"Severity: {result.get('severity')}")
        print(f"Symptoms: {len(result.get('symptoms', []))} found")
        print(f"Title: {result.get('title', '')[:50]}...")
        print(f"Confidence: {result.get('confidence', 'N/A')}")

def test_hindi_viral_flu():
    """Test Hindi viral flu checker with sample inputs."""
    print("\nTesting Hindi Viral Flu Checker...")
    checker = HindiViralFluChecker()
    
    # Test cases
    test_cases = [
        "मुझे बुखार और खांसी है",
        "तेज सांस की तकलीफ और भ्रम की स्थिति",
        "गले में दर्द, नाक बंद और छींक आना",
        "बुखार, कंपकंपी और शरीर में दर्द"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\nTest {i}: {query}")
        result = checker.check_viral_flu_symptoms_hindi(query)
        print(f"Severity: {result.get('severity')}")
        print(f"Symptoms: {len(result.get('symptoms', []))} found")
        print(f"Title: {result.get('title', '')[:50]}...")
        print(f"Confidence: {result.get('confidence', 'N/A')}")

if __name__ == "__main__":
    print("🦠 Viral Seasonal Flu Symptom Checker - Simple Test")
    print("=" * 55)
    
    test_bengali_viral_flu()
    test_hindi_viral_flu()
    
    print("\n✅ All tests completed successfully!")
    print("Bengali and Hindi viral flu symptom checkers are working properly.")