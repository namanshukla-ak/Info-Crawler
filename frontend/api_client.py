"""
API utilities for communicating with backend services
"""
import requests
from typing import Dict, List, Optional, Any
import logging
from config import Config

logger = logging.getLogger(__name__)


class APIClient:
    """Client for backend API communication"""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or Config.API_BASE_URL
        self.timeout = timeout or Config.API_TIMEOUT
        self.session = requests.Session()
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request to backend API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: JSON payload for POST requests
            params: Query parameters for GET requests
            
        Returns:
            Response JSON or None if error
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {method} {endpoint}")
            raise Exception(f"Request timed out after {self.timeout}s")
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for {method} {endpoint}")
            raise Exception("Cannot connect to backend API. Please check if the backend is running.")
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} for {method} {endpoint}")
            error_detail = e.response.json().get("detail", str(e)) if e.response.text else str(e)
            raise Exception(f"API error: {error_detail}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {method} {endpoint}: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
    
    def fetch_bios(self, org_name: str, role_title: str) -> List[Dict]:
        """
        Fetch people bios from organization
        
        Args:
            org_name: Organization name
            role_title: Role/title to search for
            
        Returns:
            List of bio dictionaries
        """
        result = self._make_request(
            "POST",
            "/bios",
            data={"org_name": org_name, "role_title": role_title}
        )
        return result.get("bios", []) if result else []
    
    def fetch_jobs(self, role_title: str, search_type: str) -> List[Dict]:
        """
        Fetch competing job searches
        
        Args:
            role_title: Job title to search for
            search_type: Type of search (Executive, Academic, etc.)
            
        Returns:
            List of job posting dictionaries
        """
        result = self._make_request(
            "POST",
            "/jobs",
            data={"role_title": role_title, "search_type": search_type}
        )
        return result.get("jobs", []) if result else []
    
    def fetch_news(self, org_name: str) -> List[Dict]:
        """
        Fetch and summarize news articles
        
        Args:
            org_name: Organization name
            
        Returns:
            List of news article dictionaries
        """
        result = self._make_request(
            "POST",
            "/news",
            data={"org_name": org_name}
        )
        return result.get("news", []) if result else []
    
    def trigger_workflow(
        self, 
        org_name: str, 
        role_title: str, 
        search_type: str
    ) -> Optional[str]:
        """
        Trigger complete workflow
        
        Args:
            org_name: Organization name
            role_title: Role/title to search for
            search_type: Type of search
            
        Returns:
            Run ID if successful, None otherwise
        """
        result = self._make_request(
            "POST",
            "/trigger",
            data={
                "org_name": org_name,
                "role_title": role_title,
                "search_type": search_type
            }
        )
        return result.get("run_id") if result else None
    
    def get_workflow_status(self, run_id: str) -> Optional[Dict]:
        """
        Get status of workflow run
        
        Args:
            run_id: Workflow run ID
            
        Returns:
            Status dictionary or None
        """
        return self._make_request("GET", f"/status/{run_id}")
    
    def get_export_urls(self, run_id: str) -> Optional[Dict]:
        """
        Get presigned URLs for export files
        
        Args:
            run_id: Workflow run ID
            
        Returns:
            Dictionary with export URLs or None
        """
        return self._make_request("GET", f"/exports/{run_id}")
    
    def health_check(self) -> bool:
        """
        Check if backend API is healthy
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            result = self._make_request("GET", "/health")
            return result.get("status") == "healthy" if result else False
        except Exception:
            return False
