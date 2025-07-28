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
        "body pain", "joint aches", "feeling unwell", "malaise"
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
        "सांस लेने में तकलीफ": "difficulty breathing"
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