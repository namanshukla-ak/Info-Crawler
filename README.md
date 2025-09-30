# Research Intelligence Platform

A comprehensive POC for automated intelligence gathering and analysis system with web scraping, LLM processing, and data export capabilities.

## 🎯 Overview

This platform automates the collection and analysis of:
- **People Bios**: Leadership information from organization websites
- **Job Postings**: Competing searches from multiple job boards
- **News Articles**: Recent news with AI-powered summarization and tagging

## 🏗️ Architecture

### Frontend
- **Framework**: Streamlit
- **Features**: Interactive UI, data tables, CSV export
- **Deployment**: Docker container on ECS Fargate

### Backend
- **Framework**: FastAPI
- **Features**: RESTful API, async processing, synthetic data generation
- **Deployment**: Docker container on ECS Fargate

### Data Layer (Production)
- **S3**: Raw data, curated results, exports
- **DynamoDB**: Workflow metadata, structured data
- **OpenSearch**: Search, filtering, deduplication
- **Bedrock**: LLM processing (entity extraction, summarization, tagging)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose (optional)
- Git

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
cd /path/to/project

# Start both frontend and backend
docker-compose up --build

# Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

## 📚 Usage

### Web Interface

1. **Open Frontend**: Navigate to `http://localhost:8501`
2. **Enter Details**:
   - Organization Name (e.g., "Harvard University")
   - Role Title (e.g., "Chief Financial Officer")
   - Search Type (Executive, Academic, etc.)
3. **Fetch Data**:
   - Individual modules: Click "Fetch Bios", "Fetch Jobs", or "Fetch News"
   - Complete workflow: Click "Trigger Complete Workflow"
4. **Review Data**: View, edit, and filter results in interactive tables
5. **Export**: Download data as CSV files

### API Examples

#### Fetch Bios
```bash
curl -X POST http://localhost:8000/bios \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Harvard University",
    "role_title": "Chief Financial Officer"
  }'
```

#### Trigger Workflow
```bash
curl -X POST http://localhost:8000/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Harvard University",
    "role_title": "Chief Financial Officer",
    "search_type": "Executive"
  }'
```

#### Check Status
```bash
curl http://localhost:8000/status/{run_id}
```

## 📁 Project Structure

```
.
├── frontend/
│   ├── main.py              # Streamlit application
│   ├── api_client.py        # Backend API client
│   ├── utils.py             # Utility functions
│   ├── config.py            # Configuration
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Container definition
│   └── .streamlit/
│       └── config.toml      # Streamlit config
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── data_generator.py   # Synthetic data generator
│   ├── config.py            # Configuration
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Container definition
│   └── README.md
├── scripts/
│   └── (deployment scripts)
├── docker-compose.yml       # Multi-container setup
├── .env.example             # Environment template
├── Project.md               # SOW documentation
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

#### Frontend
```env
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30
ENABLE_AUTO_REFRESH=true
```

#### Backend
```env
DEBUG=false
HOST=0.0.0.0
PORT=8000
SYNTHETIC_DATA_ENABLED=true
LOG_LEVEL=INFO
```

#### Production (AWS)
```env
AWS_REGION=us-east-1
S3_BUCKET_NAME=research-intelligence-data
DYNAMODB_RUNS_TABLE=research_runs
OPENSEARCH_ENDPOINT=your-endpoint
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

## 🧪 Testing

### Backend API
```bash
# Health check
curl http://localhost:8000/health

# Interactive API documentation
open http://localhost:8000/docs
```

### Frontend
```bash
# Access the UI
open http://localhost:8501
```

## 🎨 Features

### Current (POC)
- ✅ Synthetic data generation for testing
- ✅ RESTful API with FastAPI
- ✅ Interactive Streamlit UI
- ✅ Async workflow processing
- ✅ CSV export functionality
- ✅ Docker containerization
- ✅ Health checks and monitoring

### Production Roadmap
- ⏳ Web scraping with crawl4ai/Playwright
- ⏳ AWS service integration (S3, DynamoDB, OpenSearch)
- ⏳ Amazon Bedrock for LLM processing
- ⏳ EventBridge/Lambda async architecture
- ⏳ DOCX and PDF export formats
- ⏳ Advanced search and filtering
- ⏳ User authentication
- ⏳ Rate limiting and caching

## 🔒 Security Considerations

### POC
- Basic CORS configuration
- No authentication required
- In-memory data storage

### Production
- AWS IAM roles and policies
- Secrets Manager for API keys
- HTTPS/TLS encryption
- VPC and security groups
- CloudWatch logging
- Data encryption at rest and in transit

## 📊 Monitoring

### Health Checks
- Backend: `GET /health`
- Frontend: `GET /_stcore/health`

### Logs
```bash
# Docker Compose logs
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🐛 Troubleshooting

### Backend not starting
```bash
# Check logs
docker-compose logs backend

# Rebuild container
docker-compose up --build backend
```

### Frontend can't connect to backend
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check network
docker-compose exec frontend ping backend

# Verify environment variable
docker-compose exec frontend env | grep API_BASE_URL
```

### Port conflicts
```bash
# Change ports in docker-compose.yml
services:
  backend:
    ports:
      - "8001:8000"  # Change 8000 to 8001
  frontend:
    ports:
      - "8502:8501"  # Change 8501 to 8502
```

## 🚀 Deployment

### AWS ECS Fargate

1. **Build and push images to ECR**:
```bash
# Backend
cd backend
docker build -t research-backend .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag research-backend:latest <account>.dkr.ecr.us-east-1.amazonaws.com/research-backend:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/research-backend:latest

# Frontend
cd ../frontend
docker build -t research-frontend .
docker tag research-frontend:latest <account>.dkr.ecr.us-east-1.amazonaws.com/research-frontend:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/research-frontend:latest
```

2. **Create ECS Task Definitions** for backend and frontend

3. **Create ECS Services** on Fargate with load balancers

4. **Configure DNS** and SSL certificates

## 📝 API Documentation

Full API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/bios` | Fetch people bios |
| POST | `/jobs` | Fetch job postings |
| POST | `/news` | Fetch news articles |
| POST | `/trigger` | Start complete workflow |
| GET | `/status/{run_id}` | Get workflow status |
| GET | `/exports/{run_id}` | Get export file URLs |
| GET | `/workflows` | List all workflows |
| DELETE | `/workflows/{run_id}` | Delete workflow |

## 🤝 Contributing

This is an internal POC. For questions or issues:
1. Review documentation
2. Check logs for errors
3. Contact the development team

## 📄 License

Internal POC - Confidential

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Streamlit for rapid UI development
- Faker for synthetic data generation
- AWS for cloud infrastructure

---

**Version**: 1.0.0  
**Last Updated**: September 30, 2025  
**Status**: POC - Active Development
