# 🚀 Getting Started - 5 Minute Setup

## Prerequisites

✅ Python 3.11 or higher  
✅ pip (Python package installer)  
⚠️ Docker & Docker Compose (optional, but recommended)

## Quick Start

### Method 1: Docker Compose (Recommended) 🐳

```bash
# 1. Navigate to project directory
cd "/home/naman/Downloads/AK Projects/Issacson"

# 2. Start everything
docker-compose up --build

# 3. Wait for services to start (~30 seconds)

# 4. Open your browser
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000/docs
```

That's it! 🎉

---

### Method 2: Local Python (Alternative) 🐍

#### Terminal 1 - Start Backend
```bash
cd "/home/naman/Downloads/AK Projects/Issacson/backend"

# Install dependencies
pip install -r requirements.txt

# Start backend
python main.py
```

#### Terminal 2 - Start Frontend
```bash
cd "/home/naman/Downloads/AK Projects/Issacson/frontend"

# Install dependencies
pip install -r requirements.txt

# Start frontend
streamlit run main.py
```

#### Access the Application
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000/docs

---

## First Test Run

1. **Open Frontend**: http://localhost:8501

2. **Enter Information** (sidebar):
   - Organization: `Harvard University`
   - Role Title: `Chief Financial Officer`
   - Search Type: `Executive`

3. **Try Individual Fetches**:
   - Click "📋 Fetch Bios" → See 8 people bios
   - Click "💼 Fetch Jobs" → See 15 job postings
   - Click "📰 Fetch News" → See 12 news articles

4. **Try Complete Workflow**:
   - Click "🚀 Trigger Complete Workflow"
   - Watch real-time progress
   - See all modules complete
   - Download CSV files

## Verify Everything Works

### Test Backend
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### Test Frontend
Open browser to http://localhost:8501 - you should see the Research Intelligence Platform

### Run Full API Test
```bash
cd "/home/naman/Downloads/AK Projects/Issacson"
./scripts/test_api.sh
```

## Common Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild containers
docker-compose up --build

# Stop and remove everything
docker-compose down -v
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

### Docker Issues
```bash
# Clean everything
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

### Python Issues
```bash
# Reinstall backend dependencies
cd backend
pip install -r requirements.txt --force-reinstall

# Reinstall frontend dependencies
cd frontend
pip install -r requirements.txt --force-reinstall
```

## What to Try Next

### 1. Explore the Frontend
- Edit data inline in tables
- Try different organizations and roles
- Export data as CSV
- Monitor workflow progress

### 2. Explore the API
- Visit http://localhost:8000/docs
- Try the interactive Swagger UI
- Test different endpoints
- View response schemas

### 3. Check the Code
- `backend/main.py` - See how API works
- `backend/data_generator.py` - See synthetic data
- `frontend/main.py` - See UI implementation
- `backend/models.py` - See data models

### 4. Modify and Experiment
- Change data generation counts in `backend/config.py`
- Modify UI styling in `frontend/main.py`
- Add new fields to data models
- Create new API endpoints

## Project Structure Quick Reference

```
.
├── frontend/           → Streamlit UI
│   ├── main.py         → Start here for UI
│   └── api_client.py   → API communication
│
├── backend/            → FastAPI API
│   ├── main.py         → Start here for API
│   ├── data_generator.py → Synthetic data
│   └── models.py       → Data schemas
│
├── docker-compose.yml  → Run everything
├── README.md           → Full documentation
├── QUICKSTART.md       → Detailed guide
└── TECHNICAL_SUMMARY.md → Technical details
```

## Getting Help

1. **Check Logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **Read Documentation**:
   - `README.md` - Complete guide
   - `QUICKSTART.md` - Step by step
   - `TECHNICAL_SUMMARY.md` - Architecture
   - http://localhost:8000/docs - API docs

3. **Test API Directly**:
   ```bash
   ./scripts/test_api.sh
   ```

## Success Checklist

- [ ] Services start without errors
- [ ] Frontend loads at http://localhost:8501
- [ ] Backend API responds at http://localhost:8000/health
- [ ] Can fetch bios successfully
- [ ] Can fetch jobs successfully
- [ ] Can fetch news successfully
- [ ] Can trigger complete workflow
- [ ] Can see real-time status updates
- [ ] Can download CSV exports

## Next Steps

Once everything works:

1. **Read the full documentation**: `README.md`
2. **Explore the API**: http://localhost:8000/docs
3. **Try different inputs**: Various organizations and roles
4. **Review the code**: Understand the implementation
5. **Plan production**: Review `Project.md` for full SOW

---

**🎉 You're Ready to Go!**

Questions? Check the documentation or API docs.

Happy Testing! 🚀
