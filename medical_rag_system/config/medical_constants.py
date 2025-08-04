from typing import Dict, List, Set

class DengueConstants:
    """Medical constants and definitions for dengue detection and triage."""
    
    # Emergency symptoms that require immediate medical attention
    EMERGENCY_SYMPTOMS: Set[str] = {
        "plasma leakage", "severe bleeding", "internal bleeding", "nosebleed persistent",
        "gum bleeding", "vomiting blood", "blood in stool", "black stool",
        "severe abdominal pain", "persistent vomiting", "difficulty breathing",
        "restlessness", "lethargy", "confusion", "irritability",
        "cold clammy skin", "weak pulse", "low blood pressure",
        "seizure", "seizures", "unconscious", "unconsciousness"
    }
    
    # Warning signs requiring urgent medical care
    WARNING_SYMPTOMS: Set[str] = {
        "abdominal pain", "persistent vomiting", "clinical fluid accumulation",
        "mucosal bleeding", "increased vascular permeability", "thrombocytopenia",
        "rapid breathing", "fatigue", "restlessness", "skin paleness"
    }
    
    # Early/typical dengue symptoms
    EARLY_SYMPTOMS: Set[str] = {
        "high fever", "severe headache", "eye pain", "retro-orbital pain",
        "muscle aches", "joint aches", "bone pain", "back pain",
        "skin rash", "nausea", "vomiting", "loss of appetite",
        "weakness", "fatigue", "body aches", "chills"
    }
    
    # Bengali dengue symptom translations
    BENGALI_DENGUE_SYMPTOMS: Dict[str, str] = {
        # Basic dengue symptoms
        "তীব্র জ্বর": "high fever",
        "প্রচণ্ড জ্বর": "high fever", 
        "গুরুতর মাথাব্যথা": "severe headache",
        "প্রচণ্ড মাথাব্যথা": "severe headache",
        "চোখের ব্যথা": "eye pain",
        "চোখের পেছনে ব্যথা": "retro-orbital pain",
        "পেশীর ব্যথা": "muscle aches",
        "গা ব্যথা": "body aches",
        "শরীর ব্যথা": "body aches",
        "হাড়ের ব্যথা": "bone pain",
        "জয়েন্টের ব্যথা": "joint aches",
        "কোমরের ব্যথা": "back pain",
        "র‍্যাশ": "skin rash",
        "চামড়ায় দাগ": "skin rash",
        "বমি": "vomiting",
        "বমি বমি ভাব": "nausea",
        "ক্ষুধামন্দা": "loss of appetite",
        "দুর্বলতা": "weakness",
        "ক্লান্তি": "fatigue",
        "কাঁপুনি": "chills",
        
        # Warning signs
        "পেটের ব্যথা": "abdominal pain",
        "তীব্র পেট ব্যথা": "severe abdominal pain",
        "ক্রমাগত বমি": "persistent vomiting",
        "নাক দিয়ে রক্ত": "nosebleed",
        "দাঁতের মাড়ি দিয়ে রক্ত": "gum bleeding",
        "রক্তবমি": "vomiting blood",
        "পায়খানায় রক্ত": "blood in stool",
        "কালো পায়খানা": "black stool",
        "শ্বাসকষ্ট": "difficulty breathing",
        "দ্রুত শ্বাস": "rapid breathing",
        "অস্থিরতা": "restlessness",
        "ঝিমুনি": "lethargy",
        "বিভ্রান্তি": "confusion",
        "খিটখিটে ভাব": "irritability",
        "ঠান্ডা ঘাম": "cold clammy skin",
        "দুর্বল নাড়ি": "weak pulse",
        "চামড়া ফ্যাকাশে": "skin paleness",
        
        # Emergency symptoms
        "অজ্ঞান": "unconscious",
        "অচেতন": "unconscious",
        "খিঁচুনি": "seizures",
        "রক্তক্ষরণ": "bleeding",
        "অভ্যন্তরীণ রক্তক্ষরণ": "internal bleeding",
        
        # Common expressions
        "ডেঙ্গুর লক্ষণ": "dengue symptoms",
        "ডেঙ্গু জ্বর": "dengue fever",
        "হাড় ভাঙা জ্বর": "bone-breaking fever",
        "শরীর খারাপ": "feeling unwell",
        "তবিয়ত খারাপ": "feeling sick"
    }
    
    # Hindi dengue symptom translations  
    HINDI_DENGUE_SYMPTOMS: Dict[str, str] = {
        # Basic dengue symptoms
        "तेज बुखार": "high fever",
        "तीव्र बुखार": "high fever",
        "गंभीर सिर दर्द": "severe headache",
        "प्रचंड सिर दर्द": "severe headache", 
        "आंखों में दर्द": "eye pain",
        "आंखों के पीछे दर्द": "retro-orbital pain",
        "मांसपेशियों में दर्द": "muscle aches",
        "शरीर में दर्द": "body aches",
        "हड्डी में दर्द": "bone pain",
        "जोड़ों में दर्द": "joint aches",
        "कमर दर्द": "back pain",
        "रैश": "skin rash",
        "चकत्ते": "skin rash",
        "उल्टी": "vomiting",
        "जी मिचलाना": "nausea",
        "भूख न लगना": "loss of appetite",
        "कमजोरी": "weakness",
        "थकान": "fatigue",
        "कंपकंपी": "chills",
        
        # Warning signs  
        "पेट दर्द": "abdominal pain",
        "तेज पेट दर्द": "severe abdominal pain",
        "लगातार उल्टी": "persistent vomiting",
        "नाक से खून": "nosebleed",
        "मसूड़ों से खून": "gum bleeding",
        "खून की उल्टी": "vomiting blood",
        "मल में खून": "blood in stool",
        "काला मल": "black stool",
        "सांस लेने में तकलीफ": "difficulty breathing",
        "तेज सांस": "rapid breathing",
        "बेचैनी": "restlessness",
        "सुस्ती": "lethargy",
        "भ्रम": "confusion",
        "चिड़चिड़ाहट": "irritability",
        "ठंडा पसीना": "cold clammy skin",
        "कमजोर नाड़ी": "weak pulse",
        "पीली त्वचा": "skin paleness",
        
        # Emergency symptoms
        "बेहोशी": "unconscious",
        "दौरे": "seizures", 
        "रक्तस्राव": "bleeding",
        "आंतरिक रक्तस्राव": "internal bleeding",
        
        # Common expressions
        "डेंगू के लक्षण": "dengue symptoms",
        "डेंगू बुखार": "dengue fever",
        "हड्डी तोड़ बुखार": "bone-breaking fever"
    }
    
    # Dengue disclaimer templates
    BENGALI_DENGUE_DISCLAIMERS = {
        "general": "এই তথ্য শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে এবং পেশাদার চিকিৎসা পরামর্শের বিকল্প নয়। ডেঙ্গু সন্দেহ হলে অবিলম্বে চিকিৎসকের পরামর্শ নিন।",
        "warning": "⚠️ সতর্কতা: এই লক্ষণগুলি ডেঙ্গুর গুরুতর পর্যায়ের ইঙ্গিত দিতে পারে। অবিলম্বে নিকটস্থ হাসপাতালে যান।",
        "emergency": "🚨 জরুরি অবস্থা: এই লক্ষণগুলি ডেঙ্গু হেমোরেজিক ফিভার বা ডেঙ্গু শক সিনড্রোমের ইঙ্গিত দিতে পারে। তাৎক্ষণিক চিকিৎসা সেবা প্রয়োজন।"
    }
    
    HINDI_DENGUE_DISCLAIMERS = {
        "general": "यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है और पेशेवर चिकित्सा सलाह का विकल्प नहीं है। डेंगू का संदेह होने पर तुरंत डॉक्टर से सलाह लें।",
        "warning": "⚠️ चेतावनी: ये लक्षण डेंगू की गंभीर अवस्था का संकेत हो सकते हैं। तुरंत नजदीकी अस्पताल जाएं।",
        "emergency": "🚨 आपातकाल: ये लक्षण डेंगू हेमोरेजिक फीवर या डेंगू शॉक सिंड्रोम का संकेत हो सकते हैं। तत्काल चिकित्सा सहायता की आवश्यकता है।"
    }

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