# 🚀 Complete Setup & Deployment Guide

## ✅ Current Status

Your NorthStar AI is now **fully integrated**:
- ✅ Backend with AI analysis engine (Gemini)
- ✅ Frontend React app with chat interface
- ✅ All API endpoints connected
- ✅ Chat interface for natural language queries

---

## 📋 Prerequisites Check

```bash
# Check MongoDB
docker ps | grep mongodb

# Check Backend
curl http://localhost:8001/api/health

# Both should be running!
```

---

## 🎯 Part 1: Run Locally (Both Frontend + Backend)

### Terminal 1: Backend (Already Running ✅)
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
python3 -m uvicorn server:app --reload --port 8001
```

### Terminal 2: Frontend (Let's start this!)
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm start
```

Frontend will open at: **http://localhost:3000**

---

## 🧪 Part 2: Test the Full Application

Once both are running:

1. **Open Browser**: http://localhost:3000
2. **Upload Data**:
   - Click "Select File" under Mixpanel CSV
   - Choose `/Users/Anirudh.Kanojia/NorthStar-AI/sample_data/mixpanel_sample.csv`
   - Click Upload
   - Repeat for Jira and MoEngage files

3. **View Anomalies**: You'll see metric cards with detected changes

4. **Click "Generate Insights"**: Wait 30 seconds for AI analysis

5. **Go to "Insights" tab**: See comprehensive AI-generated insights

6. **Go to "Chat" tab**: Ask questions like:
   - "Why did activation rate drop?"
   - "Which campaign performed best?"
   - "What caused the biggest metric change?"

---

## 🌐 Part 3: Deploy to Render (Free Hosting)

### Why Render?
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Supports both frontend and backend
- ✅ Custom domains
- ✅ Auto-deploy from Git

### Step 1: Prepare for Deployment

Create a Procfile for backend:
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
cat > Procfile << 'EOF'
web: uvicorn server:app --host 0.0.0.0 --port $PORT
EOF
```

Create runtime.txt:
```bash
cat > runtime.txt << 'EOF'
python-3.9.18
EOF
```

Update requirements.txt (simplified):
```bash
cat > requirements.txt << 'EOF'
fastapi==0.119.0
uvicorn==0.38.0
motor==3.7.1
pandas==2.3.3
numpy==2.0.2
python-dotenv==1.1.1
google-generativeai==0.8.5
python-multipart==0.0.20
EOF
```

### Step 2: Push to GitHub

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI

# Initialize git (if not already)
git init
git add .
git commit -m "Complete NorthStar AI with backend and frontend"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/northstar-ai.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy Backend on Render

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Fill in:
   - **Name**: northstar-ai-backend
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `MONGO_URL`: (get free MongoDB from MongoDB Atlas)
   - `DB_NAME`: growth_copilot_db
   - `GOOGLE_API_KEY`: your-gemini-key
   - `CORS_ORIGINS`: *
6. Click "Create Web Service"

### Step 4: Deploy Frontend on Render

1. Click "New +" → "Static Site"
2. Connect same GitHub repo
3. Fill in:
   - **Name**: northstar-ai-frontend
   - **Root Directory**: frontend
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: build
4. Add Environment Variable:
   - `REACT_APP_BACKEND_URL`: https://northstar-ai-backend.onrender.com
5. Click "Create Static Site"

---

## 🎉 Part 4: Alternative - Deploy to Heroku

### Backend Deployment

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
heroku create northstar-ai-backend

# Set environment variables
heroku config:set GOOGLE_API_KEY=your-key
heroku config:set MONGO_URL=your-mongodb-url
heroku config:set DB_NAME=growth_copilot_db

# Deploy
git push heroku main
```

### Frontend Deployment

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/frontend

# Update .env
echo "REACT_APP_BACKEND_URL=https://northstar-ai-backend.herokuapp.com" > .env

# Build
npm run build

# Deploy to Netlify/Vercel (easier for React)
npx netlify-cli deploy --prod --dir=build
```

---

## 📊 Part 5: Get Free MongoDB Atlas

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free tier)
3. Create cluster (M0 free tier)
4. Click "Connect"
5. Create database user
6. Whitelist IP: `0.0.0.0/0` (allow all)
7. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/`
8. Use this as your `MONGO_URL`

---

## 🔧 Part 6: Update Frontend .env

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/frontend

# For local development
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=http://localhost:8001
EOF

# For production (update after backend is deployed)
cat > .env.production << 'EOF'
REACT_APP_BACKEND_URL=https://northstar-ai-backend.onrender.com
EOF
```

---

## 🎯 Quick Start Commands

### Local Development
```bash
# Terminal 1: MongoDB
docker start mongodb

# Terminal 2: Backend
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
python3 -m uvicorn server:app --reload --port 8001

# Terminal 3: Frontend
cd /Users/Anirudh.Kanojia/NorthStar-AI/frontend
npm start

# Open browser: http://localhost:3000
```

---

## 🐛 Troubleshooting

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Backend connection error
- Check `.env` has correct `GOOGLE_API_KEY`
- Check MongoDB is running: `docker ps`
- Check backend is running: `curl http://localhost:8001/api/health`

### CORS errors
- Backend `.env` should have: `CORS_ORIGINS=*`
- For production, set specific domain

---

## 📝 Next Steps

1. **Test Locally**: Start both backend and frontend
2. **Upload Sample Data**: Use files from `sample_data/`
3. **Try Chat Interface**: Ask natural language questions
4. **Deploy**: Choose Render or Heroku
5. **Share**: Get your public URL!

---

## 🎉 Your URLs

**Local:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs

**Production (after deployment):**
- Frontend: https://northstar-ai-frontend.onrender.com
- Backend: https://northstar-ai-backend.onrender.com

---

Ready to start the frontend? Run this now:

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/frontend
npm install
npm start
```
