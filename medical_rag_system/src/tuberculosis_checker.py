#!/usr/bin/env python3
"""
Bengali and Hindi Tuberculosis Symptom Checker Module

This module provides specialized functionality for checking tuberculosis symptoms 
in Bengali and Hindi languages, with appropriate medical guidance and safety measures.
"""

import re
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
import logging

from config.medical_constants import TuberculosisConstants
from src.rag_system.query_processor import MedicalQueryProcessor

logger = logging.getLogger(__name__)

class BengaliTuberculosisChecker:
    """Bengali language tuberculosis symptom checker with medical safety protocols."""
    
    def __init__(self):
        self.tb_constants = TuberculosisConstants()
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
    
    def extract_tb_symptoms(self, bengali_text: str) -> List[str]:
        """Extract tuberculosis symptoms from Bengali text."""
        symptoms_found = []
        text_lower = bengali_text.lower()
        
        for bengali_symptom, english_symptom in self.tb_constants.BENGALI_TB_SYMPTOMS.items():
            if bengali_symptom in text_lower:
                symptoms_found.append(english_symptom)
                logger.info(f"Found TB symptom: {bengali_symptom} -> {english_symptom}")
        
        return list(set(symptoms_found))
    
    def assess_tb_severity(self, symptoms: List[str]) -> Dict[str, any]:
        """Assess the severity level of tuberculosis symptoms."""
        emergency_count = 0
        warning_count = 0
        early_count = 0
        
        emergency_symptoms = []
        warning_symptoms = []
        early_symptoms = []
        
        for symptom in symptoms:
            if symptom in self.tb_constants.EMERGENCY_SYMPTOMS:
                emergency_count += 1
                emergency_symptoms.append(symptom)
            elif symptom in self.tb_constants.WARNING_SYMPTOMS:
                warning_count += 1
                warning_symptoms.append(symptom)
            elif symptom in self.tb_constants.EARLY_SYMPTOMS:
                early_count += 1
                early_symptoms.append(symptom)
        
        # Determine severity level - TB specific logic
        if emergency_count > 0:
            severity = "emergency"
            confidence = 0.95
        elif warning_count >= 3 or (warning_count >= 2 and early_count >= 1):
            severity = "high_suspicion"
            confidence = 0.85
        elif warning_count >= 2 or (warning_count >= 1 and early_count >= 2):
            severity = "suspected"
            confidence = 0.75
        elif early_count >= 3 or (early_count >= 2 and "persistent cough" in symptoms):
            severity = "possible"
            confidence = 0.65
        elif early_count >= 1:
            severity = "monitor"
            confidence = 0.45
        else:
            severity = "unclear"
            confidence = 0.30
        
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
        elif severity == "high_suspicion":
            response = self._generate_high_suspicion_response_bengali(assessment, symptoms)
        elif severity == "suspected":
            response = self._generate_suspected_response_bengali(assessment, symptoms)
        elif severity == "possible":
            response = self._generate_possible_response_bengali(assessment, symptoms)
        elif severity == "monitor":
            response = self._generate_monitor_response_bengali(assessment, symptoms)
        else:
            response = self._generate_general_response_bengali(assessment, symptoms)
        
        return response
    
    def _generate_emergency_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate emergency response in Bengali."""
        return {
            "severity": "emergency",
            "title": "🚨 জরুরি চিকিৎসা প্রয়োজন",
            "message": f"""আপনার বর্ণিত লক্ষণগুলি গুরুতর যক্ষ্মা বা জটিলতার ইঙ্গিত দিচ্ছে।

🚨 তাৎক্ষণিক করণীয়:
• অবিলম্বে নিকটস্থ হাসপাতালে যান
• জরুরি বিভাগে যোগাযোগ করুন
• শ্বাসযন্ত্রের মাস্ক ব্যবহার করুন
• অন্যদের থেকে দূরত্ব বজায় রাখুন

বিপজ্জনক লক্ষণসমূহ:
{', '.join(assessment['emergency_symptoms'])}

যক্ষ্মা একটি সংক্রামক রোগ তাই অন্যদের সুরক্ষার জন্য সতর্কতা অবলম্বন করুন।""",
            "disclaimer": self.tb_constants.BENGALI_TB_DISCLAIMERS["emergency"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_high_suspicion_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate high suspicion response in Bengali."""
        return {
            "severity": "high_suspicion",
            "title": "⚠️ যক্ষ্মার উচ্চ সম্ভাবনা",
            "message": f"""আপনার লক্ষণগুলি যক্ষ্মার প্রবল সম্ভাবনা নির্দেশ করে।

⚠️ জরুরি পদক্ষেপ:
• আগামী ২৪ ঘন্টার মধ্যে ডাক্তার দেখান
• কফ পরীক্ষা (স্পুটাম টেস্ট) করান
• বুকের এক্স-রে করান
• পারিবারিক সদস্যদের পরীক্ষা করান

প্রবল সন্দেহজনক লক্ষণসমূহ:
{', '.join(assessment['warning_symptoms'])}

🔸 সংক্রমণ প্রতিরোধে:
• কাশির সময় মুখ ঢেকে রাখুন
• পর্যাপ্ত বায়ু চলাচলযুক্ত জায়গায় থাকুন
• অন্যদের কাছ থেকে দূরত্ব বজায় রাখুন""",
            "disclaimer": self.tb_constants.BENGALI_TB_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_suspected_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate suspected TB response in Bengali."""
        return {
            "severity": "suspected",
            "title": "🩺 যক্ষ্মার সন্দেহজনক লক্ষণ",
            "message": f"""আপনার লক্ষণগুলি যক্ষ্মার সাথে সামঞ্জস্যপূর্ণ।

📋 পরামর্শ:
• ২-৩ দিনের মধ্যে ডাক্তার দেখান
• কফ পরীক্ষা করান (৩ দিন পর পর)
• বুকের এক্স-রে করান
• টিউবারকুলিন স্কিন টেস্ট (TST) করান

সন্দেহজনক লক্ষণসমূহ:
{', '.join(assessment['warning_symptoms'] + assessment['early_symptoms'])}

🔸 সাবধানতা:
• যক্ষ্মা নিশ্চিত না হওয়া পর্যন্ত সতর্কতা অবলম্বন করুন
• পুষ্টিকর খাবার খান এবং পর্যাপ্ত বিশ্রাম নিন
• ধূমপান ও মদ্যপান এড়িয়ে চলুন""",
            "disclaimer": self.tb_constants.BENGALI_TB_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_possible_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate possible TB response in Bengali."""
        return {
            "severity": "possible",
            "title": "🤔 যক্ষ্মার সম্ভাব্য লক্ষণ",
            "message": f"""আপনার লক্ষণগুলি যক্ষ্মার প্রাথমিক পর্যায়ের হতে পারে।

💡 পরামর্শ:
• এক সপ্তাহের মধ্যে ডাক্তার দেখান
• লক্ষণ উন্নতি না হলে কফ পরীক্ষা করান
• স্বাস্থ্যকর জীবনযাত্রা বজায় রাখুন

বর্তমান লক্ষণসমূহ:
{', '.join(assessment['early_symptoms'])}

🔸 নিরীক্ষণ করুন:
• কাশি ৩ সপ্তাহের বেশি থাকলে অবশ্যই ডাক্তার দেখান
• ওজন কমতে থাকলে সতর্ক হন
• রাতের ঘাম বাড়লে চিকিৎসা নিন""",
            "disclaimer": self.tb_constants.BENGALI_TB_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_monitor_response_bengali(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate monitoring response in Bengali."""
        return {
            "severity": "monitor",
            "title": "👁️ লক্ষণ পর্যবেক্ষণ করুন",
            "message": f"""আপনার উল্লেখিত লক্ষণগুলি নিরীক্ষণ প্রয়োজন।

📊 পর্যবেক্ষণ করুন:
• লক্ষণগুলি কতদিন স্থায়ী হচ্ছে
• লক্ষণ খারাপ হচ্ছে নাকি ভালো হচ্ছে
• নতুন কোনো লক্ষণ যোগ হচ্ছে কিনা

বর্তমান লক্ষণ: {', '.join(symptoms)}

⚠️ সতর্কতা - এই লক্ষণগুলি দেখা দিলে তাৎক্ষণিক ডাক্তার দেখান:
• ৩ সপ্তাহের বেশি কাশি
• কফে রক্ত
• দ্রুত ওজন কমা
• তীব্র রাতের ঘাম
• শ্বাসকষ্ট""",
            "disclaimer": self.tb_constants.BENGALI_TB_DISCLAIMERS["general"],
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
• পুষ্টিকর খাবার খান
• প্রচুর তরল খাবার খান
• লক্ষণ অব্যাহত থাকলে ডাক্তার দেখান

বর্তমান লক্ষণসমূহ: {', '.join(symptoms)}

🔸 যক্ষ্মার ঝুঁকি কমানোর উপায়:
• সুষম খাদ্য গ্রহণ করুন
• নিয়মিত ব্যায়াম করুন
• ধূমপান ত্যাগ করুন
• ভালো বায়ু চলাচলযুক্ত পরিবেশে থাকুন""",
            "disclaimer": self.tb_constants.BENGALI_TB_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }

    def check_tuberculosis_symptoms_bengali(self, bengali_query: str) -> Dict[str, any]:
        """Main function to check tuberculosis symptoms from Bengali text."""
        
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
            symptoms = self.extract_tb_symptoms(bengali_query)
            
            if not symptoms:
                return {
                    "severity": "unclear",
                    "title": "🤔 লক্ষণ স্পষ্ট নয়",
                    "message": "আপনার বর্ণনা থেকে স্পষ্ট লক্ষণ বুঝতে পারিনি। অনুগ্রহ করে আরও বিস্তারিত বলুন।",
                    "disclaimer": self.tb_constants.BENGALI_TB_DISCLAIMERS["general"],
                    "symptoms": [],
                    "confidence": "0%"
                }
            
            # Assess severity
            assessment = self.assess_tb_severity(symptoms)
            
            # Generate response
            response = self.generate_bengali_response(assessment, symptoms)
            
            # Add metadata
            response.update({
                "symptoms": symptoms,
                "language": "bengali",
                "timestamp": datetime.now().isoformat(),
                "total_symptoms_found": len(symptoms)
            })
            
            logger.info(f"Processed Bengali TB query: {len(symptoms)} symptoms found, severity: {assessment['severity']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing Bengali TB query: {e}")
            return {
                "error": "প্রক্রিয়াকরণে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
                "language": "bengali"
            }

class HindiTuberculosisChecker:
    """Hindi language tuberculosis symptom checker with medical safety protocols."""
    
    def __init__(self):
        self.tb_constants = TuberculosisConstants()
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
    
    def extract_tb_symptoms(self, hindi_text: str) -> List[str]:
        """Extract tuberculosis symptoms from Hindi text."""
        symptoms_found = []
        text_lower = hindi_text.lower()
        
        for hindi_symptom, english_symptom in self.tb_constants.HINDI_TB_SYMPTOMS.items():
            if hindi_symptom in text_lower:
                symptoms_found.append(english_symptom)
                logger.info(f"Found TB symptom: {hindi_symptom} -> {english_symptom}")
        
        return list(set(symptoms_found))
    
    def assess_tb_severity(self, symptoms: List[str]) -> Dict[str, any]:
        """Assess the severity level of tuberculosis symptoms."""
        emergency_count = 0
        warning_count = 0
        early_count = 0
        
        emergency_symptoms = []
        warning_symptoms = []
        early_symptoms = []
        
        for symptom in symptoms:
            if symptom in self.tb_constants.EMERGENCY_SYMPTOMS:
                emergency_count += 1
                emergency_symptoms.append(symptom)
            elif symptom in self.tb_constants.WARNING_SYMPTOMS:
                warning_count += 1
                warning_symptoms.append(symptom)
            elif symptom in self.tb_constants.EARLY_SYMPTOMS:
                early_count += 1
                early_symptoms.append(symptom)
        
        # Determine severity level - TB specific logic
        if emergency_count > 0:
            severity = "emergency"
            confidence = 0.95
        elif warning_count >= 3 or (warning_count >= 2 and early_count >= 1):
            severity = "high_suspicion"
            confidence = 0.85
        elif warning_count >= 2 or (warning_count >= 1 and early_count >= 2):
            severity = "suspected"
            confidence = 0.75
        elif early_count >= 3 or (early_count >= 2 and "persistent cough" in symptoms):
            severity = "possible"
            confidence = 0.65
        elif early_count >= 1:
            severity = "monitor"
            confidence = 0.45
        else:
            severity = "unclear"
            confidence = 0.30
        
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
        elif severity == "high_suspicion":
            response = self._generate_high_suspicion_response_hindi(assessment, symptoms)
        elif severity == "suspected":
            response = self._generate_suspected_response_hindi(assessment, symptoms)
        elif severity == "possible":
            response = self._generate_possible_response_hindi(assessment, symptoms)
        elif severity == "monitor":
            response = self._generate_monitor_response_hindi(assessment, symptoms)
        else:
            response = self._generate_general_response_hindi(assessment, symptoms)
        
        return response
    
    def _generate_emergency_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate emergency response in Hindi."""
        return {
            "severity": "emergency",
            "title": "🚨 तत्काल चिकित्सा सहायता आवश्यक",
            "message": f"""आपके बताए गए लक्षण गंभीर टीबी या जटिलताओं का संकेत दे रहे हैं।

🚨 तुरंत करें:
• नजदीकी अस्पताल जाएं
• इमरजेंसी विभाग से संपर्क करें
• सांस की मास्क का उपयोग करें
• दूसरों से दूरी बनाए रखें

खतरनाक लक्षण:
{', '.join(assessment['emergency_symptoms'])}

टीबी एक संक्रामक बीमारी है इसलिए दूसरों की सुरक्षा के लिए सावधानी बरतें।""",
            "disclaimer": self.tb_constants.HINDI_TB_DISCLAIMERS["emergency"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_high_suspicion_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate high suspicion response in Hindi."""
        return {
            "severity": "high_suspicion",
            "title": "⚠️ टीबी की उच्च संभावना",
            "message": f"""आपके लक्षण टीबी की प्रबल संभावना दर्शाते हैं।

⚠️ जरूरी कदम:
• अगले 24 घंटों में डॉक्टर से मिलें
• कफ की जांच (स्पूटम टेस्ट) कराएं
• छाती का एक्स-रे कराएं
• परिवारजनों की जांच कराएं

प्रबल संदेह के लक्षण:
{', '.join(assessment['warning_symptoms'])}

🔸 संक्रमण रोकथाम के लिए:
• खांसते समय मुंह ढकें
• पर्याप्त हवा आने-जाने वाली जगह रहें
• दूसरों से दूरी बनाए रखें""",
            "disclaimer": self.tb_constants.HINDI_TB_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_suspected_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate suspected TB response in Hindi."""
        return {
            "severity": "suspected",
            "title": "🩺 टीबी के संदिग्ध लक्षण",
            "message": f"""आपके लक्षण टीबी से मेल खाते हैं।

📋 सलाह:
• 2-3 दिन में डॉक्टर से मिलें
• कफ की जांच कराएं (3 दिन अलग-अलग)
• छाती का एक्स-रे कराएं
• ट्यूबरकुलिन स्किन टेस्ट (TST) कराएं

संदिग्ध लक्षण:
{', '.join(assessment['warning_symptoms'] + assessment['early_symptoms'])}

🔸 सावधानी:
• टीबी की पुष्टि न होने तक सतर्कता बरतें
• पौष्टिक भोजन लें और पर्याप्त आराम करें
• धूम्रपान और शराब से बचें""",
            "disclaimer": self.tb_constants.HINDI_TB_DISCLAIMERS["warning"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_possible_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate possible TB response in Hindi."""
        return {
            "severity": "possible",
            "title": "🤔 टीबी के संभावित लक्षण",
            "message": f"""आपके लक्षण टीबी की प्रारंभिक अवस्था के हो सकते हैं।

💡 सलाह:
• एक सप्ताह में डॉक्टर से मिलें
• लक्षण में सुधार न हो तो कफ की जांच कराएं
• स्वस्थ जीवनशैली बनाए रखें

वर्तमान लक्षण:
{', '.join(assessment['early_symptoms'])}

🔸 निगरानी करें:
• खांसी 3 सप्ताह से ज्यादा हो तो डॉक्टर दिखाएं
• वजन कम हो रहा हो तो सचेत रहें
• रात में पसीना बढ़े तो इलाज लें""",
            "disclaimer": self.tb_constants.HINDI_TB_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }
    
    def _generate_monitor_response_hindi(self, assessment: Dict, symptoms: List[str]) -> Dict[str, str]:
        """Generate monitoring response in Hindi."""
        return {
            "severity": "monitor",
            "title": "👁️ लक्षणों पर नजर रखें",
            "message": f"""आपके बताए गए लक्षणों की निगरानी आवश्यक है।

📊 निगरानी करें:
• लक्षण कितने दिनों से हैं
• लक्षण बिगड़ रहे हैं या सुधर रहे हैं
• नए लक्षण जुड़ रहे हैं या नहीं

वर्तमान लक्षण: {', '.join(symptoms)}

⚠️ सावधानी - ये लक्षण दिखें तो तुरंत डॉक्टर दिखाएं:
• 3 सप्ताह से ज्यादा खांसी
• कफ में खून
• तेजी से वजन कम होना
• तीव्र रात का पसीना
• सांस फूलना""",
            "disclaimer": self.tb_constants.HINDI_TB_DISCLAIMERS["general"],
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
• पौष्टिक भोजन लें
• भरपूर तरल पदार्थ लें
• लक्षण बने रहें तो डॉक्टर से मिलें

वर्तमान लक्षण: {', '.join(symptoms)}

🔸 टीबी का खतरा कम करने के तरीके:
• संतुलित आहार लें
• नियमित व्यायाम करें
• धूम्रपान छोड़ें
• अच्छी हवा वाले माहौल में रहें""",
            "disclaimer": self.tb_constants.HINDI_TB_DISCLAIMERS["general"],
            "confidence": f"{assessment['confidence']*100:.0f}%"
        }

    def check_tuberculosis_symptoms_hindi(self, hindi_query: str) -> Dict[str, any]:
        """Main function to check tuberculosis symptoms from Hindi text."""
        
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
            symptoms = self.extract_tb_symptoms(hindi_query)
            
            if not symptoms:
                return {
                    "severity": "unclear",
                    "title": "🤔 लक्षण स्पष्ट नहीं",
                    "message": "आपके विवरण से स्पष्ट लक्षण समझ नहीं आए। कृपया और विस्तार से बताएं।",
                    "disclaimer": self.tb_constants.HINDI_TB_DISCLAIMERS["general"],
                    "symptoms": [],
                    "confidence": "0%"
                }
            
            # Assess severity
            assessment = self.assess_tb_severity(symptoms)
            
            # Generate response
            response = self.generate_hindi_response(assessment, symptoms)
            
            # Add metadata
            response.update({
                "symptoms": symptoms,
                "language": "hindi",
                "timestamp": datetime.now().isoformat(),
                "total_symptoms_found": len(symptoms)
            })
            
            logger.info(f"Processed Hindi TB query: {len(symptoms)} symptoms found, severity: {assessment['severity']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing Hindi TB query: {e}")
            return {
                "error": "प्रसंस्करण में समस्या हुई। कृपया फिर से कोशिश करें।",
                "language": "hindi"
            }