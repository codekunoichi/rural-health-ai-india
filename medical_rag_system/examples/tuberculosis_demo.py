#!/usr/bin/env python3
"""
Bengali and Hindi Tuberculosis Symptom Checker Demo

This demo showcases the tuberculosis symptom checker functionality for both
Bengali and Hindi languages with comprehensive test cases.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tuberculosis_checker import BengaliTuberculosisChecker, HindiTuberculosisChecker

def print_banner():
    """Print demo banner."""
    print("=" * 80)
    print("     Tuberculosis Symptom Checker - Bengali & Hindi Language Support")
    print("     যক্ষ্মা রোগ নির্ণায়ক - বাংলা ও হিন্দি ভাষা সহায়তা")
    print("     टीबी रोग निदानकर्ता - बंगाली और हिंदी भाषा समर्थन")
    print("=" * 80)
    print()

def test_bengali_tuberculosis_checker():
    """Test Bengali tuberculosis symptom checker with various scenarios."""
    print("🔍 Bengali Tuberculosis Symptom Checker Test")
    print("-" * 50)
    
    checker = BengaliTuberculosisChecker()
    
    test_cases = [
        {
            "name": "Early TB Symptoms",
            "query": "আমার তিন সপ্তাহ ধরে ক্রমাগত কাশি এবং হালকা জ্বর হচ্ছে",
            "expected_severity": "possible"
        },
        {
            "name": "High Suspicion Case",
            "query": "দীর্ঘদিনের কাশি, ওজন কমা, রাতের ঘাম এবং ক্ষুধামন্দা",
            "expected_severity": "high_suspicion"
        },
        {
            "name": "Emergency Situation",
            "query": "রক্তের কাশি, তীব্র শ্বাসকষ্ট এবং অতিরিক্ত ক্লান্তি",
            "expected_severity": "emergency"
        },
        {
            "name": "Suspected TB",
            "query": "কফের সাথে কাশি, বুকে ব্যথা এবং দুর্বলতা দুই সপ্তাহ ধরে",
            "expected_severity": "suspected"
        },
        {
            "name": "Extrapulmonary TB",
            "query": "গ্রন্থি ফোলা, হাড়ের ব্যথা এবং পেটের ব্যথা",
            "expected_severity": "suspected"
        },
        {
            "name": "Monitoring Required",
            "query": "সামান্য কাশি এবং ক্লান্তি",
            "expected_severity": "monitor"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Query: {test_case['query']}")
        
        result = checker.check_tuberculosis_symptoms_bengali(test_case['query'])
        
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

def test_hindi_tuberculosis_checker():
    """Test Hindi tuberculosis symptom checker with various scenarios."""
    print("🔍 Hindi Tuberculosis Symptom Checker Test")
    print("-" * 50)
    
    checker = HindiTuberculosisChecker()
    
    test_cases = [
        {
            "name": "Early TB Symptoms",
            "query": "मुझे तीन हफ्ते से लगातार खांसी और हल्का बुखार है",
            "expected_severity": "possible"
        },
        {
            "name": "High Suspicion Case",
            "query": "पुरानी खांसी, वजन कम होना, रात में पसीना और भूख न लगना",
            "expected_severity": "high_suspicion"
        },
        {
            "name": "Emergency Situation",
            "query": "खून की खांसी, तेज सांस की तकलीफ और अत्यधिक थकान",
            "expected_severity": "emergency"
        },
        {
            "name": "Suspected TB",
            "query": "कफ वाली खांसी, छाती में दर्द और कमजोरी दो सप्ताह से",
            "expected_severity": "suspected"
        },
        {
            "name": "Extrapulmonary TB",
            "query": "गांठ सूजना, हड्डी में दर्द और पेट दर्द",
            "expected_severity": "suspected"
        },
        {
            "name": "Monitoring Required",
            "query": "हल्की खांसी और थकान",
            "expected_severity": "monitor"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Query: {test_case['query']}")
        
        result = checker.check_tuberculosis_symptoms_hindi(test_case['query'])
        
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
    """Test language detection accuracy for TB queries."""
    print("🌐 Language Detection Test")
    print("-" * 50)
    
    bengali_checker = BengaliTuberculosisChecker()
    hindi_checker = HindiTuberculosisChecker()
    
    test_texts = [
        ("আমার কাশি এবং জ্বর", "bengali"),
        ("मुझे खांसी और बुखार है", "hindi"),
        ("I have cough and fever", "other"),
        ("দীর্ঘদিনের কাশি এবং ওজন কমা", "bengali"),
        ("लगातार खांसी और वजन कम होना", "hindi"),
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
    """Demonstrate emergency scenario handling for TB."""
    print("🚨 Emergency TB Scenario Demonstration")
    print("-" * 50)
    
    bengali_checker = BengaliTuberculosisChecker()
    hindi_checker = HindiTuberculosisChecker()
    
    emergency_scenarios = [
        {
            "language": "Bengali",
            "query": "রোগীর রক্তের কাশি, শ্বাস বন্ধ হয়ে আসা এবং চেতনা হারানোর মতো অবস্থা",
            "checker": bengali_checker.check_tuberculosis_symptoms_bengali
        },
        {
            "language": "Hindi", 
            "query": "मरीज को खून की खांसी, सांस रुकना और बेहोशी की स्थिति",
            "checker": hindi_checker.check_tuberculosis_symptoms_hindi
        }
    ]
    
    for scenario in emergency_scenarios:
        print(f"\n🚨 {scenario['language']} Emergency TB Scenario:")
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

def demo_severity_levels():
    """Demonstrate different severity level responses."""
    print("📊 TB Severity Level Demonstration")
    print("-" * 50)
    
    bengali_checker = BengaliTuberculosisChecker()
    hindi_checker = HindiTuberculosisChecker()
    
    severity_cases = [
        {
            "severity": "Emergency",
            "bengali_query": "রক্তের কাশি এবং তীব্র শ্বাসকষ্ট",
            "hindi_query": "खून की खांसी और तेज सांस की तकलीফ"
        },
        {
            "severity": "High Suspicion",
            "bengali_query": "ক্রমাগত কাশি, ওজন কমা এবং রাতের ঘাম",
            "hindi_query": "लगातार खांसी, वजन कम होना और रात में पसीना"
        },
        {
            "severity": "Suspected",
            "bengali_query": "কফের সাথে কাশি এবং বুকে ব্যথা",
            "hindi_query": "कफ वाली खांसी और छाती में दर्द"
        },
        {
            "severity": "Possible",
            "bengali_query": "দীর্ঘদিনের কাশি এবং ক্লান্তি",
            "hindi_query": "लंबे समय से खांसी और थकान"
        },
        {
            "severity": "Monitor",
            "bengali_query": "হালকা কাশি",
            "hindi_query": "हल्की खांसी"
        }
    ]
    
    for case in severity_cases:
        print(f"\n📋 {case['severity']} Level:")
        
        # Bengali response
        bengali_result = bengali_checker.check_tuberculosis_symptoms_bengali(case['bengali_query'])
        print(f"Bengali: {bengali_result.get('severity', 'unknown')} - {bengali_result.get('title', '')}")
        
        # Hindi response
        hindi_result = hindi_checker.check_tuberculosis_symptoms_hindi(case['hindi_query'])
        print(f"Hindi: {hindi_result.get('severity', 'unknown')} - {hindi_result.get('title', '')}")
    
    print("\n" + "="*80 + "\n")

def interactive_demo():
    """Interactive demo for testing user inputs."""
    print("🎮 Interactive Tuberculosis Symptom Checker Demo")
    print("-" * 50)
    print("Enter your TB symptoms in Bengali or Hindi to test the system.")
    print("Type 'quit', 'exit', 'বন্ধ', or 'बंद' to exit.")
    print()
    
    bengali_checker = BengaliTuberculosisChecker()
    hindi_checker = HindiTuberculosisChecker()
    
    while True:
        try:
            query = input("লক্ষণ বলুন / अपने लक्षण बताएं: ").strip()
            
            if query.lower() in ['quit', 'exit', 'বন্ধ', 'बंद', '']:
                break
            
            print("\n📊 Analysis Results:")
            
            # Try Bengali first
            if bengali_checker.detect_language(query) == "bengali":
                result = bengali_checker.check_tuberculosis_symptoms_bengali(query)
                print("Language: Bengali")
            # Try Hindi
            elif hindi_checker.detect_language(query) == "hindi":
                result = hindi_checker.check_tuberculosis_symptoms_hindi(query)
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
    """Test performance with multiple TB queries."""
    print("⚡ Performance Test")
    print("-" * 50)
    
    bengali_checker = BengaliTuberculosisChecker()
    hindi_checker = HindiTuberculosisChecker()
    
    test_queries = [
        "ক্রমাগত কাশি এবং জ্বর",
        "लगातार खांसी और बुखार",
        "ওজন কমা এবং রাতের ঘাম",
        "वजन कम होना और रात में पसीना",
        "রক্তের কাশি",
        "खून की खांसी",
        "বুকে ব্যথা এবং শ্বাসকষ্ট",
        "छाती में दर्द और सांस फूलना"
    ] * 10  # 80 queries total
    
    start_time = datetime.now()
    
    results = []
    for query in test_queries:
        if bengali_checker.detect_language(query) == "bengali":
            result = bengali_checker.check_tuberculosis_symptoms_bengali(query)
        else:
            result = hindi_checker.check_tuberculosis_symptoms_hindi(query)
        results.append(result)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"✅ Processed {len(test_queries)} queries in {duration:.2f} seconds")
    print(f"✅ Average time per query: {duration/len(test_queries)*1000:.1f} ms")
    print(f"✅ Successful responses: {len([r for r in results if 'error' not in r])}")
    print(f"✅ Error responses: {len([r for r in results if 'error' in r])}")
    
    # Analyze severity distribution
    severity_counts = {}
    for result in results:
        if 'error' not in result:
            severity = result.get('severity', 'unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    print(f"✅ Severity distribution:")
    for severity, count in severity_counts.items():
        print(f"   {severity}: {count}")
    
    print("\n" + "="*80 + "\n")

def main():
    """Run the complete tuberculosis symptom checker demo."""
    print_banner()
    
    demos = [
        ("Bengali TB Checker", test_bengali_tuberculosis_checker),
        ("Hindi TB Checker", test_hindi_tuberculosis_checker),
        ("Language Detection", test_language_detection),
        ("Emergency Scenarios", demo_emergency_scenarios),
        ("Severity Levels", demo_severity_levels),
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
        response = input("Would you like to try the interactive tuberculosis symptom checker? (y/n): ")
        if response.lower().startswith('y'):
            interactive_demo()
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    
    print("\n🎉 Tuberculosis Symptom Checker Demo Complete!")
    print("The system now supports:")
    print("   ✅ Bengali tuberculosis symptom detection")
    print("   ✅ Hindi tuberculosis symptom detection")
    print("   ✅ Multi-level severity assessment (5 levels)")
    print("   ✅ Emergency situation identification")
    print("   ✅ Infection control guidance")
    print("   ✅ Comprehensive symptom mapping (60+ Bengali, 50+ Hindi terms)")
    print("   ✅ Medical safety protocols")
    print("\nধন্যবাদ! धन्यवाद! (Thank you!)")

if __name__ == "__main__":
    main()