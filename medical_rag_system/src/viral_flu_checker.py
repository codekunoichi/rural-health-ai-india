#!/usr/bin/env python3
"""
Bengali and Hindi Viral Seasonal Flu Symptom Checker Module

This module provides specialized functionality for checking viral seasonal flu symptoms 
in Bengali and Hindi languages, with appropriate medical guidance and management advice.
"""

import re
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
import logging

from config.medical_constants import ViralFluConstants
from src.rag_system.query_processor import MedicalQueryProcessor

logger = logging.getLogger(__name__)

class BengaliViralFluChecker:
    """Bengali language viral flu symptom checker with medical guidance."""
    
    def __init__(self):
        self.flu_constants = ViralFluConstants()
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
    
    def extract_flu_symptoms(self, bengali_text: str) -> List[str]:
        """Extract viral flu symptoms from Bengali text."""
        symptoms_found = []
        text_lower = bengali_text.lower()
        
        for bengali_symptom, english_symptom in self.flu_constants.BENGALI_FLU_SYMPTOMS.items():
            if bengali_symptom in text_lower:
                symptoms_found.append(english_symptom)
                logger.info(f"Found flu symptom: {bengali_symptom} -> {english_symptom}")
        
        return list(set(symptoms_found))
    
    def assess_flu_severity(self, symptoms: List[str]) -> Dict[str, any]:
        """Assess the severity level of viral flu symptoms."""
        emergency_count = 0
        warning_count = 0
        common_count = 0
        
        emergency_symptoms = []
        warning_symptoms = []
        common_symptoms = []
        
        for symptom in symptoms:
            if symptom in self.flu_constants.EMERGENCY_SYMPTOMS:
                emergency_count += 1
                emergency_symptoms.append(symptom)
            elif symptom in self.flu_constants.WARNING_SYMPTOMS:
                warning_count += 1
                warning_symptoms.append(symptom)
            elif symptom in self.flu_constants.COMMON_SYMPTOMS:
                common_count += 1
                common_symptoms.append(symptom)
        
        # Determine severity level - Flu specific logic
        if emergency_count > 0:
            severity = "emergency"
            confidence = 0.95
        elif warning_count >= 3 or (warning_count >= 2 and "high fever" in symptoms):
            severity = "severe_flu"
            confidence = 0.85
        elif warning_count >= 2 or (warning_count >= 1 and common_count >= 3):
            severity = "moderate_flu"
            confidence = 0.75
        elif common_count >= 4 or (common_count >= 3 and "fever" in symptoms):
            severity = "typical_flu"
            confidence = 0.70
        elif common_count >= 2:
            severity = "mild_flu"
            confidence = 0.60
        elif common_count >= 1:
            severity = "possible_cold"
            confidence = 0.45
        else:
            severity = "unclear"
            confidence = 0.30
        
        return {
            "severity": severity,
            "confidence": confidence,
            "emergency_symptoms": emergency_symptoms,
            "warning_symptoms": warning_symptoms,
            "common_symptoms": common_symptoms,
            "total_symptoms": len(symptoms)
        }
    
    def generate_bengali_response(self, assessment: Dict[str, any], symptoms: List[str]) -> Dict[str, str]:
        """Generate appropriate Bengali response based on assessment."""
        severity = assessment["severity"]
        
        if severity == "emergency":
            response = self._generate_emergency_response_bengali(assessment, symptoms)
        elif severity == "severe_flu":
            response = self._generate_severe_flu_response_bengali(assessment, symptoms)
        elif severity == "moderate_flu":
            response = self._generate_moderate_flu_response_bengali(assessment, symptoms)
        elif severity == "typical_flu":
            response = self._generate_typical_flu_response_bengali(assessment, symptoms)
        elif severity == "mild_flu":
            response = self._generate_mild_flu_response_bengali(assessment, symptoms)
        elif severity == "possible_cold":
            response = self._generate_cold_response_bengali(assessment, symptoms)
        else:
            response = self._generate_general_response_bengali(assessment, symptoms)
        
        return response
    
    def _generate_emergency_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate emergency response in Bengali."""
        return {
            "severity": "emergency",
            "title": "🚨 জরুরি চিকিৎসা প্রয়োজন",
            "message": f"""আপনার বর্ণিত লক্ষণগুলি গুরুতর ভাইরাল সংক্রমণ বা জটিলতার ইঙ্গিত দিচ্ছে।

🚨 তাৎক্ষণিক করণীয়:
• অবিলম্বে নিকটস্থ হাসপাতালে যান
• জরুরি বিভাগে যোগাযোগ করুন
• শ্বাসযন্ত্রের সমস্যা হলে অ্যাম্বুলেন্স ডাকুন

বিপজ্জনক লক্ষণসমূহ:
{', '.join(assessment['emergency_symptoms'])}

⚠️ বিশেষ সতর্কতা:
• পানিশূন্যতা রোধে তরল খাবার খেতে থাকুন
• শ্বাসকষ্ট হলে বসে থাকুন, শুয়ে থাকবেন না""",
            "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["emergency"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_severe_flu_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate severe flu response in Bengali."""
        return {
            "severity": "severe_flu",
            "title": "⚠️ গুরুতর ভাইরাল ফ্লু",
            "message": f"""আপনার লক্ষণগুলি গুরুতর ভাইরাল ফ্লুর ইঙ্গিত দিচ্ছে।

⚠️ জরুরি পদক্ষেপ:
• আজই ডাক্তার দেখান
• প্রয়োজনে হাসপাতালে ভর্তি হতে হতে পারে
• সম্পূর্ণ বিশ্রাম নিন

গুরুতর লক্ষণসমূহ:
{', '.join(assessment['warning_symptoms'])}

🏥 চিকিৎসা পরামর্শ:
• ডাক্তারের পরামর্শ ছাড়া কোনো ওষুধ খাবেন না
• জ্বর কমানোর জন্য প্যারাসিটামল খেতে পারেন
• প্রচুর পানি ও তরল খাবার খান

🔸 সংক্রমণ প্রতিরোধে:
• মাস্ক ব্যবহার করুন
• অন্যদের কাছ থেকে দূরত্ব বজায় রাখুন
• হাত নিয়মিত ধুয়ে রাখুন""",
            "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_moderate_flu_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate moderate flu response in Bengali."""
        return {
            "severity": "moderate_flu",
            "title": "🤒 মাঝারি মাত্রার ভাইরাল ফ্লু",
            "message": f"""আপনার লক্ষণগুলি মাঝারি মাত্রার ভাইরাল ফ্লুর সাথে সামঞ্জস্যপূর্ণ।

📋 পরামর্শ:
• ২-৩ দিনের মধ্যে ডাক্তার দেখান
• পূর্ণ বিশ্রাম নিন (৫-৭ দিন)
• কাজ/স্কুল থেকে ছুটি নিন

বর্তমান লক্ষণসমূহ:
সতর্কতামূলক: {', '.join(assessment['warning_symptoms'])}
সাধারণ: {', '.join(assessment['common_symptoms'])}

💊 ঘরোয়া চিকিৎসা:
• জ্বরের জন্য প্যারাসিটামল (৬-৮ ঘন্টা পরপর)
• গলা ব্যথার জন্য গরম পানিতে লবণ দিয়ে গার্গল
• কাশির জন্য মধু ও আদার চা
• প্রচুর তরল খাবার (পানি, স্যুপ, ডাবের পানি)

🔸 নিরীক্ষণ করুন:
• জ্বর ১০৪°F এর উপরে গেলে তাৎক্ষণিক ডাক্তার দেখান
• শ্বাসকষ্ট বাড়লে দেরি করবেন না
• ৭ দিনে উন্নতি না হলে আবার ডাক্তার দেখান""",
            "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_typical_flu_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate typical flu response in Bengali."""
        return {
            "severity": "typical_flu",
            "title": "🤧 সাধারণ ভাইরাল ফ্লু",
            "message": f"""আপনার লক্ষণগুলি সাধারণ ভাইরাল ফ্লুর মতো।

💡 পরিচর্যা:
• ৫-৭ দিন বিশ্রাম নিন
• প্রয়োজনে ডাক্তার দেখান
• অন্যদের সংক্রমণ থেকে রক্ষা করুন

সাধারণ লক্ষণসমূহ:
{', '.join(assessment['common_symptoms'])}

🏠 ঘরোয়া পরিচর্যা:
• পর্যাপ্ত ঘুম (৮-১০ ঘন্টা)
• প্রচুর তরল খাবার খান
• পুষ্টিকর খাবার খান (ভিটামিন সি যুক্ত ফল)
• হালকা গরম খাবার ও পানীয়

💊 উপসর্গ নিয়ন্ত্রণ:
• জ্বর: প্যারাসিটামল
• গলা ব্যথা: গরম পানিতে লবণ
• কাশি: মধু ও তুলসী পাতা
• নাক বন্ধ: বাষ্প নিন

⚠️ সতর্কতা - এই লক্ষণ দেখা দিলে ডাক্তার দেখান:
• ১০৩°F এর উপরে জ্বর
• তীব্র শ্বাসকষ্ট
• বুকে ব্যথা
• অতিরিক্ত দুর্বলতা""",
            "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_mild_flu_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate mild flu response in Bengali."""
        return {
            "severity": "mild_flu",
            "title": "🤧 হালকা ভাইরাল ফ্লু",
            "message": f"""আপনার লক্ষণগুলি হালকা ভাইরাল ফ্লু বা সর্দি-কাশির মতো।

💚 সুখবর: সাধারণত ৩-৫ দিনে ভালো হয়ে যাবে

বর্তমান লক্ষণসমূহ: {', '.join(assessment['common_symptoms'])}

🏠 ঘরোয়া পরিচর্যা:
• পর্যাপ্ত বিশ্রাম নিন
• প্রচুর পানি পান করুন
• গরম চা, স্যুপ খান
• ভিটামিন সি যুক্ত খাবার খান

💊 প্রাকৃতিক প্রতিকার:
• আদা-মধুর চা
• তুলসী পাতার রস
• লেবু-মধু গরম পানিতে
• হলুদ-দুধ রাতে

🔸 প্রতিরোধ ব্যবস্থা:
• হাত নিয়মিত ধুয়ে রাখুন
• টিস্যু ব্যবহার করুন
• মাস্ক পরুন
• ভিড় এড়িয়ে চলুন

⚠️ ডাক্তার দেখান যদি:
• ৩ দিনে উন্নতি না হয়
• জ্বর বাড়তে থাকে
• নতুন লক্ষণ দেখা দেয়""",
            "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_cold_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate common cold response in Bengali."""
        return {
            "severity": "possible_cold",
            "title": "🤧 সাধারণ সর্দি-কাশি",
            "message": f"""আপনার লক্ষণগুলি সাধারণ সর্দি-কাশির মতো।

💚 ভালো খবর: সাধারণত ২-৪ দিনে ভালো হয়ে যাবে

বর্তমান লক্ষণসমূহ: {', '.join(symptoms)}

🏠 সহজ প্রতিকার:
• পর্যাপ্ত ঘুম ও বিশ্রাম
• গরম পানি, চা, স্যুপ
• মধু ও লেবুর শরবত
• বাষ্প নিন (গরম পানিতে মুখ দিয়ে)

🌿 প্রাকৃতিক উপাদান:
• আদা চা
• তুলসী পাতা
• মধু
• লেবু

💡 দ্রুত সুস্থতার জন্য:
• প্রচুর তরল খাবার খান
• হালকা গরম খাবার খান
• ধূমপান এড়িয়ে চলুন
• পর্যাপ্ত ভিটামিন সি নিন

🔸 কখন চিকিৎসকের পরামর্শ নেবেন:
• ৫ দিনেও ভালো না হলে
• জ্বর এলে
• গলা ব্যথা বাড়লে""",
            "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_general_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate general health response in Bengali."""
        return {
            "severity": "general",
            "title": "🏥 স্বাস্থ্য পরামর্শ",
            "message": f"""আপনার উল্লেখিত লক্ষণগুলি বিভিন্ন কারণে হতে পারে।

💡 সাধারণ পরামর্শ:
• পর্যাপ্ত বিশ্রাম নিন
• প্রচুর তরল খাবার খান
• পুষ্টিকর খাবার খান
• প্রয়োজনে ডাক্তার দেখান

বর্তমান লক্ষণসমূহ: {', '.join(symptoms)}

🔸 সাধারণ স্বাস্থ্যবিধি:
• নিয়মিত হাত ধোয়া
• স্বাস্থ্যকর খাদ্যাভ্যাস
• পর্যাপ্ত ঘুম
• নিয়মিত ব্যায়াম

⚠️ এই লক্ষণ দেখা দিলে ডাক্তার দেখান:
• জ্বর (১০১°F এর উপরে)
• তীব্র মাথাব্যথা
• শ্বাসকষ্ট
• অব্যাহত বমি""",
            "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }

    def check_viral_flu_symptoms_bengali(self, bengali_query: str) -> Dict[str, any]:
        """Main function to check viral flu symptoms from Bengali text."""
        
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
            symptoms = self.extract_flu_symptoms(bengali_query)
            
            if not symptoms:
                return {
                    "severity": "unclear",
                    "title": "🤔 লক্ষণ স্পষ্ট নয়",
                    "message": "আপনার বর্ণনা থেকে স্পষ্ট লক্ষণ বুঝতে পারিনি। অনুগ্রহ করে আরও বিস্তারিত বলুন।",
                    "disclaimer": self.flu_constants.BENGALI_FLU_DISCLAIMERS["general"],
                    "symptoms": [],
                    "confidence": "0%"
                }
            
            # Assess severity
            assessment = self.assess_flu_severity(symptoms)
            
            # Generate response
            response = self.generate_bengali_response(assessment, symptoms)
            
            # Add metadata
            response.update({
                "symptoms": symptoms,
                "language": "bengali",
                "timestamp": datetime.now().isoformat(),
                "total_symptoms_found": len(symptoms)
            })
            
            logger.info(f"Processed Bengali flu query: {len(symptoms)} symptoms found, severity: {assessment['severity']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing Bengali flu query: {e}")
            return {
                "error": "প্রক্রিয়াকরণে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
                "language": "bengali"
            }

class HindiViralFluChecker:
    """Hindi language viral flu symptom checker with medical guidance."""
    
    def __init__(self):
        self.flu_constants = ViralFluConstants()
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
    
    def extract_flu_symptoms(self, hindi_text: str) -> List[str]:
        """Extract viral flu symptoms from Hindi text."""
        symptoms_found = []
        text_lower = hindi_text.lower()
        
        for hindi_symptom, english_symptom in self.flu_constants.HINDI_FLU_SYMPTOMS.items():
            if hindi_symptom in text_lower:
                symptoms_found.append(english_symptom)
                logger.info(f"Found flu symptom: {hindi_symptom} -> {english_symptom}")
        
        return list(set(symptoms_found))
    
    def assess_flu_severity(self, symptoms: List[str]) -> Dict[str, any]:
        """Assess the severity level of viral flu symptoms."""
        emergency_count = 0
        warning_count = 0
        common_count = 0
        
        emergency_symptoms = []
        warning_symptoms = []
        common_symptoms = []
        
        for symptom in symptoms:
            if symptom in self.flu_constants.EMERGENCY_SYMPTOMS:
                emergency_count += 1
                emergency_symptoms.append(symptom)
            elif symptom in self.flu_constants.WARNING_SYMPTOMS:
                warning_count += 1
                warning_symptoms.append(symptom)
            elif symptom in self.flu_constants.COMMON_SYMPTOMS:
                common_count += 1
                common_symptoms.append(symptom)
        
        # Determine severity level - Flu specific logic
        if emergency_count > 0:
            severity = "emergency"
            confidence = 0.95
        elif warning_count >= 3 or (warning_count >= 2 and "high fever" in symptoms):
            severity = "severe_flu"
            confidence = 0.85
        elif warning_count >= 2 or (warning_count >= 1 and common_count >= 3):
            severity = "moderate_flu"
            confidence = 0.75
        elif common_count >= 4 or (common_count >= 3 and "fever" in symptoms):
            severity = "typical_flu"
            confidence = 0.70
        elif common_count >= 2:
            severity = "mild_flu"
            confidence = 0.60
        elif common_count >= 1:
            severity = "possible_cold"
            confidence = 0.45
        else:
            severity = "unclear"
            confidence = 0.30
        
        return {
            "severity": severity,
            "confidence": confidence,
            "emergency_symptoms": emergency_symptoms,
            "warning_symptoms": warning_symptoms,
            "common_symptoms": common_symptoms,
            "total_symptoms": len(symptoms)
        }
    
    def generate_hindi_response(self, assessment: Dict[str, any], symptoms: List[str]) -> Dict[str, str]:
        """Generate appropriate Hindi response based on assessment."""
        severity = assessment["severity"]
        
        if severity == "emergency":
            response = self._generate_emergency_response_hindi(assessment, symptoms)
        elif severity == "severe_flu":
            response = self._generate_severe_flu_response_hindi(assessment, symptoms)
        elif severity == "moderate_flu":
            response = self._generate_moderate_flu_response_hindi(assessment, symptoms)
        elif severity == "typical_flu":
            response = self._generate_typical_flu_response_hindi(assessment, symptoms)
        elif severity == "mild_flu":
            response = self._generate_mild_flu_response_hindi(assessment, symptoms)
        elif severity == "possible_cold":
            response = self._generate_cold_response_hindi(assessment, symptoms)
        else:
            response = self._generate_general_response_hindi(assessment, symptoms)
        
        return response
    
    def _generate_emergency_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate emergency response in Hindi."""
        return {
            "severity": "emergency",
            "title": "🚨 तत्काल चिकित्सा सहायता आवश्यक",
            "message": f"""आपके बताए गए लक्षण गंभीर वायरल संक्रमण या जटिलताओं का संकेत दे रहे हैं।

🚨 तुरंत करें:
• नजदीकी अस्पताल जाएं
• इमरजेंसी विभाग से संपर्क करें
• सांस की समस्या हो तो एम्बुलेंस बुलाएं

खतरनाक लक्षण:
{', '.join(assessment['emergency_symptoms'])}

⚠️ विशेष सावधानी:
• पानी की कमी रोकने के लिए तरल पदार्थ लेते रहें
• सांस फूले तो बैठकर रहें, लेटें नहीं""",
            "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["emergency"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_severe_flu_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate severe flu response in Hindi."""
        return {
            "severity": "severe_flu",
            "title": "⚠️ गंभीर वायरल फ्लू",
            "message": f"""आपके लक्षण गंभीर वायरल फ्लू का संकेत दे रहे हैं।

⚠️ जरूरी कदम:
• आज ही डॉक्टर से मिलें
• जरूरत पड़े तो अस्पताल में भर्ती हो सकते हैं
• पूर्ण आराम करें

गंभीर लक्षण:
{', '.join(assessment['warning_symptoms'])}

🏥 चिकित्सा सलाह:
• डॉक्टर की सलाह के बिना कोई दवा न लें
• बुखार के लिए पैरासिटामोल ले सकते हैं
• भरपूर पानी और तरल पदार्थ लें

🔸 संक्रमण रोकथाम के लिए:
• मास्क का उपयोग करें
• दूसरों से दूरी बनाए रखें
• हाथ नियमित रूप से धोएं""",
            "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_moderate_flu_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate moderate flu response in Hindi."""
        return {
            "severity": "moderate_flu",
            "title": "🤒 मध्यम दर्जे का वायरल फ्लू",
            "message": f"""आपके लक्षण मध्यम दर्जे के वायरल फ्लू से मेल खाते हैं।

📋 सलाह:
• 2-3 दिन में डॉक्टर से मिलें
• पूर्ण आराम करें (5-7 दिन)
• काम/स्कूल से छुट्टी लें

वर्तमान लक्षण:
चेतावनी वाले: {', '.join(assessment['warning_symptoms'])}
सामान्य: {', '.join(assessment['common_symptoms'])}

💊 घरेलू इलाज:
• बुखार के लिए पैरासिटामोल (6-8 घंटे बाद)
• गले के दर्द के लिए नमक के पानी से गरारे
• खांसी के लिए शहद और अदरक की चाय
• भरपूर तरल पदार्थ (पानी, सूप, नारियल पानी)

🔸 निगरानी करें:
• बुखार 104°F से ऊपर जाए तो तुरंत डॉक्टर दिखाएं
• सांस फूलने लगे तो देरी न करें
• 7 दिन में सुधार न हो तो फिर डॉक्टर दिखाएं""",
            "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_typical_flu_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate typical flu response in Hindi."""
        return {
            "severity": "typical_flu",
            "title": "🤧 सामान्य वायरल फ्लू",
            "message": f"""आपके लक्षण सामान्य वायरल फ्लू जैसे हैं।

💡 देखभाल:
• 5-7 दिन आराम करें
• जरूरत पड़े तो डॉक्टर दिखाएं
• दूसरों को संक्रमण से बचाएं

सामान्य लक्षण:
{', '.join(assessment['common_symptoms'])}

🏠 घरेलू देखभाल:
• पर्याप्त नींद (8-10 घंटे)
• भरपूर तरल पदार्थ लें
• पौष्टिक भोजन (विटामिन सी वाले फल)
• हल्के गर्म खाना और पेय

💊 लक्षण नियंत्रण:
• बुखार: पैरासिटामोल
• गले का दर्द: नमक के पानी से गरारे
• खांसी: शहद और तुलसी
• नाक बंद: भाप लें

⚠️ सावधानी - ये लक्षण दिखें तो डॉक्टर दिखाएं:
• 103°F से ऊपर बुखार
• तेज सांस फूलना
• छाती में दर्द
• अत्यधिक कमजोरी""",
            "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_mild_flu_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate mild flu response in Hindi."""
        return {
            "severity": "mild_flu",
            "title": "🤧 हल्का वायरल फ्लू",
            "message": f"""आपके लक्षण हल्के वायरल फ्लू या सर्दी-खांसी जैसे हैं।

💚 अच्छी खबर: आमतौर पर 3-5 दिन में ठीक हो जाएगा

वर्तमान लक्षण: {', '.join(assessment['common_symptoms'])}

🏠 घरेलू देखभाल:
• पर्याप्त आराम करें
• भरपूर पानी पिएं
• गर्म चाय, सूप लें
• विटामिन सी वाला भोजन लें

💊 प्राकृतिक उपचार:
• अदरक-शहद की चाय
• तुलसी के पत्ते का रस
• नींबू-शहद गर्म पानी में
• हल्दी-दूध रात को

🔸 बचाव के उपाय:
• हाथ नियमित रूप से धोएं
• टिस्यू का इस्तेमाल करें
• मास्क पहनें
• भीड़ से बचें

⚠️ डॉक्टर दिखाएं अगर:
• 3 दिन में सुधार न हो
• बुखार बढ़ता जाए
• नए लक्षण दिखें""",
            "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_cold_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate common cold response in Hindi."""
        return {
            "severity": "possible_cold",
            "title": "🤧 सामान्य सर्दी-खांसी",
            "message": f"""आपके लक्षण सामान्य सर्दी-खांसी जैसे हैं।

💚 अच्छी खबर: आमतौर पर 2-4 दिन में ठीक हो जाएगा

वर्तमान लक्षण: {', '.join(symptoms)}

🏠 आसान उपाय:
• पर्याप्त नींद और आराम
• गर्म पानी, चाय, सूप
• शहद और नींबू का शरबत
• भाप लें (गर्म पानी में मुंह करके)

🌿 प्राकृतिक सामग्री:
• अदरक की चाय
• तुलसी के पत्ते
• शहद
• नींबू

💡 जल्दी ठीक होने के लिए:
• भरपूर तरल पदार्थ लें
• हल्का गर्म खाना खाएं
• धूम्रपान से बचें
• पर्याप्त विटामिन सी लें

🔸 कब डॉक्टर की सलाह लें:
• 5 दिन में भी ठीक न हो
• बुखार आ जाए
• गले का दर्द बढ़ जाए""",
            "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_general_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate general health response in Hindi."""
        return {
            "severity": "general",
            "title": "🏥 स्वास्थ्य सलाह",
            "message": f"""आपके बताए गए लक्षण विभिन्न कारणों से हो सकते हैं।

💡 सामान्य सलाह:
• पर्याप्त आराम करें
• भरपूर तरल पदार्थ लें
• पौष्टिक भोजन लें
• जरूरत पड़े तो डॉक्टर दिखाएं

वर्तमान लक्षण: {', '.join(symptoms)}

🔸 सामान्य स्वास्थ्य नियम:
• नियमित हाथ धोना
• स्वस्थ खान-पान
• पर्याप्त नींद
• नियमित व्यायाम

⚠️ ये लक्षण दिखें तो डॉक्टर दिखाएं:
• बुखार (101°F से ऊपर)
• तेज सिर दर्द
• सांस फूलना
• लगातार उल्टी""",
            "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }

    def check_viral_flu_symptoms_hindi(self, hindi_query: str) -> Dict[str, any]:
        """Main function to check viral flu symptoms from Hindi text."""
        
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
            symptoms = self.extract_flu_symptoms(hindi_query)
            
            if not symptoms:
                return {
                    "severity": "unclear",
                    "title": "🤔 लक्षण स्पष्ट नहीं",
                    "message": "आपके विवरण से स्पष्ट लक्षण समझ नहीं आए। कृपया और विस्तार से बताएं।",
                    "disclaimer": self.flu_constants.HINDI_FLU_DISCLAIMERS["general"],
                    "symptoms": [],
                    "confidence": "0%"
                }
            
            # Assess severity
            assessment = self.assess_flu_severity(symptoms)
            
            # Generate response
            response = self.generate_hindi_response(assessment, symptoms)
            
            # Add metadata
            response.update({
                "symptoms": symptoms,
                "language": "hindi",
                "timestamp": datetime.now().isoformat(),
                "total_symptoms_found": len(symptoms)
            })
            
            logger.info(f"Processed Hindi flu query: {len(symptoms)} symptoms found, severity: {assessment['severity']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing Hindi flu query: {e}")
            return {
                "error": "प्रसंस्करण में समस्या हुई। कृपया फिर से कोशिश करें।",
                "language": "hindi"
            }