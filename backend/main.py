"""
FastAPI Backend for Research Intelligence Platform
POC with synthetic data generation
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import uuid
from typing import Dict
import asyncio
import logging

from models import (
    BiosRequest, BiosResponse, PersonBio,
    JobsRequest, JobsResponse, JobPosting,
    NewsRequest, NewsResponse, NewsArticle,
    TriggerRequest, TriggerResponse, StatusResponse,
    ExportsResponse, ExportUrls, HealthResponse,
    WorkflowStatus, ModuleStatus, ModuleProgress,
    ErrorResponse
)
from data_generator import generate_bios, generate_jobs, generate_news

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Research Intelligence Platform API",
    description="Backend API for automated intelligence gathering and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for POC (replace with DynamoDB in production)
workflow_runs: Dict[str, Dict] = {}
workflow_data: Dict[str, Dict] = {}


# Helper functions
def simulate_processing_delay(min_seconds: float = 0.5, max_seconds: float = 2.0):
    """Simulate processing time"""
    import random
    import time
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


async def process_workflow_async(run_id: str, org_name: str, role_title: str, search_type: str):
    """
    Asynchronously process complete workflow
    Simulates the EventBridge/Lambda architecture
    """
    try:
        logger.info(f"Starting workflow {run_id}")
        
        # Update status to running
        workflow_runs[run_id]["status"] = WorkflowStatus.RUNNING
        workflow_runs[run_id]["updated_at"] = datetime.now()
        
        # Process bios module
        logger.info(f"Processing bios module for run {run_id}")
        workflow_runs[run_id]["modules"]["bios"]["status"] = ModuleStatus.RUNNING
        workflow_runs[run_id]["modules"]["bios"]["started_at"] = datetime.now()
        
        await asyncio.sleep(2)  # Simulate processing
        bios = generate_bios(org_name, role_title, count=8)
        
        workflow_runs[run_id]["modules"]["bios"]["status"] = ModuleStatus.COMPLETED
        workflow_runs[run_id]["modules"]["bios"]["count"] = len(bios)
        workflow_runs[run_id]["modules"]["bios"]["completed_at"] = datetime.now()
        workflow_runs[run_id]["bios_count"] = len(bios)
        workflow_data[run_id]["bios"] = bios
        
        # Process jobs module
        logger.info(f"Processing jobs module for run {run_id}")
        workflow_runs[run_id]["modules"]["jobs"]["status"] = ModuleStatus.RUNNING
        workflow_runs[run_id]["modules"]["jobs"]["started_at"] = datetime.now()
        
        await asyncio.sleep(3)  # Simulate processing
        jobs = generate_jobs(role_title, search_type, count=15)
        
        workflow_runs[run_id]["modules"]["jobs"]["status"] = ModuleStatus.COMPLETED
        workflow_runs[run_id]["modules"]["jobs"]["count"] = len(jobs)
        workflow_runs[run_id]["modules"]["jobs"]["completed_at"] = datetime.now()
        workflow_runs[run_id]["jobs_count"] = len(jobs)
        workflow_data[run_id]["jobs"] = jobs
        
        # Process news module
        logger.info(f"Processing news module for run {run_id}")
        workflow_runs[run_id]["modules"]["news"]["status"] = ModuleStatus.RUNNING
        workflow_runs[run_id]["modules"]["news"]["started_at"] = datetime.now()
        
        await asyncio.sleep(2.5)  # Simulate processing
        news = generate_news(org_name, count=12)
        
        workflow_runs[run_id]["modules"]["news"]["status"] = ModuleStatus.COMPLETED
        workflow_runs[run_id]["modules"]["news"]["count"] = len(news)
        workflow_runs[run_id]["modules"]["news"]["completed_at"] = datetime.now()
        workflow_runs[run_id]["news_count"] = len(news)
        workflow_data[run_id]["news"] = news
        
        # Mark workflow as completed
        workflow_runs[run_id]["status"] = WorkflowStatus.COMPLETED
        workflow_runs[run_id]["updated_at"] = datetime.now()
        
        logger.info(f"Workflow {run_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error processing workflow {run_id}: {str(e)}")
        workflow_runs[run_id]["status"] = WorkflowStatus.FAILED
        workflow_runs[run_id]["error"] = str(e)
        workflow_runs[run_id]["updated_at"] = datetime.now()


# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Research Intelligence Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Returns the health status of the API
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "api": "healthy",
            "data_generator": "healthy"
        }
    )


@app.post("/bios", response_model=BiosResponse, tags=["Data Fetching"])
async def fetch_bios(request: BiosRequest):
    """
    Fetch people bios from organization
    
    This endpoint simulates scraping an organization's website for people bios.
    In production, this would:
    - Use crawl4ai/Playwright to scrape the org website
    - Parse HTML with BeautifulSoup
    - Use Bedrock for entity extraction
    - Store results in S3 and DynamoDB
    """
    try:
        logger.info(f"Fetching bios for {request.org_name}, role: {request.role_title}")
        
        # Simulate processing delay
        simulate_processing_delay(1.0, 2.0)
        
        # Generate synthetic data
        bios = generate_bios(request.org_name, request.role_title, count=8)
        
        return BiosResponse(
            bios=[PersonBio(**bio) for bio in bios],
            count=len(bios),
            org_name=request.org_name,
            role_title=request.role_title
        )
        
    except Exception as e:
        logger.error(f"Error fetching bios: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/jobs", response_model=JobsResponse, tags=["Data Fetching"])
async def fetch_jobs(request: JobsRequest):
    """
    Fetch competing job searches
    
    This endpoint simulates querying job boards for postings.
    In production, this would:
    - Query multiple job board APIs
    - Scrape job sites with crawl4ai
    - Normalize data across sources
    - Index to OpenSearch for deduplication
    - Store results in S3 and DynamoDB
    """
    try:
        logger.info(f"Fetching jobs for role: {request.role_title}, type: {request.search_type}")
        
        # Simulate processing delay
        simulate_processing_delay(1.5, 3.0)
        
        # Generate synthetic data
        jobs = generate_jobs(request.role_title, request.search_type.value, count=15)
        
        return JobsResponse(
            jobs=[JobPosting(**job) for job in jobs],
            count=len(jobs),
            role_title=request.role_title,
            search_type=request.search_type.value
        )
        
    except Exception as e:
        logger.error(f"Error fetching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/news", response_model=NewsResponse, tags=["Data Fetching"])
async def fetch_news(request: NewsRequest):
    """
    Fetch and summarize news articles
    
    This endpoint simulates fetching news from various sources.
    In production, this would:
    - Query Google News / Bing News APIs
    - Parse and extract article data
    - Use Bedrock for summarization and tagging
    - Store results in S3 and DynamoDB
    """
    try:
        logger.info(f"Fetching news for {request.org_name}")
        
        # Simulate processing delay
        simulate_processing_delay(1.0, 2.5)
        
        # Generate synthetic data
        news = generate_news(request.org_name, count=12)
        
        return NewsResponse(
            news=[NewsArticle(**article) for article in news],
            count=len(news),
            org_name=request.org_name
        )
        
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trigger", response_model=TriggerResponse, tags=["Workflow"])
async def trigger_workflow(request: TriggerRequest, background_tasks: BackgroundTasks):
    """
    Trigger complete workflow
    
    Creates a run_id, stores run metadata, and triggers async processing
    of all three modules (bios, jobs, news).
    
    In production, this would:
    - Write run record to DynamoDB
    - Emit EventBridge events for each module
    - Lambda workers process each module independently
    """
    try:
        # Generate run ID
        run_id = str(uuid.uuid4())
        
        logger.info(f"Triggering workflow {run_id} for {request.org_name}")
        
        # Initialize workflow run metadata
        workflow_runs[run_id] = {
            "run_id": run_id,
            "status": WorkflowStatus.PENDING,
            "org_name": request.org_name,
            "role_title": request.role_title,
            "search_type": request.search_type.value,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "bios_count": 0,
            "jobs_count": 0,
            "news_count": 0,
            "modules": {
                "bios": {
                    "status": ModuleStatus.PENDING,
                    "count": 0,
                    "started_at": None,
                    "completed_at": None
                },
                "jobs": {
                    "status": ModuleStatus.PENDING,
                    "count": 0,
                    "started_at": None,
                    "completed_at": None
                },
                "news": {
                    "status": ModuleStatus.PENDING,
                    "count": 0,
                    "started_at": None,
                    "completed_at": None
                }
            }
        }
        
        # Initialize workflow data storage
        workflow_data[run_id] = {
            "bios": [],
            "jobs": [],
            "news": []
        }
        
        # Start async processing
        background_tasks.add_task(
            process_workflow_async,
            run_id,
            request.org_name,
            request.role_title,
            request.search_type.value
        )
        
        return TriggerResponse(
            run_id=run_id,
            status=WorkflowStatus.PENDING,
            message="Workflow started successfully",
            org_name=request.org_name,
            role_title=request.role_title,
            search_type=request.search_type.value
        )
        
    except Exception as e:
        logger.error(f"Error triggering workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{run_id}", response_model=StatusResponse, tags=["Workflow"])
async def get_workflow_status(run_id: str):
    """
    Get workflow status
    
    Returns the current status and progress of a workflow run.
    In production, this would query DynamoDB for run metadata.
    """
    try:
        if run_id not in workflow_runs:
            raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found")
        
        run_data = workflow_runs[run_id]
        
        # Convert module data to ModuleProgress objects
        modules = {}
        for module_name, module_data in run_data["modules"].items():
            modules[module_name] = ModuleProgress(**module_data)
        
        return StatusResponse(
            run_id=run_id,
            status=run_data["status"],
            bios_count=run_data["bios_count"],
            jobs_count=run_data["jobs_count"],
            news_count=run_data["news_count"],
            modules=modules,
            created_at=run_data["created_at"],
            updated_at=run_data["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows/{run_id}/data", tags=["Workflow"])
async def get_workflow_data(run_id: str):
    """
    Get all data generated by a workflow run
    
    Returns the complete dataset (bios, jobs, news) for a specific workflow run.
    """
    try:
        if run_id not in workflow_runs:
            raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found")
        
        run_data = workflow_runs[run_id]
        
        if run_data["status"] != WorkflowStatus.COMPLETED:
            return {
                "run_id": run_id,
                "status": run_data["status"],
                "message": "Workflow not yet completed. Data will be available once processing is complete.",
                "data": {
                    "bios": [],
                    "jobs": [],
                    "news": []
                }
            }
        
        # Get the generated data from workflow_data storage
        data = workflow_data.get(run_id, {})
        
        return {
            "run_id": run_id,
            "status": run_data["status"],
            "message": "Workflow data retrieved successfully",
            "data": {
                "bios": data.get("bios", []),
                "jobs": data.get("jobs", []),
                "news": data.get("news", [])
            },
            "counts": {
                "bios": len(data.get("bios", [])),
                "jobs": len(data.get("jobs", [])),
                "news": len(data.get("news", []))
            }
        }
    
    except Exception as e:
        logger.error(f"Error retrieving workflow data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/exports/{run_id}", response_model=ExportsResponse, tags=["Export"])
async def get_export_urls(run_id: str):
    """
    Get export file URLs
    
    Returns presigned S3 URLs for downloading export files.
    In production, this would:
    - Check if workflow is completed
    - Generate CSV/DOCX/PDF files
    - Upload to S3/exports/
    - Return presigned URLs
    """
    try:
        if run_id not in workflow_runs:
            raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found")
        
        run_data = workflow_runs[run_id]
        
        if run_data["status"] != WorkflowStatus.COMPLETED:
            return ExportsResponse(
                run_id=run_id,
                urls=ExportUrls(),
                status="pending",
                message="Workflow not yet completed. Export files will be available once processing is complete."
            )
        
        # In POC, generate mock presigned URLs
        # In production, these would be actual S3 presigned URLs
        base_url = "https://research-intelligence-data.s3.amazonaws.com/exports"
        
        return ExportsResponse(
            run_id=run_id,
            urls=ExportUrls(
                csv=f"{base_url}/{run_id}/data.csv?signature=mock_signature",
                # DOCX and PDF not implemented in POC
                # docx=f"{base_url}/{run_id}/data.docx?signature=mock_signature",
                # pdf=f"{base_url}/{run_id}/data.pdf?signature=mock_signature"
            ),
            status="ready",
            message="Export files are ready for download"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting export URLs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows", tags=["Workflow"])
async def list_workflows():
    """
    List all workflow runs
    Useful for debugging and monitoring
    """
    return {
        "count": len(workflow_runs),
        "workflows": [
            {
                "run_id": run_id,
                "status": run_data["status"],
                "org_name": run_data["org_name"],
                "created_at": run_data["created_at"].isoformat(),
                "updated_at": run_data["updated_at"].isoformat()
            }
            for run_id, run_data in workflow_runs.items()
        ]
    }


@app.delete("/workflows/{run_id}", tags=["Workflow"])
async def delete_workflow(run_id: str):
    """
    Delete a workflow run
    Useful for cleanup during development
    """
    if run_id not in workflow_runs:
        raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found")
    
    del workflow_runs[run_id]
    if run_id in workflow_data:
        del workflow_data[run_id]
    
    return {"message": f"Workflow {run_id} deleted successfully"}


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=str(exc)
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).model_dump()
    )


# Run application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
