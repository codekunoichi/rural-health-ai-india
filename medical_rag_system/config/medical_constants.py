from typing import Dict, List, Set

class MalariaConstants:
    """Medical constants and definitions for malaria detection and triage."""
    
    # Emergency symptoms that require immediate medical attention
    EMERGENCY_SYMPTOMS: Set[str] = {
        "unconscious", "unconsciousness", "coma", "seizure", "seizures",
        "convulsion", "convulsions", "difficulty breathing", "shortness of breath",
        "severe vomiting", "repeated vomiting", "blood in vomit", "black vomit",
        "confusion", "delirium", "severe headache", "neck stiffness",
        "yellowing skin", "jaundice", "dark urine", "bloody urine",
        "severe weakness", "collapse", "unable to sit", "unable to stand",
        "high fever", "fever above 104", "fever over 40"
    }
    
    # Severe symptoms requiring urgent medical care
    SEVERE_SYMPTOMS: Set[str] = {
        "persistent fever", "severe chills", "rigors", "profuse sweating", "night sweats",
        "severe muscle pain", "body aches", "joint pain",
        "persistent headache", "nausea", "vomiting",
        "diarrhea", "abdominal pain", "stomach pain"
    }
    
    # Early/mild symptoms of malaria
    EARLY_SYMPTOMS: Set[str] = {
        "fever", "headache", "chills", "muscle aches", "tiredness",
        "fatigue", "weakness", "loss of appetite", "mild nausea",
        "body pain", "joint aches", "feeling unwell", "malaise", "sweating"
    }
    
    # Hindi symptom translations
    HINDI_SYMPTOMS: Dict[str, str] = {
        "बुखार": "fever",
        "सिर दर्द": "headache", 
        "सिरदर्द": "headache",
        "कंपकंपी": "chills",
        "मांसपेशियों में दर्द": "muscle pain",
        "कमजोरी": "weakness",
        "थकान": "fatigue",
        "उल्टी": "vomiting",
        "दस्त": "diarrhea",
        "पेट दर्द": "stomach pain",
        "बेहोशी": "unconsciousness",
        "दौरे": "seizures",
        "सांस लেने में तकলीफ": "difficulty breathing",
        # Additional Hindi symptoms
        "तेज बुखार": "high fever",
        "गले में खराश": "sore throat",
        "खांसी": "cough",
        "सर चकराना": "dizziness",
        "भूख न लगना": "loss of appetite",
        "जी मिचलाना": "nausea",
        "शरीर में दर्द": "body aches",
        "जोड़ों में दर्द": "joint pain"
    }
    
    # Bengali symptom translations
    BENGALI_SYMPTOMS: Dict[str, str] = {
        # Basic symptoms
        "জ্বর": "fever",
        "মাথাব্যথা": "headache",
        "মাথা ব্যথা": "headache",
        "কাঁপুনি": "chills",
        "ঠান্ডা লাগা": "chills",
        "পেশীর ব্যথা": "muscle pain",
        "দুর্বলতা": "weakness",
        "ক্লান্তি": "fatigue",
        "বমি": "vomiting",
        "বমি বমি ভাব": "nausea",
        "ডায়রিয়া": "diarrhea",
        "পেটের ব্যথা": "stomach pain",
        "পেট ব্যথা": "stomach pain",
        
        # Severe symptoms
        "অজ্ঞান": "unconsciousness",
        "খিঁচুনি": "seizures",
        "শ্বাসকষ্ট": "difficulty breathing",
        "তীব্র জ্বর": "high fever",
        "প্রচণ্ড জ্বর": "high fever",
        "গলা ব্যথা": "sore throat",
        "কাশি": "cough",
        "মাথা ঘোরা": "dizziness",
        "চক্কর": "dizziness",
        "ক্ষুধামন্দা": "loss of appetite",
        "খাওয়ার রুচি নেই": "loss of appetite",
        "শরীর ব্যথা": "body aches",
        "গা ব্যথা": "body aches",
        "হাড়ের ব্যথা": "bone pain",
        "জয়েন্টের ব্যথা": "joint pain",
        "গলার খুসখুসানি": "throat irritation",
        "নিঃশ্বাসে কষ্ট": "breathing difficulty",
        
        # Emergency symptoms
        "অচেতন": "unconscious",
        "অচেতন অবস্থা": "unconscious",
        "জ্ঞান হারানো": "loss of consciousness",
        "রক্তবমি": "blood in vomit",
        "কালো বমি": "black vomit",
        "গুরুতর মাথাব্যথা": "severe headache",
        "ঘাড় শক্ত": "neck stiffness",
        "চোখ হলুদ": "yellow eyes",
        "জন্ডিস": "jaundice",
        "প্রস্রাবে রক্ত": "blood in urine",
        "গাঢ় প্রস্রাব": "dark urine",
        
        # Common expressions
        "শরীর খারাপ": "feeling unwell",
        "খারাপ লাগছে": "feeling unwell",
        "অসুস্থ লাগছে": "feeling sick", 
        "কেমন যেন লাগছে": "feeling strange",
        "গা গুলানো": "nausea",
        "পেট খারাপ": "stomach upset"
    }
    
    # Risk factors for malaria
    RISK_FACTORS: Set[str] = {
        "mosquito bite", "mosquito exposure", "rural area", "forest area",
        "pregnancy", "pregnant", "travel", "recent travel", "rainy season",
        "stagnant water", "no bed net", "evening outdoor activity"
    }
    
    # Medical disclaimer templates
    DISCLAIMERS = {
        "general": "This information is for educational purposes only and does not replace professional medical advice. Always consult with a healthcare provider for medical concerns.",
        "emergency": "⚠️ EMERGENCY: These symptoms may indicate a serious condition. Seek immediate medical attention at the nearest hospital or healthcare facility.",
        "pregnancy": "⚠️ PREGNANCY ALERT: Malaria during pregnancy can be dangerous for both mother and baby. Seek immediate medical care."
    }
    
    # Bengali disclaimer templates
    BENGALI_DISCLAIMERS = {
        "general": "এই তথ্য শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে এবং পেশাদার চিকিৎসা পরামর্শের বিকল্প নয়। স্বাস্থ্য সংক্রান্ত যেকোনো সমস্যার জন্য সর্বদা একজন চিকিৎসকের পরামর্শ নিন।",
        "emergency": "⚠️ জরুরি অবস্থা: এই লক্ষণগুলি একটি গুরুতর অবস্থার ইঙ্গিত দিতে পারে। অবিলম্বে নিকটস্থ হাসপাতাল বা স্বাস্থ্যসেবা কেন্দ্রে চিকিৎসা সেবা নিন।",
        "pregnancy": "⚠️ গর্ভাবস্থার সতর্কতা: গর্ভাবস্থায় ম্যালেরিয়া মা ও শিশু উভয়ের জন্য বিপজ্জনক হতে পারে। অবিলম্বে চিকিৎসা সেবা নিন।"
    }
    
    # Hindi disclaimer templates  
    HINDI_DISCLAIMERS = {
        "general": "यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है और पेशेवर चिकित्सा सलाह का विकल्प नहीं है। स्वास्थ्य संबंधी किसी भी समस्या के लिए हमेशा डॉक्टर से सलाह लें।",
        "emergency": "⚠️ आपातकाल: ये लक्षण एक गंभीर स्थिति का संकेत हो सकते हैं। तुरंत नजदीकी अस्पताल या स्वास्थ्य केंद्र में चिकित्सा सहायता लें।",
        "pregnancy": "⚠️ गर्भावस्था चेतावनी: गर्भावस्था में मलेरिया माँ और बच्चे दोनों के लिए खतरनाक हो सकता है। तुरंत चिकित्सा सहायता लें।"
    }
    
    # Confidence thresholds for different actions
    CONFIDENCE_THRESHOLDS = {
        "emergency_detection": 0.8,
        "malaria_likelihood": 0.6,
        "general_response": 0.4
    }
    
    # Data sources for attribution
    DATA_SOURCES = {
        "medlineplus": "MedlinePlus (U.S. National Library of Medicine)",
        "who": "World Health Organization",
        "cdc": "Centers for Disease Control and Prevention",
        "icmr": "Indian Council of Medical Research",
        "nhp": "National Health Portal India"
    }

class ResponseTemplates:
    """Templates for generating consistent medical responses."""
    
    EMERGENCY_RESPONSE = """
    🚨 EMERGENCY SITUATION DETECTED 🚨
    
    Based on the symptoms described, this may be a medical emergency requiring immediate attention.
    
    IMMEDIATE ACTION REQUIRED:
    • Go to the nearest hospital or healthcare center immediately
    • Call emergency services if available
    • Do not delay seeking medical care
    
    {disclaimer}
    
    Source: {sources}
    """
    
    MALARIA_SUSPECTED_RESPONSE = """
    ⚠️ POSSIBLE MALARIA SYMPTOMS
    
    The symptoms you've described are consistent with malaria, which is common in rural areas.
    
    RECOMMENDED ACTIONS:
    • Visit a healthcare center for malaria testing (blood test)
    • Seek medical attention within 24 hours
    • Monitor symptoms closely
    • Avoid self-medication
    
    SYMPTOM SUMMARY:
    {symptoms}
    
    {disclaimer}
    
    Source: {sources}
    Confidence: {confidence}%
    """
    
    GENERAL_HEALTH_RESPONSE = """
    HEALTH INFORMATION
    
    Based on your symptoms, here's what you should know:
    
    {information}
    
    RECOMMENDATIONS:
    • Consult with a healthcare provider for proper evaluation
    • Monitor your symptoms
    • Seek medical care if symptoms worsen
    
    {disclaimer}
    
    Source: {sources}
    Confidence: {confidence}%
    """