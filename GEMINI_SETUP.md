# ✅ Gemini Setup Complete!

## What I Did

1. ✅ Updated `.env` file to use `GOOGLE_API_KEY` instead of `EMERGENT_LLM_KEY`
2. ✅ Modified `ai_engine.py` to use Google Gemini API directly
3. ✅ Modified `server.py` to use Google Gemini API directly
4. ✅ Using **Gemini 2.0 Flash** (free tier, fast, smart)

## 🎯 What You Need to Do Now

### Step 1: Get Your Gemini API Key (2 minutes)

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Click **"Create API key in new project"** (or select existing)
5. **Copy the API key** (starts with `AIza...`)

### Step 2: Add Your API Key to .env

Open the `.env` file and replace `your-gemini-api-key-here` with your actual key:

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend

# Option 1: Edit with nano
nano .env

# Option 2: Edit with VS Code
code .env

# Option 3: Use cat (if you have your key ready)
cat > .env << 'EOF'
MONGO_URL=mongodb://localhost:27017
DB_NAME=growth_copilot_db
CORS_ORIGINS=*
GOOGLE_API_KEY=AIza...your-actual-key-here...
EOF
```

The file should look like:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=growth_copilot_db
CORS_ORIGINS=*
GOOGLE_API_KEY=AIzaSyABC123XYZ...your-actual-key...
```

### Step 3: Start MongoDB (if not already running)

```bash
# Check if MongoDB is running
ps aux | grep mongod

# If not running, start with Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or start local MongoDB:
mongod --dbpath /path/to/data
```

### Step 4: Start the Backend Server

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
uvicorn server:app --reload --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

### Step 5: Test It!

Open a **new terminal** and run:

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI
python play_with_backend.py
```

Or test manually:
```bash
curl http://localhost:8001/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_engine": "ready"
}
```

## 🎉 That's It!

Once you add your Gemini API key, everything will work!

## 📊 Gemini Free Tier Limits

- ✅ **15 requests per minute**
- ✅ **1500 requests per day**
- ✅ **1 million tokens per day**
- ✅ Perfect for testing and development!

## 🔍 Troubleshooting

### If you get "API key not configured"
- Make sure you saved the .env file
- Check the key starts with `AIza`
- Restart the server after updating .env

### If MongoDB connection fails
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Check if everything is working
```bash
# Test health
curl http://localhost:8001/api/health

# Should return:
# {"status":"healthy","database":"connected","ai_engine":"ready"}
```

## 📚 Next Steps

Once the backend starts successfully:

1. Upload sample data
2. See AI insights generated
3. Ask natural language questions
4. Integrate with your React frontend

---

**Ready to start?** Get your Gemini API key from:
👉 https://aistudio.google.com/app/apikey

Then add it to `/Users/Anirudh.Kanojia/NorthStar-AI/backend/.env`
