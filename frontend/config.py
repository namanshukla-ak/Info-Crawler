"""
Configuration module for Streamlit frontend application
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    
    # UI Configuration
    PAGE_TITLE: str = "Research Intelligence Platform"
    PAGE_ICON: str = "🔍"
    LAYOUT: str = "wide"
    
    # Feature Flags
    ENABLE_AUTO_REFRESH: bool = os.getenv("ENABLE_AUTO_REFRESH", "true").lower() == "true"
    AUTO_REFRESH_INTERVAL: int = int(os.getenv("AUTO_REFRESH_INTERVAL", "5"))
    
    # Export Configuration
    EXPORT_FORMATS: list = ["csv"]  # Future: ["csv", "docx", "pdf"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    
    # Theme
    PRIMARY_COLOR: str = "#1f77b4"
    BACKGROUND_COLOR: str = "#ffffff"
    SECONDARY_BACKGROUND_COLOR: str = "#f8f9fa"
    
    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        """Get full API URL for an endpoint"""
        return f"{cls.API_BASE_URL}{endpoint}"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.API_BASE_URL:
            raise ValueError("API_BASE_URL is required")
        return True

# Validate on import
Config.validate()
