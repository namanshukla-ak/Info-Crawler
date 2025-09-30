# Research Intelligence Platform - Backend

FastAPI backend for the Research Intelligence Platform POC with synthetic data generation.

## Features

- **RESTful API** with FastAPI framework
- **Synthetic Data Generation** using Faker for POC testing
- **Async Workflow Processing** simulating EventBridge/Lambda architecture
- **Pydantic Models** for request/response validation
- **In-memory Storage** (simulating DynamoDB for POC)
- **Health Checks** and monitoring endpoints
- **Interactive API Docs** with Swagger UI

## API Endpoints

### Data Fetching
- `POST /bios` - Fetch people bios from organization
- `POST /jobs` - Query job boards for postings
- `POST /news` - Fetch and summarize news articles

### Workflow Management
- `POST /trigger` - Start complete workflow (all modules)
- `GET /status/{run_id}` - Get workflow status and progress
- `GET /workflows` - List all workflow runs
- `DELETE /workflows/{run_id}` - Delete a workflow run

### Export
- `GET /exports/{run_id}` - Get presigned URLs for export files

### System
- `GET /health` - Health check endpoint
- `GET /` - API information

## Installation

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
cp ../.env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
# Development mode with auto-reload
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t research-intelligence-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 \
  -e DEBUG=true \
  research-intelligence-backend
```

### AWS ECS Deployment

1. Push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag research-intelligence-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-intelligence-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-intelligence-backend:latest
```

2. Create ECS Task Definition and Service using the provided image

## Configuration

Configuration is managed through environment variables and `config.py`. Key settings:

- `DEBUG`: Enable debug mode (default: False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `SYNTHETIC_DATA_ENABLED`: Use synthetic data (default: True)
- `DEFAULT_BIOS_COUNT`: Number of bios to generate (default: 8)
- `DEFAULT_JOBS_COUNT`: Number of jobs to generate (default: 15)
- `DEFAULT_NEWS_COUNT`: Number of news articles to generate (default: 12)

## Usage Examples

### Fetch Bios
```bash
curl -X POST http://localhost:8000/bios \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Harvard University",
    "role_title": "Chief Financial Officer"
  }'
```

### Fetch Jobs
```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "role_title": "Chief Financial Officer",
    "search_type": "Executive"
  }'
```

### Trigger Workflow
```bash
curl -X POST http://localhost:8000/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Harvard University",
    "role_title": "Chief Financial Officer",
    "search_type": "Executive"
  }'
```

### Check Status
```bash
curl http://localhost:8000/status/{run_id}
```

## Project Structure

```
backend/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic models for validation
├── data_generator.py    # Synthetic data generation
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container definition
└── README.md           # This file
```

## Synthetic Data

For POC purposes, the backend generates realistic synthetic data using the Faker library:

### People Bios
- Names, titles, organizations
- Short and long biographies
- Education background
- Previous positions
- Tenure information
- Profile photos (via pravatar.cc)

### Job Postings
- Job titles and organizations
- Locations and salary ranges
- Job descriptions
- Application deadlines
- Multiple job board sources

### News Articles
- Titles and summaries
- Publication dates and sources
- Categories (Leadership Change, Financial, etc.)
- Tags for classification
- Read time estimates

## Production Considerations

For production deployment, replace synthetic data with actual services:

1. **Web Scraping**: Implement crawl4ai/Playwright scraping
2. **AWS Services**: 
   - DynamoDB for data storage
   - S3 for file storage
   - OpenSearch for search/deduplication
   - Bedrock for LLM processing
   - EventBridge/Lambda for async processing
3. **Security**:
   - Secrets Manager for API keys
   - IAM roles and policies
   - HTTPS/TLS encryption
4. **Monitoring**:
   - CloudWatch Logs
   - Application metrics
   - Error tracking

## Development

### Adding New Endpoints

1. Define request/response models in `models.py`
2. Add endpoint function in `main.py`
3. Update data generator if needed
4. Test with interactive docs at `/docs`

### Testing

Test the API locally:

```bash
# Start the backend
cd backend
python main.py

# In another terminal, test endpoints
curl http://localhost:8000/health
```

Or use the interactive docs at `http://localhost:8000/docs`

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change port: `uvicorn main:app --port 8001`
   - Or kill process using port 8000

2. **Import errors**
   - Ensure all dependencies installed: `pip install -r requirements.txt`
   - Check Python version (3.11+ recommended)

3. **CORS errors**
   - Update `ALLOWED_ORIGINS` in config
   - Check frontend API_BASE_URL

## License

Internal POC - Confidential
