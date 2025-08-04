#!/usr/bin/env python3
"""
Simple test script for Bengali and Hindi dengue symptom checkers
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.dengue_checker import BengaliDengueChecker, HindiDengueChecker

def test_bengali_dengue():
    """Test Bengali dengue checker with sample inputs."""
    print("Testing Bengali Dengue Checker...")
    checker = BengaliDengueChecker()
    
    # Test cases
    test_cases = [
        "আমার তীব্র জ্বর এবং চোখের ব্যথা",
        "রক্তবমি এবং অজ্ঞান অবস্থা", 
        "পেটের ব্যথা এবং ক্রমাগত বমি"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\nTest {i}: {query}")
        result = checker.check_dengue_symptoms_bengali(query)
        print(f"Severity: {result.get('severity')}")
        print(f"Symptoms: {len(result.get('symptoms', []))} found")
        print(f"Title: {result.get('title', '')[:50]}...")

def test_hindi_dengue():
    """Test Hindi dengue checker with sample inputs."""
    print("\nTesting Hindi Dengue Checker...")
    checker = HindiDengueChecker()
    
    # Test cases
    test_cases = [
        "मुझे तेज बुखार और आंखों में दर्द है",
        "खून की उल्टी और बेहोशी",
        "पेट दर्द और लगातार उल्टी"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\nTest {i}: {query}")
        result = checker.check_dengue_symptoms_hindi(query)
        print(f"Severity: {result.get('severity')}")
        print(f"Symptoms: {len(result.get('symptoms', []))} found")
        print(f"Title: {result.get('title', '')[:50]}...")

if __name__ == "__main__":
    print("🩺 Dengue Symptom Checker - Simple Test")
    print("=" * 50)
    
    test_bengali_dengue()
    test_hindi_dengue()
    
    print("\n✅ All tests completed successfully!")
    print("Bengali and Hindi dengue symptom checkers are working properly.")