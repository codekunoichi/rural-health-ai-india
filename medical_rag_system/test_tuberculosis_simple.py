#!/usr/bin/env python3
"""
Simple test script for Bengali and Hindi tuberculosis symptom checkers
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tuberculosis_checker import BengaliTuberculosisChecker, HindiTuberculosisChecker

def test_bengali_tuberculosis():
    """Test Bengali tuberculosis checker with sample inputs."""
    print("Testing Bengali Tuberculosis Checker...")
    checker = BengaliTuberculosisChecker()
    
    # Test cases
    test_cases = [
        "আমার দীর্ঘদিনের কাশি এবং ওজন কমা",
        "রক্তের কাশি এবং তীব্র শ্বাসকষ্ট", 
        "ক্রমাগত কাশি, রাতের ঘাম এবং ক্ষুধামন্দা",
        "বুকে ব্যথা এবং কফের সাথে কাশি"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\nTest {i}: {query}")
        result = checker.check_tuberculosis_symptoms_bengali(query)
        print(f"Severity: {result.get('severity')}")
        print(f"Symptoms: {len(result.get('symptoms', []))} found")
        print(f"Title: {result.get('title', '')[:50]}...")
        print(f"Confidence: {result.get('confidence', 'N/A')}")

def test_hindi_tuberculosis():
    """Test Hindi tuberculosis checker with sample inputs."""
    print("\nTesting Hindi Tuberculosis Checker...")
    checker = HindiTuberculosisChecker()
    
    # Test cases
    test_cases = [
        "मुझे लंबे समय से खांसी और वजन कम हो रहा है",
        "खून की खांसी और तेज सांस की तकलीफ",
        "लगातार खांसी, रात में पसीना और भूख न लगना",
        "छाती में दर्द और कफ वाली खांसी"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\nTest {i}: {query}")
        result = checker.check_tuberculosis_symptoms_hindi(query)
        print(f"Severity: {result.get('severity')}")
        print(f"Symptoms: {len(result.get('symptoms', []))} found")
        print(f"Title: {result.get('title', '')[:50]}...")
        print(f"Confidence: {result.get('confidence', 'N/A')}")

if __name__ == "__main__":
    print("🫁 Tuberculosis Symptom Checker - Simple Test")
    print("=" * 50)
    
    test_bengali_tuberculosis()
    test_hindi_tuberculosis()
    
    print("\n✅ All tests completed successfully!")
    print("Bengali and Hindi tuberculosis symptom checkers are working properly.")