import requests
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from urllib.parse import urlencode
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)

class MedlinePlusAPI:
    """
    Client for interacting with MedlinePlus API to retrieve medical information.
    Focuses on malaria and symptom-related content for rural healthcare.
    """
    
    def __init__(self):
        """Initialize the MedlinePlus API client."""
        self.base_url = Settings.MEDLINEPLUS_API_URL
        self.max_retries = Settings.MAX_RETRIES
        self.timeout = Settings.REQUEST_TIMEOUT
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'Rural-Health-AI-India/1.0 (Medical Research)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def search_medical_topic(self, topic: str) -> List[Dict[str, str]]:
        """
        Search MedlinePlus for medical information on a specific topic.
        
        Args:
            topic: Medical topic to search for (e.g., "malaria", "fever symptoms")
            
        Returns:
            List of medical documents with title, summary, URL, date, and source
            
        Raises:
            requests.exceptions.HTTPError: For HTTP errors
            requests.exceptions.ConnectionError: For network errors
            ValueError: For invalid search terms
        """
        if not self._validate_search_term(topic):
            raise ValueError(f"Invalid search term: {topic}")
        
        params = {
            'db': 'healthTopics',
            'term': topic,
            'tool': 'QueryMedlineplus'
        }
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Searching MedlinePlus for topic: {topic} (attempt {attempt + 1})")
                
                response = self.session.get(
                    self.base_url,
                    params=params,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                
                # Parse XML response
                xml_data = response.text
                return self._parse_xml_results(xml_data)
                
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error for topic '{topic}': {e}")
                raise
                
            except Exception as e:
                logger.error(f"Unexpected error searching for '{topic}': {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(1)
        
        return []
    
    def _validate_search_term(self, term: str) -> bool:
        """
        Validate search term for medical query.
        
        Args:
            term: Search term to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not term or not isinstance(term, str):
            return False
        
        term = term.strip()
        
        # Check length constraints
        if len(term) < 2 or len(term) > 100:
            return False
        
        # Check for only whitespace
        if not term or term.isspace():
            return False
        
        return True
    
    def _parse_xml_results(self, xml_data: str) -> List[Dict[str, str]]:
        """
        Parse MedlinePlus XML API response into standardized format.
        
        Args:
            xml_data: Raw XML response data
            
        Returns:
            List of parsed medical documents
        """
        results = []
        
        try:
            # Parse XML
            root = ET.fromstring(xml_data)
            logger.debug(f"Parsed XML root: {root.tag}")
            
            # Find all document elements
            documents = root.findall('.//document')
            logger.debug(f"Found {len(documents)} documents")
            
            for doc in documents:
                content = doc.find('content')
                if content is not None:
                    # Extract fields with fallback to empty string
                    title_elem = content.find('title')
                    summary_elem = content.find('summary')
                    url_elem = content.find('url')
                    date_elem = content.find('date')
                    
                    title = title_elem.text if title_elem is not None and title_elem.text else ''
                    summary = summary_elem.text if summary_elem is not None and summary_elem.text else ''
                    url = url_elem.text if url_elem is not None and url_elem.text else ''
                    date = date_elem.text if date_elem is not None and date_elem.text else ''
                    
                    logger.debug(f"Extracted: title='{title}', summary='{summary}'")
                    
                    parsed_doc = {
                        'title': title,
                        'summary': summary,
                        'url': url,
                        'date': date,
                        'source': 'medlineplus'
                    }
                    
                    # Only include documents with essential information
                    if parsed_doc['title'] and parsed_doc['summary']:
                        results.append(parsed_doc)
                        logger.debug(f"Added document: {parsed_doc['title']}")
                    else:
                        logger.debug(f"Skipped document due to missing title or summary")
                
        except ET.ParseError as e:
            logger.error(f"Error parsing XML response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error parsing search results: {e}")
            
        logger.info(f"Parsed {len(results)} documents from XML response")
        return results
    
    def search_malaria_information(self) -> List[Dict[str, str]]:
        """
        Retrieve comprehensive malaria information from MedlinePlus.
        
        Returns:
            List of malaria-related medical documents
        """
        malaria_topics = [
            "malaria",
            "malaria symptoms", 
            "malaria prevention",
            "malaria treatment",
            "mosquito-borne diseases",
            "fever in tropical areas"
        ]
        
        all_results = []
        
        for topic in malaria_topics:
            try:
                results = self.search_medical_topic(topic)
                all_results.extend(results)
                
                # Add delay between requests to be respectful to the API
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to retrieve information for topic '{topic}': {e}")
                continue
        
        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        logger.info(f"Retrieved {len(unique_results)} unique malaria documents")
        return unique_results
    
    def search_symptom_information(self, symptoms: List[str]) -> List[Dict[str, str]]:
        """
        Search for information about specific symptoms.
        
        Args:
            symptoms: List of symptoms to search for
            
        Returns:
            List of symptom-related medical documents
        """
        all_results = []
        
        for symptom in symptoms:
            search_terms = [
                f"{symptom} symptoms",
                f"{symptom} causes",
                f"when to see doctor {symptom}"
            ]
            
            for search_term in search_terms:
                try:
                    results = self.search_medical_topic(search_term)
                    all_results.extend(results)
                    time.sleep(0.5)  # Small delay between requests
                    
                except Exception as e:
                    logger.error(f"Failed to search for symptom '{symptom}': {e}")
                    continue
        
        # Remove duplicates
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        return unique_results