from src.data_collection.data_processor import DataProcessor

text = "  Malaria causes fever and chills. Emergency: high fever requires immediate care.  "

processor = DataProcessor()
cleaned = processor.clean_text(text)
print("Cleaned text:", repr(cleaned))

symptoms = processor.extract_symptoms(cleaned)
print("Symptoms:", symptoms)

emergency_indicators = processor.detect_emergency_indicators(cleaned)
print("Emergency indicators:", emergency_indicators)

# Check if "high fever" is in emergency keywords
print("Emergency keywords:", list(processor.emergency_keywords))
print("'high fever' in emergency keywords:", "high fever" in processor.emergency_keywords)