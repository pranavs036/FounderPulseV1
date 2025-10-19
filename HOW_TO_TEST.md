# 🎮 How to Play with NorthStar AI Backend

## Quick Start (3 Steps)

### Step 1: Start MongoDB

Choose one option:

**Option A: Using Docker (Recommended)**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Option B: Using Local MongoDB**
```bash
mongod --dbpath /path/to/your/data
```

**Option C: Check if already running**
```bash
# On Mac/Linux
ps aux | grep mongod

# If running, you'll see mongod process
```

### Step 2: Start the Backend

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI

# Make script executable
chmod +x start_backend.sh

# Run it
./start_backend.sh
```

Or manually:
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend

# Create .env if needed
cat > .env << 'EOF'
MONGO_URL=mongodb://localhost:27017
DB_NAME=growth_copilot_db
CORS_ORIGINS=*
EMERGENT_LLM_KEY=your-actual-key-here
EOF

# Start server
uvicorn server:app --reload --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Run the Interactive Test

Open a **NEW terminal** (keep the server running in the first one):

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI

# Run the interactive test script
python play_with_backend.py
```

This will:
1. ✓ Check if server is healthy
2. ✓ Clear old data
3. ✓ Upload Mixpanel data (metrics)
4. ✓ Upload Jira data (releases)
5. ✓ Upload MoEngage data (campaigns)
6. ✓ Show detected anomalies
7. ✓ Wait for AI analysis (30 seconds)
8. ✓ Display AI-generated insights
9. ✓ Answer natural language questions

## 📁 Sample Data Files Available

Your project has these test files ready:

### Basic Sample Data
```
sample_data/
├── mixpanel_sample.csv      # 8 metric records, 4 anomalies
├── jira_sample.csv           # 4 releases
└── moengage_sample.json      # 3 campaigns
```

### Extended Sample Data (More scenarios)
```
sample_data/
├── mixpanel_extended.csv     # 20 metric records
├── jira_extended.csv         # 5 more releases
└── moengage_extended.json    # 4 more campaigns
```

## 🧪 Manual Testing with cURL

### 1. Health Check
```bash
curl http://localhost:8001/api/health | jq
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_engine": "ready"
}
```

### 2. Upload Mixpanel Data
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI

curl -X POST http://localhost:8001/api/upload/mixpanel \
  -F "file=@sample_data/mixpanel_sample.csv" | jq
```

Expected response:
```json
{
  "id": "...",
  "file_type": "mixpanel",
  "filename": "mixpanel_sample.csv",
  "record_count": 8,
  "insights_generated": 4,
  "status": "success"
}
```

### 3. Upload Jira Data
```bash
curl -X POST http://localhost:8001/api/upload/jira \
  -F "file=@sample_data/jira_sample.csv" | jq
```

### 4. Upload MoEngage Data
```bash
curl -X POST http://localhost:8001/api/upload/moengage \
  -F "file=@sample_data/moengage_sample.json" | jq
```

### 5. Get Data Summary
```bash
curl http://localhost:8001/api/summary | jq
```

Expected response:
```json
{
  "mixpanel_records": 8,
  "jira_records": 4,
  "moengage_records": 3,
  "detected_anomalies": 4,
  "generated_insights": 12,
  "action_logs": 0
}
```

### 6. View Detected Anomalies
```bash
curl http://localhost:8001/api/metrics | jq
```

### 7. Wait for AI Analysis (30 seconds)
```bash
echo "Waiting for AI analysis..."
sleep 30
```

### 8. Get Enhanced Insights
```bash
curl http://localhost:8001/api/insights/enhanced | jq
```

### 9. Ask a Question
```bash
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Why did activation rate drop for Android users?"
  }' | jq
```

Expected response:
```json
{
  "answer": "The activation rate declined primarily due to...",
  "supporting_evidence": [
    "Release 1056 deployed on Oct 2, 2025",
    "Activation rate for tier2 Android: 0.42 → 0.39 (-7.1%)"
  ],
  "recommendations": [
    "Make phone verification optional",
    "A/B test verification requirement"
  ],
  "confidence": "high"
}
```

## 🌐 Using the Interactive API Docs

Visit: **http://localhost:8001/docs**

This gives you a Swagger UI where you can:
- See all available endpoints
- Try them directly in the browser
- See request/response schemas
- No need for curl or Python!

### To test via Swagger:
1. Go to http://localhost:8001/docs
2. Click on any endpoint (e.g., `POST /api/upload/mixpanel`)
3. Click "Try it out"
4. Upload a file or enter JSON
5. Click "Execute"
6. See the response below

## 🧪 Test Different Scenarios

### Scenario 1: Upload Extended Data (More Metrics)
```bash
# Reset first
curl -X DELETE http://localhost:8001/api/reset

# Upload extended data
curl -X POST http://localhost:8001/api/upload/mixpanel \
  -F "file=@sample_data/mixpanel_extended.csv"

curl -X POST http://localhost:8001/api/upload/jira \
  -F "file=@sample_data/jira_extended.csv"

curl -X POST http://localhost:8001/api/upload/moengage \
  -F "file=@sample_data/moengage_extended.json"

# Wait 30 seconds
sleep 30

# Get insights
curl http://localhost:8001/api/insights/enhanced | jq
```

### Scenario 2: Ask Multiple Questions
```bash
# Question 1
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Which platform performs best?"}' | jq

# Question 2
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What caused the biggest metric decline?"}' | jq

# Question 3
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How effective were the campaigns?"}' | jq
```

### Scenario 3: Manual Insight Generation
```bash
# Trigger manual analysis
curl -X POST http://localhost:8001/api/insights/generate

# Wait 30 seconds
sleep 30

# Check results
curl http://localhost:8001/api/insights/enhanced | jq
```

## 🔍 What to Look For

### 1. Metric Anomalies
Check: `curl http://localhost:8001/api/metrics | jq`

Look for:
- ✓ Metrics with >5% change
- ✓ Platform and segment information
- ✓ Before/after values

### 2. AI Insights
Check: `curl http://localhost:8001/api/insights/enhanced | jq`

You should see 6 types of insights:
- **trend_analysis** - Metric trends over time
- **release_impact** - How releases affected metrics
- **campaign_impact** - Campaign effectiveness
- **segment_analysis** - User segment comparison
- **platform_comparison** - Cross-platform performance

### 3. Query Responses
Check your natural language query responses for:
- ✓ Clear, direct answer
- ✓ Supporting evidence (data points)
- ✓ Actionable recommendations
- ✓ Confidence score (high/medium/low)

## 🐛 Troubleshooting

### Issue: "Cannot connect to server"
**Solution:**
```bash
# Check if server is running
curl http://localhost:8001/api/health

# If not, start it:
cd backend
uvicorn server:app --reload --port 8001
```

### Issue: "No insights generated"
**Solution:**
```bash
# Check if data is uploaded
curl http://localhost:8001/api/summary | jq

# If insights_generated is 0, manually trigger:
curl -X POST http://localhost:8001/api/insights/generate

# Wait 30 seconds
sleep 30

# Check again
curl http://localhost:8001/api/insights/enhanced | jq
```

### Issue: "MongoDB connection failed"
**Solution:**
```bash
# Check if MongoDB is running
ps aux | grep mongod

# Start MongoDB with Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or start local MongoDB:
mongod --dbpath /path/to/data
```

### Issue: AI query returns error
**Solution:**
- Check your `EMERGENT_LLM_KEY` in `backend/.env`
- Make sure you have uploaded all 3 data sources
- Wait 30 seconds after upload for insights to generate

## 📊 Expected Results

After running the full test, you should see:

### Anomalies Detected: 4
1. Activation rate (Android, tier2): -7.1%
2. Retention rate (iOS, tier1): +10.3%
3. CTR (Android, tier1): -16.7%
4. Conversion rate (Web, tier2): -20.0%

### Insights Generated: 10-15
- 3-4 trend analysis insights
- 2-3 release impact insights
- 2-3 campaign impact insights
- 1-2 segment analysis insights
- 1-2 platform comparison insights

### Queries Answered: 100%
All natural language queries should return:
- Clear answer
- Supporting evidence
- Recommendations
- Confidence score

## 🎓 Next Steps

Once everything works:

1. **Create Your Own Data Files**
   - Export real Mixpanel data
   - Get actual Jira releases
   - Export MoEngage campaigns

2. **Integrate with Frontend**
   - Connect React app to these endpoints
   - Build query interface
   - Display insights dashboard

3. **Customize AI Prompts**
   - Edit `backend/ai_engine.py`
   - Tune prompts for your domain
   - Adjust confidence thresholds

4. **Set Up Automation**
   - Schedule daily uploads
   - Email insight summaries
   - Slack notifications

## 📚 Resources

- **Interactive API Docs**: http://localhost:8001/docs
- **Backend Documentation**: `BACKEND_DOCUMENTATION.md`
- **Quick Start Guide**: `QUICK_START.md`
- **Implementation Summary**: `IMPLEMENTATION_SUMMARY.md`

## 🎉 You're Ready!

You now know how to:
- ✅ Start the backend
- ✅ Upload data files
- ✅ View anomalies and insights
- ✅ Ask natural language questions
- ✅ Test all features

**Happy testing!** 🚀
