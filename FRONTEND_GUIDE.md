# 🎨 Frontend Setup and Deployment Guide

## ✅ What's Been Done

I've completely integrated the frontend with your backend and added a Chat Interface! Here's what's new:

### New Features Added:
1. **✨ AI Chat Interface** - Natural language queries with your data
2. **📊 Enhanced Insights Tab** - Shows comprehensive AI analysis
3. **🔄 Auto-refresh** - Data updates automatically after uploads
4. **📈 Data Summary** - Real-time stats in the header
5. **🎯 Generate Insights Button** - Manual trigger for AI analysis
6. **🎨 Improved UI** - Better visual hierarchy and user experience

### New Files Created:
- `/src/components/ChatInterface.jsx` - Complete chat UI with message history
- `/src/services/api.js` - Clean API service layer
- `/frontend/.env` - Environment configuration

### Updated Files:
- `/src/pages/Dashboard.jsx` - Integrated chat, enhanced insights, better data flow

---

## 🚀 How to Run the Frontend

### Step 1: Install Dependencies

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/frontend

# Install all packages
npm install
# or
yarn install
```

This will install all required packages including React, Tailwind, shadcn/ui components, etc.

### Step 2: Start the Development Server

```bash
# Start frontend (runs on http://localhost:3000)
npm start
# or
yarn start
```

The app will automatically open in your browser at `http://localhost:3000`

---

## 🎯 Complete System - How to Run Everything

### Terminal 1: MongoDB
```bash
docker ps  # Check if already running
# If not running:
docker start mongodb
# Or start fresh:
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Terminal 2: Backend Server
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
python3 -m uvicorn server:app --reload --port 8001
```

### Terminal 3: Frontend
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/frontend
npm start
```

---

## 🎨 Using the Frontend

### 1. **Overview Tab** - Upload Data
- Upload Mixpanel CSV, Jira CSV, and MoEngage JSON files
- See detected anomalies in real-time
- Click "Analyze with AI" on any metric card
- Click "Generate Insights" button for comprehensive analysis

### 2. **Insights Tab** - View AI Analysis
- See all AI-generated insights
- Trigger MoEngage campaigns or Jira tasks
- View confidence levels (high/medium/low)
- See recommendations for each insight

### 3. **Chat Tab** - Ask Questions! 🆕
This is the BIG new feature you requested!

**Try asking:**
- "Why did activation rate drop for Android users?"
- "Which campaign performed best?"
- "What caused the biggest metric change?"
- "How do tier1 users compare to tier2 users?"

The AI will:
- Answer your question directly
- Provide supporting evidence from your data
- Give actionable recommendations
- Show confidence level

**Features:**
- ✅ Message history
- ✅ Real-time responses
- ✅ Suggested questions
- ✅ Evidence and recommendations in each response
- ✅ Confidence scoring
- ✅ Beautiful chat UI with user/assistant messages

### 4. **Actions Tab** - View Triggered Actions
- See all campaign triggers
- View Jira task creations
- Track action history

---

## 📱 The Chat Interface

The chat interface looks like this:

```
┌─────────────────────────────────────────┐
│  🤖 AI Chat Assistant                   │
│  Ask questions about your data          │
├─────────────────────────────────────────┤
│                                         │
│  🤖 Hi! I'm your AI analyst.           │
│     Ask me anything about your          │
│     metrics, releases, or campaigns!    │
│                                         │
│     [Try asking: Why did...]  [Which...]│
│                                         │
│         Your question here? 👤         │
│                                         │
│  🤖 The activation rate declined...     │
│     📊 Evidence:                        │
│     • Release 1056 on Oct 2            │
│     • Activation: 0.42 → 0.39 (-7%)   │
│     💡 Recommendations:                 │
│     → Make verification optional        │
│     → A/B test requirement             │
│     [high confidence]                   │
│                                         │
├─────────────────────────────────────────┤
│ [Type your question...]     [Send 📤]  │
└─────────────────────────────────────────┘
```

---

## 🎯 Testing the Complete Flow

### 1. Start All Services
```bash
# Terminal 1
docker start mongodb

# Terminal 2  
cd backend && python3 -m uvicorn server:app --reload --port 8001

# Terminal 3
cd frontend && npm start
```

### 2. Open Browser
Go to: `http://localhost:3000`

### 3. Upload Data
- Click "Select File" for Mixpanel → Choose `sample_data/mixpanel_sample.csv` → Upload
- Click "Select File" for Jira → Choose `sample_data/jira_sample.csv` → Upload
- Click "Select File" for MoEngage → Choose `sample_data/moengage_sample.json` → Upload

### 4. Wait & Generate Insights
- Wait 5 seconds after uploads
- Click "Generate Insights" button
- Wait 30 seconds for AI analysis

### 5. View Insights
- Click "Insights" tab
- See comprehensive AI analysis

### 6. Chat with AI! 🎯
- Click "Chat" tab
- Click a suggested question or type your own
- Get instant AI-powered answers!

---

## 🌐 Deploying to Production

### Option 1: Vercel (Frontend) + Railway (Backend)

**Frontend on Vercel:**
```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Update environment variable on Vercel dashboard:
REACT_APP_BACKEND_URL=https://your-backend.railway.app
```

**Backend on Railway:**
1. Go to railway.app
2. Create new project
3. Connect GitHub repo
4. Set environment variables:
   - `MONGO_URL`
   - `GOOGLE_API_KEY`
   - `DB_NAME`
5. Deploy!

### Option 2: AWS (Complete Stack)

**Frontend on S3 + CloudFront:**
```bash
cd frontend
npm run build

# Upload build/ folder to S3
# Set up CloudFront distribution
```

**Backend on EC2 or ECS:**
- Deploy FastAPI with Docker
- Use RDS for PostgreSQL or MongoDB Atlas
- Set up load balancer

### Option 3: Heroku (Easy but paid)

**Frontend:**
```bash
cd frontend
# Add buildpack: heroku/nodejs
heroku create northstar-frontend
git push heroku main
```

**Backend:**
```bash
cd backend
# Add Procfile
heroku create northstar-backend
git push heroku main
```

---

## 🔧 Environment Variables

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

For production:
```
REACT_APP_BACKEND_URL=https://your-backend-domain.com
```

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=growth_copilot_db
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
GOOGLE_API_KEY=AIza...your-key...
```

---

## 📊 API Endpoints Used by Frontend

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check backend status |
| `/api/summary` | GET | Get data overview |
| `/api/upload/mixpanel` | POST | Upload metrics |
| `/api/upload/jira` | POST | Upload releases |
| `/api/upload/moengage` | POST | Upload campaigns |
| `/api/metrics` | GET | Get anomalies |
| `/api/insights` | GET | Get basic insights |
| `/api/insights/enhanced` | GET | Get AI insights |
| `/api/insights/generate` | POST | Trigger analysis |
| `/api/query` | POST | **Chat queries** 🆕 |
| `/api/action/trigger` | POST | Trigger actions |
| `/api/action-logs` | GET | Get action history |

---

## 🎨 Customizing the UI

### Colors
Edit `/frontend/tailwind.config.js`:
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: "#3b82f6",  // Change blue
        secondary: "#8b5cf6", // Change purple
      }
    }
  }
}
```

### Logo
Replace the `<Activity />` icon in `Dashboard.jsx` with your logo:
```javascript
<img src="/your-logo.png" alt="Logo" className="w-10 h-10" />
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to backend"
**Solution:**
```bash
# Check backend is running
curl http://localhost:8001/api/health

# Check .env file
cat frontend/.env  # Should show REACT_APP_BACKEND_URL=http://localhost:8001
```

### Issue: "Module not found"
**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: Chat not working
**Solution:**
- Make sure backend has Gemini API key configured
- Check browser console for errors (F12)
- Verify backend `/api/query` endpoint works:
```bash
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

---

## ✨ Features Summary

### What You Can Do Now:
1. ✅ Upload data files (Mixpanel, Jira, MoEngage)
2. ✅ See anomalies detected automatically
3. ✅ Generate comprehensive AI insights
4. ✅ **Chat with AI about your data** 🆕
5. ✅ Ask natural language questions
6. ✅ Get evidence-based answers
7. ✅ Trigger MoEngage campaigns
8. ✅ Create Jira tasks
9. ✅ View action history

### The Chat Interface Gives You:
- 💬 Natural conversation with AI
- 📊 Evidence-based answers
- 💡 Actionable recommendations
- 🎯 Confidence scoring
- 🕐 Message history
- ✨ Suggested questions

---

## 🎉 You're Ready!

Your complete Growth Copilot platform is now ready with:
- ✅ Beautiful UI
- ✅ AI-powered insights
- ✅ **Interactive chat interface**
- ✅ Real-time analysis
- ✅ Action triggers
- ✅ Full data integration

**Start the frontend and enjoy your AI growth analyst!** 🚀

```bash
cd frontend && npm start
```

Then open `http://localhost:3000` and start chatting with your AI! 💬
