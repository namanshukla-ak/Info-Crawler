"""
Configuration module for backend application
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    APP_NAME: str = "Research Intelligence Platform API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = ""
    DEBUG: bool = False
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["*"]  # In production, specify actual origins
    
    # AWS Configuration (for production)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # S3 Configuration
    S3_BUCKET_NAME: str = "research-intelligence-data"
    S3_RAW_PREFIX: str = "raw/"
    S3_CURATED_PREFIX: str = "curated/"
    S3_EXPORTS_PREFIX: str = "exports/"
    
    # DynamoDB Configuration
    DYNAMODB_RUNS_TABLE: str = "research_runs"
    DYNAMODB_PEOPLE_TABLE: str = "research_people"
    DYNAMODB_JOBS_TABLE: str = "research_jobs"
    DYNAMODB_NEWS_TABLE: str = "research_news"
    
    # OpenSearch Configuration
    OPENSEARCH_ENDPOINT: Optional[str] = None
    OPENSEARCH_INDEX_PEOPLE: str = "people"
    OPENSEARCH_INDEX_JOBS: str = "jobs"
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    BEDROCK_MAX_TOKENS: int = 4096
    
    # Scraping Configuration
    CRAWL4AI_RATE_LIMIT: int = 2
    CRAWL4AI_TIMEOUT: int = 30
    RESPECT_ROBOTS_TXT: bool = True
    
    # News API Configuration
    NEWS_API_KEY: Optional[str] = None
    NEWS_API_PROVIDER: str = "google"  # google, bing, or chronicle
    
    # Data Generation (POC)
    SYNTHETIC_DATA_ENABLED: bool = True
    DEFAULT_BIOS_COUNT: int = 8
    DEFAULT_JOBS_COUNT: int = 15
    DEFAULT_NEWS_COUNT: int = 12
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Data Retention
    DATA_TTL_DAYS: int = 90
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()
