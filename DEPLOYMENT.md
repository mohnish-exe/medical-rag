# 🚀 Deployment Guide - Medical RAG API

## Deployment Options

### Option 1: Render.com (Recommended - Free Tier)

**Advantages:**

- ✅ Free tier available
- ✅ Automatic SSL/HTTPS
- ✅ Easy environment variable management
- ✅ GitHub integration
- ✅ Auto-deploy on push

**Steps:**

1. **Push to GitHub**

   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**

   - Go to https://render.com
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `medical-rag-api`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
     - Start Command: `uvicorn rag_api:app --host 0.0.0.0 --port $PORT`
     - Instance Type: `Free`

3. **Add Environment Variables**
   In Render dashboard, add:

   ```
   SUPABASE_URL=https://rejkqxpktiynlspoyppi.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   COHERE_API_KEY=AA3kluBGWmXPaR0pz6dqQFag4oAQRExeZnTMjgqG
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your URL: `https://medical-rag-api.onrender.com`

---

### Option 2: Railway.app (Easy, Free Trial)

**Steps:**

1. **Deploy on Railway**

   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python

2. **Add Environment Variables**

   ```
   SUPABASE_URL=https://rejkqxpktiynlspoyppi.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   COHERE_API_KEY=AA3kluBGWmXPaR0pz6dqQFag4oAQRExeZnTMjgqG
   PORT=8000
   ```

3. **Configure Start Command**

   - Settings → Deploy → Start Command:

   ```
   uvicorn rag_api:app --host 0.0.0.0 --port $PORT
   ```

4. **Generate Domain**
   - Settings → Networking → Generate Domain
   - Your URL: `https://your-app-name.up.railway.app`

---

### Option 3: Fly.io (More Control)

**Steps:**

1. **Install Fly CLI**

   ```powershell
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login and Launch**

   ```bash
   fly auth login
   fly launch
   ```

3. **Set Environment Variables**

   ```bash
   fly secrets set SUPABASE_URL="https://rejkqxpktiynlspoyppi.supabase.co"
   fly secrets set SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   fly secrets set COHERE_API_KEY="AA3kluBGWmXPaR0pz6dqQFag4oAQRExeZnTMjgqG"
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```
   - Your URL: `https://your-app-name.fly.dev`

---

### Option 4: Vercel (Serverless)

**Note:** Vercel works best with serverless functions. Your current setup might need modification.

**Steps:**

1. **Install Vercel CLI**

   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`**

   ```json
   {
     "builds": [
       {
         "src": "rag_api.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "rag_api.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel
   ```

---

## 🎯 Recommended: Render.com

**Why Render?**

- Free tier sufficient for testing
- Automatic HTTPS
- No credit card required for free tier
- Easy environment variable management
- 750 hours/month free

**Quick Render Deployment:**

1. Push code to GitHub
2. Connect Render to GitHub
3. Add environment variables
4. Deploy!

**Estimated time: 10 minutes**

---

## 📝 After Deployment

Test your deployed API:

```bash
curl -X POST https://your-deployed-url.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What is diabetes?", "top_k":3}'
```

## 🔧 Troubleshooting

**Issue: Spacy model not found**

- Solution: Add to build command: `python -m spacy download en_core_web_sm`

**Issue: Port binding error**

- Solution: Make sure start command uses `--port $PORT` (not hardcoded 8000)

**Issue: Environment variables not loading**

- Solution: Verify all 3 environment variables are set in platform dashboard
