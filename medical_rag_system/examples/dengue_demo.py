#!/usr/bin/env python3
"""
Bengali and Hindi Dengue Symptom Checker Demo

This demo showcases the dengue symptom checker functionality for both
Bengali and Hindi languages with comprehensive test cases.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dengue_checker import BengaliDengueChecker, HindiDengueChecker

def print_banner():
    """Print demo banner."""
    print("=" * 80)
    print("     Dengue Symptom Checker - Bengali & Hindi Language Support")
    print("     ডেঙ্গু জ্বর পরীক্ষক - বাংলা ও হিন্দি ভাষা সহায়তা")
    print("     डेंगू बुखार जांचकर्ता - बंगाली और हिंदी भाषा समर्थन")
    print("=" * 80)
    print()

def test_bengali_dengue_checker():
    """Test Bengali dengue symptom checker with various scenarios."""
    print("🔍 Bengali Dengue Symptom Checker Test")
    print("-" * 50)
    
    checker = BengaliDengueChecker()
    
    test_cases = [
        {
            "name": "Early Dengue Symptoms",
            "query": "আমার তিন দিন ধরে তীব্র জ্বর, গুরুতর মাথাব্যথা এবং চোখের ব্যথা হচ্ছে",
            "expected_severity": "suspected"
        },
        {
            "name": "Warning Signs",
            "query": "পেটের ব্যথা, ক্রমাগত বমি এবং নাক দিয়ে রক্ত পড়ছে",
            "expected_severity": "warning"
        },
        {
            "name": "Emergency Situation",
            "query": "রোগীর অজ্ঞান অবস্থা, রক্তবমি এবং শ্বাসকষ্ট হচ্ছে",
            "expected_severity": "emergency"
        },
        {
            "name": "Complete Dengue Profile",
            "query": "তীব্র জ্বর, হাড়ের ব্যথা, চোখের পেছনে ব্যথা, র‍্যাশ এবং দুর্বলতা",
            "expected_severity": "suspected"
        },
        {
            "name": "Bleeding Symptoms",
            "query": "দাঁতের মাড়ি দিয়ে রক্ত, কালো পায়খানা এবং তীব্র পেট ব্যথা",
            "expected_severity": "emergency"
        },
        {
            "name": "Mild Symptoms",
            "query": "সামান্য জ্বর এবং শরীর ব্যথা",
            "expected_severity": "possible"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Query: {test_case['query']}")
        
        result = checker.check_dengue_symptoms_bengali(test_case['query'])
        
        print(f"✅ Severity: {result.get('severity', 'N/A')}")
        print(f"✅ Confidence: {result.get('confidence', 'N/A')}")
        print(f"✅ Symptoms Found: {len(result.get('symptoms', []))}")
        if result.get('symptoms'):
            print(f"   Symptoms: {', '.join(result['symptoms'])}")
        print(f"✅ Response Title: {result.get('title', 'N/A')}")
        
        # Show first few lines of the message
        message = result.get('message', '')
        if message:
            lines = message.split('\n')[:3]
            print(f"✅ Response Preview: {' '.join(lines)[:100]}...")
    
    print("\n" + "="*80 + "\n")

def test_hindi_dengue_checker():
    """Test Hindi dengue symptom checker with various scenarios."""
    print("🔍 Hindi Dengue Symptom Checker Test")
    print("-" * 50)
    
    checker = HindiDengueChecker()
    
    test_cases = [
        {
            "name": "Early Dengue Symptoms",
            "query": "मुझे तीन दिन से तेज बुखार, गंभीर सिर दर्द और आंखों में दर्द हो रहा है",
            "expected_severity": "suspected"
        },
        {
            "name": "Warning Signs", 
            "query": "पेट दर्द, लगातार उल्टी और नाक से खून आ रहा है",
            "expected_severity": "warning"
        },
        {
            "name": "Emergency Situation",
            "query": "मरीज बेहोश है, खून की उल्टी हो रही है और सांस लेने में तकलीफ है",
            "expected_severity": "emergency"
        },
        {
            "name": "Complete Dengue Profile",
            "query": "तीव्र बुखार, हड्डी में दर्द, आंखों के पीछे दर्द, रैश और कमजोरी",
            "expected_severity": "suspected"
        },
        {
            "name": "Bleeding Symptoms",
            "query": "मसूड़ों से खून, काला मल और तेज पेट दर्द",
            "expected_severity": "emergency"
        },
        {
            "name": "Mild Symptoms",
            "query": "हल्का बुखार और शरीर में दर्द",
            "expected_severity": "possible"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Query: {test_case['query']}")
        
        result = checker.check_dengue_symptoms_hindi(test_case['query'])
        
        print(f"✅ Severity: {result.get('severity', 'N/A')}")
        print(f"✅ Confidence: {result.get('confidence', 'N/A')}")
        print(f"✅ Symptoms Found: {len(result.get('symptoms', []))}")
        if result.get('symptoms'):
            print(f"   Symptoms: {', '.join(result['symptoms'])}")
        print(f"✅ Response Title: {result.get('title', 'N/A')}")
        
        # Show first few lines of the message
        message = result.get('message', '')
        if message:
            lines = message.split('\n')[:3]
            print(f"✅ Response Preview: {' '.join(lines)[:100]}...")
    
    print("\n" + "="*80 + "\n")

def test_language_detection():
    """Test language detection accuracy."""
    print("🌐 Language Detection Test")
    print("-" * 50)
    
    bengali_checker = BengaliDengueChecker()
    hindi_checker = HindiDengueChecker()
    
    test_texts = [
        ("আমার জ্বর এবং মাথাব্যথা", "bengali"),
        ("मुझे बुखार और सिर दर्द है", "hindi"),
        ("I have fever and headache", "other"),
        ("তীব্র জ্বর এবং চোখের ব্যথা", "bengali"),
        ("तेज बुखार और आंखों में दर्द", "hindi"),
        ("", "unknown")
    ]
    
    print("Bengali Language Detection:")
    for text, expected in test_texts:
        detected = bengali_checker.detect_language(text)
        status = "✅" if (detected == expected or (expected == "other" and detected != "bengali")) else "❌"
        print(f"  {status} '{text}' -> {detected} (expected: {expected})")
    
    print("\nHindi Language Detection:")
    for text, expected in test_texts:
        detected = hindi_checker.detect_language(text)
        status = "✅" if (detected == expected or (expected == "other" and detected != "hindi")) else "❌"
        print(f"  {status} '{text}' -> {detected} (expected: {expected})")
    
    print("\n" + "="*80 + "\n")

def demo_emergency_scenarios():
    """Demonstrate emergency scenario handling."""
    print("🚨 Emergency Scenario Demonstration")
    print("-" * 50)
    
    bengali_checker = BengaliDengueChecker()
    hindi_checker = HindiDengueChecker()
    
    emergency_scenarios = [
        {
            "language": "Bengali",
            "query": "রোগীর অচেতন অবস্থা, খিঁচুনি এবং রক্তক্ষরণ হচ্ছে",
            "checker": bengali_checker.check_dengue_symptoms_bengali
        },
        {
            "language": "Hindi", 
            "query": "मरीज बेहोश है, दौरे आ रहे हैं और रक्तस्राव हो रहा है",
            "checker": hindi_checker.check_dengue_symptoms_hindi
        }
    ]
    
    for scenario in emergency_scenarios:
        print(f"\n🚨 {scenario['language']} Emergency Scenario:")
        print(f"Query: {scenario['query']}")
        
        result = scenario['checker'](scenario['query'])
        
        print(f"\n{result.get('title', '')}")
        print(f"Severity: {result.get('severity', 'N/A')}")
        print(f"Confidence: {result.get('confidence', 'N/A')}")
        print(f"\nMessage Preview:")
        message_lines = result.get('message', '').split('\n')[:5]
        for line in message_lines:
            print(f"  {line}")
        
        print(f"\nDisclaimer: {result.get('disclaimer', '')}")
    
    print("\n" + "="*80 + "\n")

def interactive_demo():
    """Interactive demo for testing user inputs."""
    print("🎮 Interactive Dengue Symptom Checker Demo")
    print("-" * 50)
    print("Enter your symptoms in Bengali or Hindi to test the system.")
    print("Type 'quit', 'exit', 'বন্ধ', or 'बंद' to exit.")
    print()
    
    bengali_checker = BengaliDengueChecker()
    hindi_checker = HindiDengueChecker()
    
    while True:
        try:
            query = input("লক্ষণ বলুন / अपने लक्षण बताएं: ").strip()
            
            if query.lower() in ['quit', 'exit', 'বন্ধ', 'बंद', '']:
                break
            
            print("\n📊 Analysis Results:")
            
            # Try Bengali first
            if bengali_checker.detect_language(query) == "bengali":
                result = bengali_checker.check_dengue_symptoms_bengali(query)
                print("Language: Bengali")
            # Try Hindi
            elif hindi_checker.detect_language(query) == "hindi":
                result = hindi_checker.check_dengue_symptoms_hindi(query)
                print("Language: Hindi")
            else:
                print("Language: Not supported (Please use Bengali or Hindi)")
                continue
            
            print(f"Severity: {result.get('severity', 'N/A')}")
            print(f"Symptoms Found: {len(result.get('symptoms', []))}")
            if result.get('symptoms'):
                print(f"Symptoms: {', '.join(result['symptoms'])}")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
            
            print(f"\n{result.get('title', '')}")
            print(f"{result.get('message', '')}")
            print(f"\n{result.get('disclaimer', '')}")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error processing query: {e}")
            print()
    
    print("Demo ended. ধন্যবাদ! धन्यवाद! (Thank you!)")

def performance_test():
    """Test performance with multiple queries."""
    print("⚡ Performance Test")
    print("-" * 50)
    
    bengali_checker = BengaliDengueChecker()
    hindi_checker = HindiDengueChecker()
    
    test_queries = [
        "তীব্র জ্বর এবং মাথাব্যথা",
        "तेज बुखार और सिर दर्द",
        "পেটের ব্যথা এবং বমি",
        "पेट दर्द और उल्टी",
        "অজ্ঞান এবং খিঁচুনি",
        "बेहोशी और दौरे"
    ] * 10  # 60 queries total
    
    start_time = datetime.now()
    
    results = []
    for query in test_queries:
        if bengali_checker.detect_language(query) == "bengali":
            result = bengali_checker.check_dengue_symptoms_bengali(query)
        else:
            result = hindi_checker.check_dengue_symptoms_hindi(query)
        results.append(result)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"✅ Processed {len(test_queries)} queries in {duration:.2f} seconds")
    print(f"✅ Average time per query: {duration/len(test_queries)*1000:.1f} ms")
    print(f"✅ Successful responses: {len([r for r in results if 'error' not in r])}")
    print(f"✅ Error responses: {len([r for r in results if 'error' in r])}")
    
    print("\n" + "="*80 + "\n")

def main():
    """Run the complete dengue symptom checker demo."""
    print_banner()
    
    demos = [
        ("Bengali Dengue Checker", test_bengali_dengue_checker),
        ("Hindi Dengue Checker", test_hindi_dengue_checker),
        ("Language Detection", test_language_detection),
        ("Emergency Scenarios", demo_emergency_scenarios),
        ("Performance Test", performance_test)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"Error in {demo_name} demo: {e}")
            continue
    
    # Ask if user wants interactive demo
    try:
        response = input("Would you like to try the interactive dengue symptom checker? (y/n): ")
        if response.lower().startswith('y'):
            interactive_demo()
    except KeyboardInterrupt:
        pass
    
    print("\n🎉 Dengue Symptom Checker Demo Complete!")
    print("The system now supports:")
    print("   ✅ Bengali dengue symptom detection")
    print("   ✅ Hindi dengue symptom detection")
    print("   ✅ Emergency situation identification")
    print("   ✅ Severity assessment")
    print("   ✅ Multi-language medical disclaimers")
    print("   ✅ Comprehensive symptom mapping")
    print("\nধন্যবাদ! धन्यवाद! (Thank you!)")

if __name__ == "__main__":
    main()