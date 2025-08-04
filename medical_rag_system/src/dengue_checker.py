#!/usr/bin/env python3
"""
Bengali Dengue Symptom Checker Module

This module provides specialized functionality for checking dengue symptoms 
in Bengali language, with appropriate medical guidance and safety measures.
"""

import re
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
import logging

from config.medical_constants import DengueConstants
from src.rag_system.query_processor import MedicalQueryProcessor

logger = logging.getLogger(__name__)

class BengaliDengueChecker:
    """Bengali language dengue symptom checker with medical safety protocols."""
    
    def __init__(self):
        self.dengue_constants = DengueConstants()
        self.query_processor = MedicalQueryProcessor()
        
    def detect_language(self, text: str) -> str:
        """Detect if the text is in Bengali language."""
        bengali_chars = set('অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎং')
        text_chars = set(text)
        bengali_count = len(text_chars.intersection(bengali_chars))
        total_chars = len([c for c in text if c.isalpha()])
        
        if total_chars == 0:
            return "unknown"
        
        bengali_ratio = bengali_count / total_chars
        return "bengali" if bengali_ratio > 0.3 else "other"
    
    def extract_dengue_symptoms(self, bengali_text: str) -> List[str]:
        """Extract dengue symptoms from Bengali text."""
        symptoms_found = []
        text_lower = bengali_text.lower()
        
        for bengali_symptom, english_symptom in self.dengue_constants.BENGALI_DENGUE_SYMPTOMS.items():
            if bengali_symptom in text_lower:
                symptoms_found.append(english_symptom)
                logger.info(f"Found symptom: {bengali_symptom} -> {english_symptom}")
        
        return list(set(symptoms_found))
    
    def assess_severity(self, symptoms: List[str]) -> Dict[str, any]:
        """Assess the severity level of dengue symptoms."""
        emergency_count = 0
        warning_count = 0
        early_count = 0
        
        emergency_symptoms = []
        warning_symptoms = []
        early_symptoms = []
        
        for symptom in symptoms:
            if symptom in self.dengue_constants.EMERGENCY_SYMPTOMS:
                emergency_count += 1
                emergency_symptoms.append(symptom)
            elif symptom in self.dengue_constants.WARNING_SYMPTOMS:
                warning_count += 1
                warning_symptoms.append(symptom)
            elif symptom in self.dengue_constants.EARLY_SYMPTOMS:
                early_count += 1
                early_symptoms.append(symptom)
        
        # Determine severity level
        if emergency_count > 0:
            severity = "emergency"
            confidence = 0.95
        elif warning_count >= 2:
            severity = "warning"
            confidence = 0.85
        elif warning_count >= 1 and early_count >= 2:
            severity = "warning"
            confidence = 0.80
        elif early_count >= 3:
            severity = "suspected"
            confidence = 0.70
        elif early_count >= 2:
            severity = "possible"
            confidence = 0.60
        else:
            severity = "unclear"
            confidence = 0.40
        
        return {
            "severity": severity,
            "confidence": confidence,
            "emergency_symptoms": emergency_symptoms,
            "warning_symptoms": warning_symptoms,
            "early_symptoms": early_symptoms,
            "total_symptoms": len(symptoms)
        }
    
    def generate_bengali_response(self, assessment: Dict[str, any], symptoms: List[str]) -> Dict[str, str]:
        """Generate appropriate Bengali response based on assessment."""
        severity = assessment["severity"]
        
        if severity == "emergency":
            response = self._generate_emergency_response_bengali(assessment, symptoms)
        elif severity == "warning":
            response = self._generate_warning_response_bengali(assessment, symptoms)
        elif severity in ["suspected", "possible"]:
            response = self._generate_suspected_response_bengali(assessment, symptoms)
        else:
            response = self._generate_general_response_bengali(assessment, symptoms)
        
        return response
    
    def _generate_emergency_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate emergency response in Bengali."""
        return {
            "severity": "emergency",
            "title": "🚨 জরুরি চিকিৎসা প্রয়োজন",
            "message": f"""আপনার বর্ণিত লক্ষণগুলি ডেঙ্গু জ্বরের গুরুতর পর্যায়ের ইঙ্গিত দিচ্ছে।

🚨 তাৎক্ষণিক করণীয়:
• অবিলম্বে নিকটস্থ হাসপাতালে যান
• জরুরি বিভাগে যোগাযোগ করুন
• চিকিৎসায় বিলম্ব করবেন না

বিপজ্জনক লক্ষণসমূহ:
{', '.join(assessment['emergency_symptoms'])}

আত্মীয়স্বজনকে সাথে নিয়ে যান এবং রোগীর অবস্থা নিয়মিত পর্যবেক্ষণ করুন।""",
            "disclaimer": self.dengue_constants.BENGALI_DENGUE_DISCLAIMERS["emergency"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_warning_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate warning response in Bengali."""
        return {
            "severity": "warning", 
            "title": "⚠️ ডেঙ্গু জ্বরের সতর্কতামূলক লক্ষণ",
            "message": f"""আপনার লক্ষণগুলি ডেঙ্গু জ্বরের সতর্কতামূলক পর্যায়ের ইঙ্গিত দিচ্ছে।

⚠️ জরুরি পদক্ষেপ:
• আগামী ২৪ ঘন্টার মধ্যে ডাক্তার দেখান
• রক্ত পরীক্ষা করান (প্লেটলেট কাউন্ট)
• প্রচুর পানি ও তরল খাবার খান
• পূর্ণ বিশ্রাম নিন

সতর্কতামূলক লক্ষণসমূহ:
{', '.join(assessment['warning_symptoms'])}

লক্ষণ আরও খারাপ হলে অবিলম্বে হাসপাতালে যান।""",
            "disclaimer": self.dengue_constants.BENGALI_DENGUE_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_suspected_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate suspected dengue response in Bengali."""
        return {
            "severity": "suspected",
            "title": "🩺 ডেঙ্গু জ্বরের সম্ভাব্য লক্ষণ",
            "message": f"""আপনার লক্ষণগুলি ডেঙ্গু জ্বরের প্রাথমিক পর্যায়ের সাথে সামঞ্জস্যপূর্ণ।

📋 পরামর্শ:
• ২-৩ দিনের মধ্যে ডাক্তার দেখান
• ডেঙ্গু এনএস১ টেস্ট করান
• জ্বর কমানোর জন্য প্যারাসিটামল খান
• অ্যাসপিরিন এবং আইবুপ্রোফেন এড়িয়ে চলুন

প্রাথমিক লক্ষণসমূহ:
{', '.join(assessment['early_symptoms'])}

🚨 এই লক্ষণগুলি দেখা দিলে তাৎক্ষণিক হাসপাতালে যান:
• নাক বা মাড়ি দিয়ে রক্ত পড়া
• ক্রমাগত বমি
• তীব্র পেটের ব্যথা
• শ্বাসকষ্ট""",
            "disclaimer": self.dengue_constants.BENGALI_DENGUE_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_general_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate general health response in Bengali."""
        return {
            "severity": "general",
            "title": "🏥 স্বাস্থ্য সংক্রান্ত পরামর্শ",
            "message": f"""আপনার উল্লেখিত লক্ষণগুলি বিভিন্ন কারণে হতে পারে।

💡 সাধারণ পরামর্শ:
• পর্যাপ্ত বিশ্রাম নিন
• প্রচুর তরল খাবার খান
• জ্বর থাকলে প্যারাসিটামল খান
• লক্ষণ অব্যাহত থাকলে ডাক্তার দেখান

বর্তমান লক্ষণসমূহ: {', '.join(symptoms)}

যদি নিম্নলিখিত লক্ষণগুলি দেখা দেয় তাহলে অবিলম্বে চিকিৎসা সেবা নিন:
• তীব্র জ্বর (১০২°F এর উপরে)
• তীব্র মাথাব্যথা ও চোখের ব্যথা
• রক্তক্ষরণের কোনো লক্ষণ""",
            "disclaimer": self.dengue_constants.BENGALI_DENGUE_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }

    def check_dengue_symptoms_bengali(self, bengali_query: str) -> Dict[str, any]:
        """Main function to check dengue symptoms from Bengali text."""
        
        # Validate input
        if not bengali_query or not bengali_query.strip():
            return {
                "error": "অনুগ্রহ করে আপনার লক্ষণগুলি বর্ণনা করুন",
                "language": "bengali"
            }
        
        # Detect language
        language = self.detect_language(bengali_query)
        if language != "bengali":
            return {
                "error": "দয়া করে বাংলায় আপনার লক্ষণগুলি লিখুন",
                "language": language
            }
        
        try:
            # Extract symptoms
            symptoms = self.extract_dengue_symptoms(bengali_query)
            
            if not symptoms:
                return {
                    "severity": "unclear",
                    "title": "🤔 লক্ষণ স্পষ্ট নয়",
                    "message": "আপনার বর্ণনা থেকে স্পষ্ট লক্ষণ বুঝতে পারিনি। অনুগ্রহ করে আরও বিস্তারিত বলুন।",
                    "disclaimer": self.dengue_constants.BENGALI_DENGUE_DISCLAIMERS["general"],
                    "symptoms": [],
                    "confidence": "0%"
                }
            
            # Assess severity
            assessment = self.assess_severity(symptoms)
            
            # Generate response
            response = self.generate_bengali_response(assessment, symptoms)
            
            # Add metadata
            response.update({
                "symptoms": symptoms,
                "language": "bengali",
                "timestamp": datetime.now().isoformat(),
                "total_symptoms_found": len(symptoms)
            })
            
            logger.info(f"Processed Bengali dengue query: {len(symptoms)} symptoms found, severity: {assessment['severity']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing Bengali dengue query: {e}")
            return {
                "error": "প্রক্রিয়াকরণে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
                "language": "bengali"
            }

class HindiDengueChecker:
    """Hindi language dengue symptom checker with medical safety protocols."""
    
    def __init__(self):
        self.dengue_constants = DengueConstants()
        self.query_processor = MedicalQueryProcessor()
    
    def detect_language(self, text: str) -> str:
        """Detect if the text is in Hindi language."""
        hindi_chars = set('अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह')
        text_chars = set(text)
        hindi_count = len(text_chars.intersection(hindi_chars))
        total_chars = len([c for c in text if c.isalpha()])
        
        if total_chars == 0:
            return "unknown"
        
        hindi_ratio = hindi_count / total_chars
        return "hindi" if hindi_ratio > 0.3 else "other"
    
    def extract_dengue_symptoms(self, hindi_text: str) -> List[str]:
        """Extract dengue symptoms from Hindi text."""
        symptoms_found = []
        text_lower = hindi_text.lower()
        
        for hindi_symptom, english_symptom in self.dengue_constants.HINDI_DENGUE_SYMPTOMS.items():
            if hindi_symptom in text_lower:
                symptoms_found.append(english_symptom)
                logger.info(f"Found symptom: {hindi_symptom} -> {english_symptom}")
        
        return list(set(symptoms_found))
    
    def assess_severity(self, symptoms: List[str]) -> Dict[str, any]:
        """Assess the severity level of dengue symptoms."""
        emergency_count = 0
        warning_count = 0
        early_count = 0
        
        emergency_symptoms = []
        warning_symptoms = []
        early_symptoms = []
        
        for symptom in symptoms:
            if symptom in self.dengue_constants.EMERGENCY_SYMPTOMS:
                emergency_count += 1
                emergency_symptoms.append(symptom)
            elif symptom in self.dengue_constants.WARNING_SYMPTOMS:
                warning_count += 1
                warning_symptoms.append(symptom)
            elif symptom in self.dengue_constants.EARLY_SYMPTOMS:
                early_count += 1
                early_symptoms.append(symptom)
        
        # Determine severity level
        if emergency_count > 0:
            severity = "emergency"
            confidence = 0.95
        elif warning_count >= 2:
            severity = "warning"
            confidence = 0.85
        elif warning_count >= 1 and early_count >= 2:
            severity = "warning"
            confidence = 0.80
        elif early_count >= 3:
            severity = "suspected"
            confidence = 0.70
        elif early_count >= 2:
            severity = "possible"
            confidence = 0.60
        else:
            severity = "unclear"
            confidence = 0.40
        
        return {
            "severity": severity,
            "confidence": confidence,
            "emergency_symptoms": emergency_symptoms,
            "warning_symptoms": warning_symptoms,
            "early_symptoms": early_symptoms,
            "total_symptoms": len(symptoms)
        }
    
    def generate_hindi_response(self, assessment: Dict[str, any], symptoms: List[str]) -> Dict[str, str]:
        """Generate appropriate Hindi response based on assessment."""
        severity = assessment["severity"]
        
        if severity == "emergency":
            response = self._generate_emergency_response_hindi(assessment, symptoms)
        elif severity == "warning":
            response = self._generate_warning_response_hindi(assessment, symptoms)
        elif severity in ["suspected", "possible"]:
            response = self._generate_suspected_response_hindi(assessment, symptoms)
        else:
            response = self._generate_general_response_hindi(assessment, symptoms)
        
        return response
    
    def _generate_emergency_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate emergency response in Hindi."""
        return {
            "severity": "emergency",
            "title": "🚨 तत्काल चिकित्सा सहायता आवश्यक",
            "message": f"""आपके बताए गए लक्षण डेंगू बुखार की गंभीर अवस्था का संकेत दे रहे हैं।

🚨 तुरंत करें:
• नजदीकी अस्पताल जाएं
• इमरजेंसी विभाग से संपर्क करें
• इलाज में देरी न करें

खतरनाक लक्षण:
{', '.join(assessment['emergency_symptoms'])}

परिवारजनों को साथ लेकर जाएं और मरीज की स्थिति पर लगातार नजर रखें।""",
            "disclaimer": self.dengue_constants.HINDI_DENGUE_DISCLAIMERS["emergency"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_warning_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate warning response in Hindi."""
        return {
            "severity": "warning",
            "title": "⚠️ डेंगू बुखार के चेतावनी संकेत",
            "message": f"""आपके लक्षण डेंगू बुखार की चेतावनी अवस्था का संकेत दे रहे हैं।

⚠️ जरूरी कदम:
• अगले 24 घंटों में डॉक्टर से मिलें
• खून की जांच कराएं (प्लेटलेट काउंट)
• भरपूर पानी और तरल पदार्थ लें
• पूर्ण आराम करें

चेतावनी के लक्षण:
{', '.join(assessment['warning_symptoms'])}

लक्षण और बिगड़ने पर तुरंत अस्पताल जाएं।""",
            "disclaimer": self.dengue_constants.HINDI_DENGUE_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_suspected_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate suspected dengue response in Hindi."""
        return {
            "severity": "suspected",
            "title": "🩺 डेंगू बुखार के संभावित लक्षण",
            "message": f"""आपके लक्षण डेंगू बुखार की प्रारंभिक अवस्था से मेल खाते हैं।

📋 सलाह:
• 2-3 दिन में डॉक्टर से मिलें
• डेंगू NS1 टेस्ट कराएं
• बुखार के लिए पैरासिटामोल लें
• एस्पिरिन और आइबुप्रोफेन से बचें

प्रारंभिक लक्षण:
{', '.join(assessment['early_symptoms'])}

🚨 ये लक्षण दिखें तो तुरंत अस्पताल जाएं:
• नाक या मसूड़ों से खून आना
• लगातार उल्टी
• तेज पेट दर्द
• सांस लेने में तकलीफ""",
            "disclaimer": self.dengue_constants.HINDI_DENGUE_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_general_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate general health response in Hindi."""
        return {
            "severity": "general",
            "title": "🏥 स्वास्थ्य संबंधी सलाह",
            "message": f"""आपके बताए गए लक्षण विभिन्न कारणों से हो सकते हैं।

💡 सामान्य सलाह:
• पर्याप्त आराम करें
• भरपूर तरल पदार्थ लें
• बुखार हो तो पैरासिटामोल लें
• लक्षण बने रहें तो डॉक्टर से मिलें

वर्तमान लक्षण: {', '.join(symptoms)}

यदि निम्नलिखित लक्षण दिखें तो तुरंत चिकित्सा सहायता लें:
• तेज बुखार (102°F से ऊपर)
• तीव्र सिर दर्द और आंखों में दर्द
• खून बहने के कोई संकेत""",
            "disclaimer": self.dengue_constants.HINDI_DENGUE_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }

    def check_dengue_symptoms_hindi(self, hindi_query: str) -> Dict[str, any]:
        """Main function to check dengue symptoms from Hindi text."""
        
        # Validate input
        if not hindi_query or not hindi_query.strip():
            return {
                "error": "कृपया अपने लक्षणों का वर्णन करें",
                "language": "hindi"
            }
        
        # Detect language
        language = self.detect_language(hindi_query)
        if language != "hindi":
            return {
                "error": "कृपया हिंदी में अपने लक्षण लिखें",
                "language": language
            }
        
        try:
            # Extract symptoms
            symptoms = self.extract_dengue_symptoms(hindi_query)
            
            if not symptoms:
                return {
                    "severity": "unclear",
                    "title": "🤔 लक्षण स्पष्ट नहीं",
                    "message": "आपके विवरण से स्पष्ट लक्षण समझ नहीं आए। कृपया और विस्तार से बताएं।",
                    "disclaimer": self.dengue_constants.HINDI_DENGUE_DISCLAIMERS["general"],
                    "symptoms": [],
                    "confidence": "0%"
                }
            
            # Assess severity
            assessment = self.assess_severity(symptoms)
            
            # Generate response
            response = self.generate_hindi_response(assessment, symptoms)
            
            # Add metadata
            response.update({
                "symptoms": symptoms,
                "language": "hindi",
                "timestamp": datetime.now().isoformat(),
                "total_symptoms_found": len(symptoms)
            })
            
            logger.info(f"Processed Hindi dengue query: {len(symptoms)} symptoms found, severity: {assessment['severity']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing Hindi dengue query: {e}")
            return {
                "error": "प्रसंस्करण में समस्या हुई। कृपया फिर से कोशिश करें।",
                "language": "hindi"
            }