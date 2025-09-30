# Research Intelligence Platform - Frontend

Streamlit-based frontend for the Research Intelligence Platform POC.

## Features

- **Input Configuration**: Set organization name, role title, and search type
- **Data Fetching**: Individual modules for bios, jobs, and news
- **Complete Workflow**: Trigger all modules simultaneously with status tracking
- **Data Review**: Interactive tables with inline editing capabilities
- **Export**: Download data as CSV files
- **Real-time Status**: Monitor workflow progress with live updates

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

3. Set up environment variables:
```bash
cp ../.env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t research-intelligence-frontend .
```

2. Run the container:
```bash
docker run -p 8501:8501 \
  -e API_BASE_URL=http://backend:8000 \
  research-intelligence-frontend
```

### AWS ECS Deployment

1. Push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag research-intelligence-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-intelligence-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-intelligence-frontend:latest
```

2. Create ECS Task Definition and Service using the provided image

## Configuration

Configuration is managed through environment variables. Copy `.env.example` to `.env` and update values:

- `API_BASE_URL`: Backend API endpoint (default: http://localhost:8000)
- `API_TIMEOUT`: Request timeout in seconds (default: 30)
- `ENABLE_AUTO_REFRESH`: Enable auto-refresh for workflow status (default: true)
- `AUTO_REFRESH_INTERVAL`: Refresh interval in seconds (default: 5)

## Usage

### Fetching Individual Data

1. Enter organization name and role title in the sidebar
2. Click "Fetch Bios", "Fetch Jobs", or "Fetch News" buttons
3. Review data in the respective tabs
4. Edit data inline if needed
5. Download as CSV

### Running Complete Workflow

1. Configure inputs in the sidebar
2. Click "Trigger Complete Workflow"
3. Monitor progress in the status dashboard
4. Wait for completion
5. Download export files

## Project Structure

```
frontend/
├── main.py                 # Main Streamlit application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── .streamlit/
│   └── config.toml      # Streamlit configuration
└── README.md            # This file
```

## API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

- `POST /bios` - Fetch people bios
- `POST /jobs` - Fetch job postings
- `POST /news` - Fetch news articles
- `POST /trigger` - Start complete workflow
- `GET /status/{run_id}` - Get workflow status
- `GET /exports/{run_id}` - Get export file URLs

## Development

### Adding New Features

1. Update `main.py` with new UI components
2. Add API integration in helper functions
3. Update session state management if needed
4. Add corresponding backend endpoints

### Styling

Custom CSS is included in `main.py`. Modify the `st.markdown()` section to update styles.

### Testing

Test the frontend locally before deploying:

```bash
# Start backend API (in another terminal)
cd ../backend
uvicorn main:app --reload

# Start frontend
cd ../frontend
streamlit run main.py
```

## Troubleshooting

### Common Issues

1. **Cannot connect to backend**
   - Check `API_BASE_URL` in environment variables
   - Ensure backend is running
   - Check network connectivity

2. **Data not loading**
   - Verify backend API is responding
   - Check browser console for errors
   - Review Streamlit logs

3. **Export not working**
   - Ensure workflow has completed
   - Check S3 permissions
   - Verify presigned URL generation

## License

Internal POC - Confidential
