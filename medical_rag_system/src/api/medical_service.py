"""
Medical RAG Service for FastAPI application.
Handles medical query processing, emergency detection, and response generation.
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from src.rag_system.query_processor import MedicalQueryProcessor
from src.rag_system.retrieval_engine import MedicalRetrievalEngine
from src.rag_system.response_generator import MedicalResponseGenerator
from src.knowledge_base.vector_store import MedicalVectorStore
from src.data_collection.medlineplus_api import MedlinePlusAPI
from src.data_collection.data_processor import DataProcessor
from config.settings import Settings

logger = logging.getLogger(__name__)

class MedicalRAGService:
    """
    Main service class that orchestrates all medical RAG components.
    Provides async interface for FastAPI endpoints.
    """
    
    def __init__(self):
        """Initialize the medical RAG service."""
        self.query_processor = None
        self.retrieval_engine = None
        self.response_generator = None
        self.vector_store = None
        self.api_client = None
        self.data_processor = None
        
        self.initialized = False
        self.initialization_time = None
        self.query_count = 0
        self.error_count = 0
        
        logger.info("MedicalRAGService instance created")
    
    async def initialize(self):
        """Initialize all components asynchronously."""
        try:
            logger.info("Initializing Medical RAG Service components...")
            start_time = time.time()
            
            # Initialize components
            await self._initialize_components()
            
            # Load or build knowledge base
            await self._initialize_knowledge_base()
            
            self.initialized = True
            self.initialization_time = time.time() - start_time
            
            logger.info(f"Medical RAG Service initialized successfully in {self.initialization_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to initialize Medical RAG Service: {e}")
            raise
    
    async def _initialize_components(self):
        """Initialize all RAG components."""
        # Initialize synchronous components
        self.query_processor = MedicalQueryProcessor()
        self.response_generator = MedicalResponseGenerator()
        self.api_client = MedlinePlusAPI()
        self.data_processor = DataProcessor()
        
        # Initialize vector store (async operation)
        self.vector_store = MedicalVectorStore()
        
        # Initialize retrieval engine
        self.retrieval_engine = MedicalRetrievalEngine()
        
        logger.info("All RAG components initialized")
    
    async def _initialize_knowledge_base(self):
        """Initialize or load the knowledge base."""
        try:
            # Try to load existing knowledge base
            if await self._load_existing_knowledge_base():
                logger.info("Loaded existing knowledge base")
                return
            
            # If no existing KB, build a minimal one for demo
            logger.info("Building minimal knowledge base for demo...")
            await self._build_minimal_knowledge_base()
            
        except Exception as e:
            logger.warning(f"Knowledge base initialization failed: {e}")
            logger.info("Service will continue with limited functionality")
    
    async def _load_existing_knowledge_base(self) -> bool:
        """Try to load existing knowledge base."""
        try:
            # This would load a pre-built knowledge base
            # For now, return False to build minimal KB
            return False
        except Exception:
            return False
    
    async def _build_minimal_knowledge_base(self):
        """Build a minimal knowledge base for demonstration."""
        # Create minimal medical documents for demo
        demo_documents = [
            {
                'id': 'malaria_overview',
                'content': 'Malaria is a serious disease caused by parasites transmitted through infected mosquito bites. Common symptoms include fever, chills, headache, muscle aches, and fatigue. High fever, severe headache, and vomiting may indicate severe malaria requiring immediate medical attention.',
                'metadata': {
                    'source': 'medlineplus',
                    'section_type': 'symptoms',
                    'symptoms': ['fever', 'chills', 'headache', 'muscle aches', 'fatigue'],
                    'emergency_indicators': ['high fever', 'severe headache']
                }
            },
            {
                'id': 'emergency_symptoms',
                'content': 'Emergency medical symptoms that require immediate attention include unconsciousness, seizures, difficulty breathing, severe vomiting, high fever above 104°F, severe dehydration, and chest pain. Call emergency services immediately if experiencing these symptoms.',
                'metadata': {
                    'source': 'who',
                    'section_type': 'emergency',
                    'emergency_indicators': ['unconsciousness', 'seizures', 'difficulty breathing', 'high fever'],
                    'symptoms': []
                }
            },
            {
                'id': 'fever_guidance',
                'content': 'Fever is a common symptom that can indicate various conditions. Monitor temperature regularly, stay hydrated, and seek medical attention if fever persists beyond 2-3 days or is accompanied by severe symptoms. In malaria-endemic areas, any fever should be evaluated promptly.',
                'metadata': {
                    'source': 'cdc',
                    'section_type': 'symptoms',
                    'symptoms': ['fever'],
                    'emergency_indicators': []
                }
            }
        ]
        
        # Build vector index
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, self.vector_store.build_index, demo_documents
            )
            logger.info("Minimal knowledge base built successfully")
        except Exception as e:
            logger.error(f"Failed to build minimal knowledge base: {e}")
            raise
    
    async def process_query(self, query: str, language: str = "auto", 
                          include_sources: bool = True, max_results: int = 5) -> Dict[str, Any]:
        """
        Process a medical query through the complete RAG pipeline.
        
        Args:
            query: Medical query string
            language: Query language
            include_sources: Whether to include sources
            max_results: Maximum number of results
            
        Returns:
            Complete medical response
        """
        if not self.initialized:
            raise RuntimeError("Service not initialized")
        
        start_time = time.time()
        self.query_count += 1
        
        try:
            logger.info(f"Processing query: '{query[:50]}...'")
            
            # Step 1: Process query
            processed_query = await asyncio.get_event_loop().run_in_executor(
                None, self.query_processor.process_query, query
            )
            
            # Step 2: Retrieve relevant documents
            retrieval_context = await asyncio.get_event_loop().run_in_executor(
                None, self.retrieval_engine.retrieve_relevant_documents, 
                processed_query, max_results
            )
            
            # Step 3: Generate response
            retrieval_context['query'] = processed_query
            response = await asyncio.get_event_loop().run_in_executor(
                None, self.response_generator.generate_response, retrieval_context
            )
            
            # Add processing time
            processing_time = (time.time() - start_time) * 1000
            response['processing_time_ms'] = processing_time
            
            # Add extracted symptoms to response
            response['symptoms'] = processed_query.get('symptoms', [])
            
            # Filter sources if not requested
            if not include_sources:
                response['sources'] = None
            
            logger.info(f"Query processed successfully in {processing_time:.2f}ms")
            return response
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Query processing failed: {e}")
            raise
    
    async def check_emergency(self, query: str) -> Dict[str, Any]:
        """
        Quick emergency check without full processing.
        
        Args:
            query: Medical query to check
            
        Returns:
            Emergency detection results
        """
        if not self.initialized:
            raise RuntimeError("Service not initialized")
        
        try:
            # Just do emergency detection
            emergency_detected, indicators = await asyncio.get_event_loop().run_in_executor(
                None, self.query_processor.detect_emergency_intent, query
            )
            
            recommendations = []
            if emergency_detected:
                recommendations = [
                    "Seek immediate medical attention",
                    "Call emergency services if available",
                    "Go to the nearest hospital or healthcare facility"
                ]
            
            return {
                "emergency_detected": emergency_detected,
                "emergency_indicators": indicators,
                "confidence": 0.9 if emergency_detected else 0.1,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Emergency check failed: {e}")
            raise
    
    async def extract_symptoms(self, query: str) -> List[str]:
        """
        Extract symptoms from a query.
        
        Args:
            query: Medical query
            
        Returns:
            List of extracted symptoms
        """
        if not self.initialized:
            raise RuntimeError("Service not initialized")
        
        try:
            symptoms = await asyncio.get_event_loop().run_in_executor(
                None, self.query_processor.extract_symptoms, query
            )
            return symptoms
            
        except Exception as e:
            logger.error(f"Symptom extraction failed: {e}")
            raise
    
    async def health_check(self) -> bool:
        """
        Perform health check on all components.
        
        Returns:
            True if all components are healthy
        """
        try:
            if not self.initialized:
                return False
            
            # Check if key components are available
            checks = [
                self.query_processor is not None,
                self.retrieval_engine is not None,
                self.response_generator is not None,
                self.vector_store is not None
            ]
            
            return all(checks)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get detailed system status information.
        
        Returns:
            System status dictionary
        """
        try:
            components = {
                "query_processor": {
                    "status": "operational" if self.query_processor else "error",
                    "initialized": self.query_processor is not None
                },
                "retrieval_engine": {
                    "status": "operational" if self.retrieval_engine else "error",
                    "initialized": self.retrieval_engine is not None
                },
                "response_generator": {
                    "status": "operational" if self.response_generator else "error",
                    "initialized": self.response_generator is not None
                },
                "vector_store": {
                    "status": "operational" if self.vector_store else "error",
                    "initialized": self.vector_store is not None,
                    "documents_count": len(getattr(self.vector_store, 'documents', []))
                }
            }
            
            statistics = {
                "total_queries": self.query_count,
                "total_errors": self.error_count,
                "uptime_seconds": time.time() - (self.initialization_time or time.time()) if self.initialization_time else 0,
                "initialization_time_seconds": self.initialization_time,
                "error_rate": self.error_count / max(self.query_count, 1)
            }
            
            overall_status = "operational" if self.initialized and all(
                comp["status"] == "operational" for comp in components.values()
            ) else "degraded"
            
            return {
                "system_status": overall_status,
                "components": components,
                "statistics": statistics,
                "last_updated": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"System status check failed: {e}")
            return {
                "system_status": "error",
                "components": {},
                "statistics": {},
                "last_updated": datetime.now()
            }
    
    async def cleanup(self):
        """Cleanup resources on shutdown."""
        try:
            logger.info("Cleaning up Medical RAG Service...")
            
            # Cleanup components if needed
            if self.vector_store:
                # Save current state if needed
                pass
            
            self.initialized = False
            logger.info("Medical RAG Service cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")