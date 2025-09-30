# Deployment Guide for Research Intelligence Platform

## ❌ Why Vercel Won't Work

Vercel is designed for:
- Static sites
- Serverless functions (short-lived, < 10 seconds)
- Next.js applications

Streamlit requires:
- Persistent WebSocket connections
- Long-running server process
- Real-time bidirectional communication

**Verdict:** Vercel cannot run Streamlit apps.

---

## ✅ Recommended Deployment Options

### Option 1: Streamlit Community Cloud (EASIEST & FREE)

**Best for:** Frontend only (Streamlit)

**Steps:**
1. Push code to GitHub ✅ (already done)
2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. Click "New app"
5. Configure:
   - Repository: Your GitHub repo
   - Branch: main
   - Main file path: `frontend/main.py`
6. Add environment variables:
   ```
   API_BASE_URL=<your-backend-url>
   ```
7. Click "Deploy"

**Pros:**
- Free forever
- Automatic HTTPS
- Auto-deploys on git push
- Made for Streamlit

**Cons:**
- Frontend only (need separate backend)
- Limited resources on free tier

---

### Option 2: Render.com (FREE TIER)

**Best for:** Both Frontend & Backend

**Backend Deployment:**
1. Go to https://render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   ```
   Name: research-backend
   Environment: Python
   Region: Choose closest
   Branch: main
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Add Environment Variables:
   ```
   SYNTHETIC_DATA_ENABLED=true
   DEBUG=false
   ```
6. Click "Create Web Service"

**Frontend Deployment:**
1. Click "New +" → "Web Service"
2. Connect same GitHub repo
3. Configure:
   ```
   Name: research-frontend
   Environment: Python
   Region: Choose closest
   Branch: main
   Root Directory: frontend
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
   ```
4. Add Environment Variables:
   ```
   API_BASE_URL=https://research-backend.onrender.com
   ```
5. Click "Create Web Service"

**Pros:**
- Free tier available
- Can host both frontend & backend
- Automatic HTTPS
- Auto-deploys on git push
- Docker support

**Cons:**
- Free tier spins down after inactivity (cold starts)

---

### Option 3: Railway.app (GENEROUS FREE TIER)

**Steps:**
1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository

**Backend Service:**
```
Root Directory: backend
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Environment Variables:
  SYNTHETIC_DATA_ENABLED=true
```

**Frontend Service:**
```
Root Directory: frontend  
Start Command: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
Environment Variables:
  API_BASE_URL=https://your-backend-url.railway.app
```

**Pros:**
- Very fast deployments
- Great free tier ($5 credit/month)
- No cold starts
- Simple interface

---

### Option 4: Heroku (Paid but Reliable)

**Backend:**
Create `backend/Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Frontend:**
Create `frontend/Procfile`:
```
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

Deploy:
```bash
heroku create research-backend
heroku create research-frontend
git subtree push --prefix backend heroku-backend main
git subtree push --prefix frontend heroku-frontend main
```

---

### Option 5: AWS ECS Fargate (Production Ready)

Use the Docker files already created:

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Backend
cd backend
docker build -t research-backend .
docker tag research-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-backend:latest

# Frontend
cd ../frontend
docker build -t research-frontend .
docker tag research-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/research-frontend:latest
```

Then create ECS services with these images.

---

## 🎯 My Recommendation

For POC/Testing:
1. **Backend** → Render.com (free)
2. **Frontend** → Streamlit Community Cloud (free)

For Production:
1. **Both** → AWS ECS Fargate (from Project.md SOW)

---

## 🚀 Quick Start: Render.com Deployment

1. Sign up at https://render.com/
2. Connect GitHub
3. Create two web services (backend & frontend)
4. Use the configurations above
5. Done! ✅

**Your URLs will be:**
- Backend: `https://research-backend.onrender.com`
- Frontend: `https://research-frontend.onrender.com`

---

## 📝 Environment Variables Reference

### Frontend (.env)
```bash
API_BASE_URL=https://your-backend-url.com
API_TIMEOUT=30
ENABLE_AUTO_REFRESH=true
```

### Backend (.env)
```bash
SYNTHETIC_DATA_ENABLED=true
DEBUG=false
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

---

## 🔧 Troubleshooting

### Frontend can't connect to backend
- Check `API_BASE_URL` environment variable
- Ensure backend is running
- Check CORS settings in backend

### Cold starts on free tier
- Upgrade to paid tier
- Use a ping service to keep alive
- Accept the cold start delay

### Out of memory
- Reduce data generation counts
- Upgrade to larger instance
- Implement pagination

---

## 📊 Comparison

| Platform | Free Tier | Cold Starts | Best For |
|----------|-----------|-------------|----------|
| Streamlit Cloud | ✅ Yes | ❌ No | Frontend only |
| Render.com | ✅ Yes | ⚠️ Yes | Full stack POC |
| Railway | ✅ $5/mo | ❌ No | Full stack |
| Heroku | ❌ Paid | ❌ No | Reliable apps |
| AWS ECS | ❌ Paid | ❌ No | Production |

---

## 🎉 Next Steps

1. Choose a platform from above
2. Deploy backend first
3. Get backend URL
4. Deploy frontend with backend URL
5. Test the deployment
6. Share the link!

Need help with deployment? Let me know which platform you choose!
