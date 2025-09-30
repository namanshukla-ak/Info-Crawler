"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class SearchType(str, Enum):
    """Search type enumeration"""
    EXECUTIVE = "Executive"
    ACADEMIC = "Academic"
    RESEARCH = "Research"
    ADMINISTRATIVE = "Administrative"
    GENERAL = "General"


class WorkflowStatus(str, Enum):
    """Workflow status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ModuleStatus(str, Enum):
    """Module status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class NewsCategory(str, Enum):
    """News category enumeration"""
    LEADERSHIP_CHANGE = "Leadership Change"
    ORGANIZATIONAL_DEVELOPMENT = "Organizational Development"
    FINANCIAL = "Financial"
    SCANDAL = "Scandal"
    GENERAL = "General"
    ACHIEVEMENT = "Achievement"
    PARTNERSHIP = "Partnership"
    EXPANSION = "Expansion"


# Request Models
class BiosRequest(BaseModel):
    """Request model for fetching bios"""
    org_name: str = Field(..., description="Organization name", min_length=1)
    role_title: str = Field(..., description="Role title to search for", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "org_name": "Harvard University",
                "role_title": "Chief Financial Officer"
            }
        }


class JobsRequest(BaseModel):
    """Request model for fetching jobs"""
    role_title: str = Field(..., description="Job title to search for", min_length=1)
    search_type: SearchType = Field(SearchType.GENERAL, description="Type of search")
    
    class Config:
        json_schema_extra = {
            "example": {
                "role_title": "Chief Financial Officer",
                "search_type": "Executive"
            }
        }


class NewsRequest(BaseModel):
    """Request model for fetching news"""
    org_name: str = Field(..., description="Organization name", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "org_name": "Harvard University"
            }
        }


class TriggerRequest(BaseModel):
    """Request model for triggering workflow"""
    org_name: str = Field(..., description="Organization name", min_length=1)
    role_title: str = Field(..., description="Role title to search for", min_length=1)
    search_type: SearchType = Field(SearchType.GENERAL, description="Type of search")
    
    class Config:
        json_schema_extra = {
            "example": {
                "org_name": "Harvard University",
                "role_title": "Chief Financial Officer",
                "search_type": "Executive"
            }
        }


# Response Models
class PersonBio(BaseModel):
    """Person bio model"""
    name: str
    title: str
    organization: str
    bio_short: str
    bio_long: str
    headshot: str
    tenure: str
    email: Optional[str] = None
    education: Optional[List[str]] = []
    previous_positions: Optional[List[str]] = []


class BiosResponse(BaseModel):
    """Response model for bios endpoint"""
    bios: List[PersonBio]
    count: int
    org_name: str
    role_title: str
    timestamp: datetime = Field(default_factory=datetime.now)


class JobPosting(BaseModel):
    """Job posting model"""
    title: str
    organization: str
    location: str
    posted_date: str
    salary_range: str
    job_board: str
    url: str
    description: str
    employment_type: Optional[str] = "Full-time"
    application_deadline: Optional[str] = None


class JobsResponse(BaseModel):
    """Response model for jobs endpoint"""
    jobs: List[JobPosting]
    count: int
    role_title: str
    search_type: str
    timestamp: datetime = Field(default_factory=datetime.now)


class NewsArticle(BaseModel):
    """News article model"""
    title: str
    source: str
    published_date: str
    url: str
    summary: str
    category: str
    tags: List[str]
    author: Optional[str] = None
    read_time: Optional[str] = None


class NewsResponse(BaseModel):
    """Response model for news endpoint"""
    news: List[NewsArticle]
    count: int
    org_name: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ModuleProgress(BaseModel):
    """Module progress model"""
    status: ModuleStatus
    count: int = 0
    message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TriggerResponse(BaseModel):
    """Response model for trigger endpoint"""
    run_id: str
    status: WorkflowStatus
    message: str
    created_at: datetime = Field(default_factory=datetime.now)
    org_name: str
    role_title: str
    search_type: str


class StatusResponse(BaseModel):
    """Response model for status endpoint"""
    run_id: str
    status: WorkflowStatus
    bios_count: int = 0
    jobs_count: int = 0
    news_count: int = 0
    modules: Dict[str, ModuleProgress]
    created_at: datetime
    updated_at: datetime = Field(default_factory=datetime.now)


class ExportUrls(BaseModel):
    """Export URLs model"""
    csv: Optional[str] = None
    docx: Optional[str] = None
    pdf: Optional[str] = None


class ExportsResponse(BaseModel):
    """Response model for exports endpoint"""
    run_id: str
    urls: ExportUrls
    status: str
    message: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
    services: Dict[str, str] = {
        "api": "healthy",
        "data_generator": "healthy"
    }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
