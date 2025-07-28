# Claude Command: Build Medical RAG System for Rural Healthcare

You are an expert Python developer specializing in AI/ML systems for healthcare applications. Build a complete Medical RAG (Retrieval-Augmented Generation) system focused on malaria symptom checking for rural Indian villages.

## Project Requirements

### Core System Components
1. **Data Collection Pipeline** - Scrape and structure medical knowledge from open sources
2. **Knowledge Base Construction** - Process and embed medical documents with metadata
3. **RAG Implementation** - Query processing with medical context and safety validation
4. **Safety Layer** - Emergency detection and medical disclaimers
5. **Testing Framework** - Comprehensive test cases for medical accuracy

### Technical Specifications

**Technology Stack:**
- Python 3.9+
- LangChain for RAG pipeline
- FAISS for vector storage
- Hugging Face Transformers for embeddings
- BeautifulSoup for web scraping
- Flask for API endpoint
- Pytest for testing

**Data Sources to Integrate:**
- MedlinePlus API (https://medlineplus.gov/webservices.html)
- WHO Malaria Fact Sheets
- CDC Malaria Information
- ICMR Malaria Guidelines
- National Health Portal India content

### Functional Requirements

**Malaria Focus Areas:**
- Early symptoms: fever, chills, headache, muscle aches
- Severe symptoms: seizures, confusion, difficulty breathing
- Risk factors: mosquito exposure, rural areas, pregnancy
- Emergency signs: unconsciousness, repeated vomiting
- Cultural context: Hindi symptom terms, rural Indian healthcare patterns

**Safety Requirements:**
- Never provide treatment recommendations
- Always include emergency escalation paths
- Detect and flag emergency symptoms immediately
- Include clear medical disclaimers
- Validate response confidence levels

### Implementation Structure

```
medical_rag_system/
├── src/
│   ├── data_collection/
│   │   ├── medlineplus_api.py
│   │   ├── web_scraper.py
│   │   └── data_processor.py
│   ├── knowledge_base/
│   │   ├── document_processor.py
│   │   ├── vector_store.py
│   │   └── embeddings.py
│   ├── rag_system/
│   │   ├── query_processor.py
│   │   ├── retrieval_engine.py
│   │   └── response_generator.py
│   ├── safety/
│   │   ├── medical_validator.py
│   │   ├── emergency_detector.py
│   │   └── disclaimer_handler.py
│   └── api/
│       ├── flask_app.py
│       └── endpoints.py
├── tests/
│   ├── test_data_collection.py
│   ├── test_knowledge_base.py
│   ├── test_rag_system.py
│   ├── test_safety_layer.py
│   └── test_medical_scenarios.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── vector_stores/
├── config/
│   ├── settings.py
│   └── medical_constants.py
├── requirements.txt
└── README.md
```

### Specific Test Cases to Implement

**Basic Malaria Symptom Scenarios:**
1. **Early Stage**: "I have fever and headache for 2 days"
2. **Multiple Symptoms**: "Fever, chills, sweating, weakness since 5 days"
3. **Severe Symptoms**: "High fever with confusion and difficulty breathing"
4. **Emergency Case**: "Patient unconscious with high fever"
5. **Pregnancy Case**: "Pregnant woman with fever and vomiting"

**Edge Cases:**
1. **Non-Malaria Symptoms**: "Cough and runny nose"
2. **Vague Symptoms**: "Not feeling well"
3. **Multiple Conditions**: "Fever with stomach pain"
4. **Cultural Terms**: "बुखार और सिर दर्द" (fever and headache in Hindi)

**Safety Test Cases:**
1. Emergency symptom detection accuracy
2. Confidence score validation
3. Disclaimer inclusion verification
4. Response time limits
5. False negative prevention (missing emergency symptoms)

### Performance Requirements
- Response time: <3 seconds for symptom queries
- Knowledge base: Support for 1000+ medical documents
- Accuracy: >90% agreement with medical professionals on triage decisions
- Offline capability: Core functionality without internet
- Scalability: Handle 100+ concurrent users

### Medical Accuracy Requirements
- Cross-reference multiple authoritative sources
- Include confidence scores for all responses
- Flag uncertain or conflicting information
- Maintain source attribution for all medical claims
- Never contradict established medical guidelines

### Deliverables Expected

1. **Complete working codebase** with all components
2. **Comprehensive test suite** with >90% coverage
3. **Documentation** including setup and usage instructions
4. **Sample API responses** for all test scenarios
5. **Performance benchmarks** and accuracy metrics
6. **Data source validation** reports
7. **Safety compliance** verification

### Additional Requirements

**Localization Support:**
- Hindi symptom terminology mapping
- Cultural context for rural Indian healthcare
- Local healthcare facility integration patterns

**Data Privacy:**
- No storage of personal health information
- Anonymized query logging only
- GDPR-compliant data handling

**Deployment Readiness:**
- Docker containerization
- Environment configuration management
- Production-ready error handling
- Monitoring and logging integration

## Development Instructions

1. **Start with data collection** - Build MedlinePlus API integration first
2. **Create knowledge base** - Process and embed malaria-specific content
3. **Implement basic RAG** - Simple query-response pipeline
4. **Add safety layer** - Emergency detection and validation
5. **Build comprehensive tests** - All scenarios mentioned above
6. **Optimize for accuracy** - Tune retrieval and generation parameters
7. **Add API endpoints** - RESTful interface for external integration

Build this as a production-ready system that can be demonstrated to government officials and medical professionals. Include extensive error handling, logging, and validation at every step.

Focus on medical accuracy above all else - this system will be used for real health decisions in underserved communities.

Provide complete, working code with detailed comments explaining the medical reasoning behind each component.