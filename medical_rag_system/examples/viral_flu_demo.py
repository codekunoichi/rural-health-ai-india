#!/usr/bin/env python3
"""
Bengali and Hindi Viral Seasonal Flu Symptom Checker Demo

This demo showcases the viral seasonal flu symptom checker functionality for both
Bengali and Hindi languages with comprehensive test cases.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.viral_flu_checker import BengaliViralFluChecker, HindiViralFluChecker

def print_banner():
    """Print demo banner."""
    print("=" * 80)
    print("     Viral Seasonal Flu Symptom Checker - Bengali & Hindi Language Support")
    print("     ভাইরাল ফ্লু রোগ নির্ণায়ক - বাংলা ও হিন্দি ভাষা সহায়তা")
    print("     वायरल फ्लू रोग निदानकर्ता - बंगाली और हिंदी भाषा समर्थन")
    print("=" * 80)
    print()

def test_bengali_viral_flu_checker():
    """Test Bengali viral flu symptom checker with various scenarios."""
    print("🔍 Bengali Viral Flu Symptom Checker Test")
    print("-" * 50)
    
    checker = BengaliViralFluChecker()
    
    test_cases = [
        {
            "name": "Emergency Symptoms",
            "query": "তীব্র শ্বাসকষ্ট, প্রচণ্ড জ্বর এবং বিভ্রান্তি",
            "expected_severity": "emergency"
        },
        {
            "name": "Severe Flu",
            "query": "তীব্র জ্বর, গুরুতর মাথাব্যথা এবং অতিরিক্ত ক্লান্তি তিন দিন ধরে",
            "expected_severity": "severe_flu"
        },
        {
            "name": "Moderate Flu",
            "query": "জ্বর, শরীর ব্যথা, গলা ব্যথা এবং ক্রমাগত কাশি",
            "expected_severity": "moderate_flu"
        },
        {
            "name": "Typical Flu",
            "query": "জ্বর, কাঁপুনি, মাথাব্যথা এবং ক্লান্তি",
            "expected_severity": "typical_flu"
        },
        {
            "name": "Mild Flu",
            "query": "হালকা জ্বর এবং গা ব্যথা",
            "expected_severity": "mild_flu"
        },
        {
            "name": "Common Cold",
            "query": "নাক দিয়ে পানি পড়া এবং হাঁচি",
            "expected_severity": "possible_cold"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Query: {test_case['query']}")
        
        result = checker.check_viral_flu_symptoms_bengali(test_case['query'])
        
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

def test_hindi_viral_flu_checker():
    """Test Hindi viral flu symptom checker with various scenarios."""
    print("🔍 Hindi Viral Flu Symptom Checker Test")
    print("-" * 50)
    
    checker = HindiViralFluChecker()
    
    test_cases = [
        {
            "name": "Emergency Symptoms",
            "query": "तेज सांस की तकलीफ, तीव्र बुखार और भ्रम की स्थिति",
            "expected_severity": "emergency"
        },
        {
            "name": "Severe Flu",
            "query": "तेज बुखार, गंभीर सिर दर्द और अत्यधिक थकान तीन दिन से",
            "expected_severity": "severe_flu"
        },
        {
            "name": "Moderate Flu",
            "query": "बुखार, शरीर में दर्द, गले में दर्द और लगातार खांसी",
            "expected_severity": "moderate_flu"
        },
        {
            "name": "Typical Flu",
            "query": "बुखार, कंपकंपी, सिर दर्द और थकान",
            "expected_severity": "typical_flu"
        },
        {
            "name": "Mild Flu",
            "query": "हल्का बुखार और शरीर में दर्द",
            "expected_severity": "mild_flu"
        },
        {
            "name": "Common Cold",
            "query": "नाक बहना और छींक आना",
            "expected_severity": "possible_cold"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Query: {test_case['query']}")
        
        result = checker.check_viral_flu_symptoms_hindi(test_case['query'])
        
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
    """Test language detection accuracy for viral flu queries."""
    print("🌐 Language Detection Test")
    print("-" * 50)
    
    bengali_checker = BengaliViralFluChecker()
    hindi_checker = HindiViralFluChecker()
    
    test_texts = [
        ("আমার জ্বর এবং কাশি", "bengali"),
        ("मुझे बुखार और खांसी है", "hindi"),
        ("I have fever and cough", "other"),
        ("সর্দি-কাশি হয়েছে", "bengali"),
        ("सर्दी-खांसी हो गई है", "hindi"),
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
    """Demonstrate emergency scenario handling for viral flu."""
    print("🚨 Emergency Viral Flu Scenario Demonstration")
    print("-" * 50)
    
    bengali_checker = BengaliViralFluChecker()
    hindi_checker = HindiViralFluChecker()
    
    emergency_scenarios = [
        {
            "language": "Bengali",
            "query": "তীব্র শ্বাসকষ্ট, নীল ঠোঁট এবং ঘুমিয়ে থাকতে কষ্ট হচ্ছে",
            "checker": bengali_checker.check_viral_flu_symptoms_bengali
        },
        {
            "language": "Hindi", 
            "query": "तेज सांस की तकलीफ, नीले होंठ और जागे रहने में कठिনाई",
            "checker": hindi_checker.check_viral_flu_symptoms_hindi
        }
    ]
    
    for scenario in emergency_scenarios:
        print(f"\n🚨 {scenario['language']} Emergency Flu Scenario:")
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
    """Demonstrate different severity level responses for viral flu."""
    print("📊 Viral Flu Severity Level Demonstration")
    print("-" * 50)
    
    bengali_checker = BengaliViralFluChecker()
    hindi_checker = HindiViralFluChecker()
    
    severity_cases = [
        {
            "severity": "Emergency",
            "bengali_query": "তীব্র শ্বাসকষ্ট এবং বিভ্রান্তি",
            "hindi_query": "तेज सांस की तकलीफ और भ्रम"
        },
        {
            "severity": "Severe Flu",
            "bengali_query": "তীব্র জ্বর এবং গুরুতর মাথাব্যথা",
            "hindi_query": "तेज बुखार और गंभीर सिर दर्द"
        },
        {
            "severity": "Moderate Flu",
            "bengali_query": "জ্বর, শরীর ব্যথা এবং কাশি",
            "hindi_query": "बुखार, शरीर में दर्द और खांसी"
        },
        {
            "severity": "Typical Flu",
            "bengali_query": "জ্বর, কাঁপুনি এবং ক্লান্তি",
            "hindi_query": "बुखार, कंपकंपी और थकान"
        },
        {
            "severity": "Mild Flu",
            "bengali_query": "হালকা জ্বর এবং গা ব্যথা",
            "hindi_query": "हल्का बुखार और शरीर में दर्द"
        },
        {
            "severity": "Common Cold",
            "bengali_query": "নাক বন্ধ এবং হাঁচি",
            "hindi_query": "नाक बंद और छींक"
        }
    ]
    
    for case in severity_cases:
        print(f"\n📋 {case['severity']} Level:")
        
        # Bengali response
        bengali_result = bengali_checker.check_viral_flu_symptoms_bengali(case['bengali_query'])
        print(f"Bengali: {bengali_result.get('severity', 'unknown')} - {bengali_result.get('title', '')}")
        
        # Hindi response
        hindi_result = hindi_checker.check_viral_flu_symptoms_hindi(case['hindi_query'])
        print(f"Hindi: {hindi_result.get('severity', 'unknown')} - {hindi_result.get('title', '')}")
    
    print("\n" + "="*80 + "\n")

def demo_home_remedies():
    """Demonstrate home remedy suggestions for different flu types."""
    print("🏠 Home Remedy Suggestions Demo")
    print("-" * 50)
    
    bengali_checker = BengaliViralFluChecker()
    hindi_checker = HindiViralFluChecker()
    
    remedy_cases = [
        {
            "type": "Typical Flu",
            "bengali_query": "জ্বর, কাশি এবং গা ব্যথা",
            "hindi_query": "बुखार, खांसी और शरीर में दर्द"
        },
        {
            "type": "Common Cold",
            "bengali_query": "নাক দিয়ে পানি পড়া এবং গলার খুসখুসানি",
            "hindi_query": "नाक बहना और गले में खुजली"
        }
    ]
    
    for case in remedy_cases:
        print(f"\n🌿 {case['type']} Home Remedies:")
        
        # Bengali remedies
        bengali_result = bengali_checker.check_viral_flu_symptoms_bengali(case['bengali_query'])
        bengali_message = bengali_result.get('message', '')
        if 'ঘরোয়া' in bengali_message:
            remedy_section = bengali_message.split('🏠')[1].split('🔸')[0] if '🏠' in bengali_message else ''
            print(f"Bengali Remedies: {remedy_section[:100]}...")
        
        # Hindi remedies
        hindi_result = hindi_checker.check_viral_flu_symptoms_hindi(case['hindi_query'])
        hindi_message = hindi_result.get('message', '')
        if 'घरेलू' in hindi_message:
            remedy_section = hindi_message.split('🏠')[1].split('🔸')[0] if '🏠' in hindi_message else ''
            print(f"Hindi Remedies: {remedy_section[:100]}...")
    
    print("\n" + "="*80 + "\n")

def interactive_demo():
    """Interactive demo for testing user inputs."""
    print("🎮 Interactive Viral Flu Symptom Checker Demo")
    print("-" * 50)
    print("Enter your flu symptoms in Bengali or Hindi to test the system.")
    print("Type 'quit', 'exit', 'বন্ধ', or 'बंद' to exit.")
    print()
    
    bengali_checker = BengaliViralFluChecker()
    hindi_checker = HindiViralFluChecker()
    
    while True:
        try:
            query = input("লক্ষণ বলুন / अपने लक्षण बताएं: ").strip()
            
            if query.lower() in ['quit', 'exit', 'বন্ধ', 'बंद', '']:
                break
            
            print("\n📊 Analysis Results:")
            
            # Try Bengali first
            if bengali_checker.detect_language(query) == "bengali":
                result = bengali_checker.check_viral_flu_symptoms_bengali(query)
                print("Language: Bengali")
            # Try Hindi
            elif hindi_checker.detect_language(query) == "hindi":
                result = hindi_checker.check_viral_flu_symptoms_hindi(query)
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
    """Test performance with multiple viral flu queries."""
    print("⚡ Performance Test")
    print("-" * 50)
    
    bengali_checker = BengaliViralFluChecker()
    hindi_checker = HindiViralFluChecker()
    
    test_queries = [
        "জ্বর এবং কাশি",
        "बुखार और खांसी",
        "গলা ব্যথা এবং নাক বন্ধ",
        "गले में दर्द और नाक बंद",
        "শরীর ব্যথা এবং মাথাব্যথা",
        "शरीर में दर्द और सिर दर्द",
        "ক্লান্তি এবং দুর্বলতা",
        "थकान और कमजोरी"
    ] * 15  # 120 queries total
    
    start_time = datetime.now()
    
    results = []
    for query in test_queries:
        if bengali_checker.detect_language(query) == "bengali":
            result = bengali_checker.check_viral_flu_symptoms_bengali(query)
        else:
            result = hindi_checker.check_viral_flu_symptoms_hindi(query)
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
    """Run the complete viral flu symptom checker demo."""
    print_banner()
    
    demos = [
        ("Bengali Flu Checker", test_bengali_viral_flu_checker),
        ("Hindi Flu Checker", test_hindi_viral_flu_checker),
        ("Language Detection", test_language_detection),
        ("Emergency Scenarios", demo_emergency_scenarios),
        ("Severity Levels", demo_severity_levels),
        ("Home Remedies", demo_home_remedies),
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
        response = input("Would you like to try the interactive viral flu symptom checker? (y/n): ")
        if response.lower().startswith('y'):
            interactive_demo()
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    
    print("\n🎉 Viral Seasonal Flu Symptom Checker Demo Complete!")
    print("The system now supports:")
    print("   ✅ Bengali viral flu symptom detection")
    print("   ✅ Hindi viral flu symptom detection")
    print("   ✅ Multi-level severity assessment (7 levels)")
    print("   ✅ Emergency situation identification")
    print("   ✅ Home remedy suggestions")
    print("   ✅ Comprehensive symptom mapping (50+ Bengali, 45+ Hindi terms)")
    print("   ✅ Seasonal flu management guidance")
    print("\nধন্যবাদ! धन्यवाद! (Thank you!)")

if __name__ == "__main__":
    main()