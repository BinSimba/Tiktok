# Deployment Guide - Text to TikTok App

## Overview
This guide will help you deploy your AI video generation app to cloud services so you can access it from your phone anywhere.

## Architecture
- **Frontend**: Next.js app deployed to Vercel
- **Backend**: FastAPI app deployed to Render
- **Existing Site**: https://text-to-tiktok-pi.vercel.app/

## Step 1: Deploy Backend to Render

### Option A: Via Render Dashboard (Recommended)
1. Go to https://dashboard.render.com/
2. Sign in or create an account
3. Click "New +"
4. Select "Web Service"
5. Connect your GitHub repository or upload the backend folder
6. Configure:
   - **Name**: text-to-tiktok-backend
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add Environment Variables:
   - `PERPLEXITY_API_KEY`: (add your Perplexity API key here)
   - `ZHIPU_API_KEY`: (leave empty or add your key)
   - `REPLICATE_API_TOKEN`: (leave empty or add your key)
   - `PEXELS_API_KEY`: (leave empty or add your key)
8. Click "Deploy Web Service"
9. Wait for deployment (may take 5-10 minutes)
10. Copy your backend URL (e.g., https://text-to-tiktok-backend.onrender.com)

### Option B: Via Render CLI
```bash
npm install -g render-cli
cd "/Volumes/DOCK/IA/Glm Vibe coding /backend"
render deploy
```

## Step 2: Deploy Frontend to Vercel

### Option A: Via Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Sign in or create an account
3. Click "Add New Project"
4. Connect your GitHub repository or upload the frontend folder
5. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `/frontend`
6. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: `https://text-to-tiktok-backend.onrender.com`
7. Click "Deploy"
8. Wait for deployment
9. Your app will be live at: https://text-to-tiktok-pi.vercel.app/

### Option B: Via Vercel CLI
```bash
npm install -g vercel
cd "/Volumes/DOCK/IA/Glm Vibe coding /frontend"
vercel --prod
```

## Step 3: Update CORS Configuration

The backend already has CORS configured to allow requests from your Vercel site. If you need to add more origins, update `/backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://192.168.1.169:3000",
        "https://text-to-tiktok-pi.vercel.app",
        # Add your Vercel URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 4: Test the Deployed App

1. Open your phone's browser
2. Navigate to: https://text-to-tiktok-pi.vercel.app/
3. Try generating a video
4. If you encounter CORS issues, check the Render logs and update the CORS configuration

## Important Notes

- **Backend Cold Start**: Render services go to sleep when inactive. The first request may take 30-60 seconds.
- **Free Tier Limitations**: Render free tier has limits on CPU and RAM usage.
- **File Storage**: Render uses ephemeral storage. Generated videos are not persisted.
- **API Keys**: Never commit API keys to git. Use environment variables.

## Troubleshooting

### Video Generation Fails
- Check Render logs: https://dashboard.render.com/web/services/your-service/logs
- Verify environment variables are set correctly
- Check CORS settings in backend

### CORS Errors
- Verify the Vercel URL is in the CORS allow_origins list
- Check the browser console for specific CORS errors
- Ensure both frontend and backend are using HTTPS

### Backend Not Responding
- Check if the service is awake (cold start issue)
- Verify the backend URL is correct
- Check Render dashboard for service status

## URLs After Deployment

- **Frontend**: https://text-to-tiktok-pi.vercel.app/
- **Backend**: https://text-to-tiktok-backend.onrender.com
- **API Docs**: https://text-to-tiktok-backend.onrender.com/docs
