# Deploy Your App to Cloud (Free)

## Quick Deploy Guide

### Step 1: Deploy Backend to Render (Free)

1. **Go to** https://render.com
2. **Sign up** (free account)
3. Click **"New +"** → **"Web Service"**
4. **Connect your GitHub** (or upload files)
5. **Settings:**
   - Name: `vibe-coding-backend`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Python Version: `3.9.19`
6. **Environment Variables:**
   - `ZHIPU_API_KEY`: Your ZhipuAI API key
   - `PEXELS_API_KEY`: Your Pexels API key
   - `REPLICATE_API_TOKEN`: Your Replicate API token
7. Click **"Deploy Web Service"**
8. **Copy your backend URL** (e.g., `https://vibe-coding-backend.onrender.com`)

### Step 2: Deploy Frontend to Vercel (Free)

1. **Go to** https://vercel.com
2. **Sign up** (free account)
3. Click **"Add New..."** → **"Project"**
4. **Connect your GitHub** (or upload files)
5. **Select your frontend folder**
6. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL`: `https://vibe-coding-backend.onrender.com` (replace with your actual backend URL from Step 1)
7. Click **"Deploy"**
8. **Your app is now online!**

## After Deployment

Your app will be accessible at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.onrender.com`

## Benefits

✅ **Always online** - even when your PC is off
✅ **Free hosting** - no payment required
✅ **Fast** - global CDN
✅ **Secure** - HTTPS included

## Troubleshooting

If the app doesn't work:
1. Check Render logs for backend errors
2. Verify environment variables are correct
3. Ensure CORS is configured properly
4. Check Vercel logs for frontend errors

## Mobile Access

Just open your Vercel URL on your phone:
```
https://your-app.vercel.app
```

No more "site can't be reached" errors! 🎉
