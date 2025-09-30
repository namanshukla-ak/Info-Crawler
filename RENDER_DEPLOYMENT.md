# Quick Render.com Deployment Guide

## Step 1: Deploy Backend

1. Go to https://render.com/ and sign in with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `research-backend`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Add Environment Variables (click "Advanced"):
   ```
   SYNTHETIC_DATA_ENABLED = true
   DEBUG = false
   LOG_LEVEL = INFO
   ```

6. Click "Create Web Service"
7. Wait for deployment (3-5 minutes)
8. **Copy your backend URL** (e.g., `https://research-backend.onrender.com`)

---

## Step 2: Deploy Frontend

1. Click "New +" → "Web Service" again
2. Connect same GitHub repository
3. Configure:
   - **Name:** `research-frontend`
   - **Region:** Same as backend
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false`

4. Add Environment Variables:
   ```
   API_BASE_URL = https://research-backend.onrender.com
   ```
   (Use the URL from Step 1)

5. Click "Create Web Service"
6. Wait for deployment (3-5 minutes)
7. **Your app is live!** 🎉

---

## URLs

- **Frontend:** `https://research-frontend.onrender.com`
- **Backend API:** `https://research-backend.onrender.com`
- **API Docs:** `https://research-backend.onrender.com/docs`

---

## ⚠️ Important Notes

### Free Tier Limitations:
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds (cold start)
- 750 hours/month free

### To Keep Services Alive:
Use a service like:
- https://uptimerobot.com/ (free)
- https://cron-job.org/ (free)

Ping your URLs every 10 minutes.

---

## Testing After Deployment

1. Visit your frontend URL
2. Try a Quick Preset (e.g., "University CFO Search")
3. Click "Trigger Complete Workflow"
4. Watch the auto-refresh work!

---

## Troubleshooting

### "Application Error" on Frontend
- Check logs in Render dashboard
- Verify `API_BASE_URL` is correct
- Make sure backend is running first

### "502 Bad Gateway"
- Service is still starting (wait 1-2 minutes)
- Or cold start (wait 30 seconds)

### Frontend can't connect to Backend
- Verify `API_BASE_URL` environment variable
- Check backend is accessible at `/health`
- Ensure CORS is enabled in backend

---

## Next Steps

1. Deploy both services
2. Test functionality
3. Share the frontend URL
4. Monitor logs for any issues

Need help? Check the Render logs or let me know!
