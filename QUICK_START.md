# Quick Start Guide - NorthStar AI Backend

## Setup (5 minutes)

### 1. Install Dependencies

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in `backend/` directory:

```bash
MONGO_URL="mongodb://localhost:27017"
DB_NAME="growth_copilot_db"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY="your-emergent-api-key-here"
```

### 3. Start MongoDB

```bash
# If using Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest

# If using local MongoDB:
mongod --dbpath /path/to/data
```

### 4. Start Backend Server

```bash
cd backend
uvicorn server:app --reload --port 8001
```

Server will start at: `http://localhost:8001`

## Test the Enhanced Backend (2 minutes)

### Step 1: Upload Sample Data

```bash
# Upload Mixpanel data
curl -X POST http://localhost:8001/api/upload/mixpanel \
  -F "file=@../sample_data/mixpanel_sample.csv"

# Upload Jira data
curl -X POST http://localhost:8001/api/upload/jira \
  -F "file=@../sample_data/jira_sample.csv"

# Upload MoEngage data
curl -X POST http://localhost:8001/api/upload/moengage \
  -F "file=@../sample_data/moengage_sample.json"
```

### Step 2: Wait for Background Processing

```bash
# Wait 30 seconds for AI analysis to complete
sleep 30
```

### Step 3: Check Results

```bash
# Get data summary
curl http://localhost:8001/api/summary

# Get detected anomalies
curl http://localhost:8001/api/metrics

# Get comprehensive AI insights
curl http://localhost:8001/api/insights/enhanced
```

### Step 4: Try Natural Language Query

```bash
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Why did activation rate drop for Android users?"}'
```

## API Testing with Python

```python
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8001/api"

# 1. Upload data
with open('../sample_data/mixpanel_sample.csv', 'rb') as f:
    response = requests.post(f"{BASE_URL}/upload/mixpanel", files={'file': f})
    print("Mixpanel upload:", response.json())

with open('../sample_data/jira_sample.csv', 'rb') as f:
    response = requests.post(f"{BASE_URL}/upload/jira", files={'file': f})
    print("Jira upload:", response.json())

with open('../sample_data/moengage_sample.json', 'rb') as f:
    response = requests.post(f"{BASE_URL}/upload/moengage", files={'file': f})
    print("MoEngage upload:", response.json())

# 2. Wait for background processing
print("\nWaiting for AI analysis...")
sleep(30)

# 3. Get comprehensive insights
response = requests.get(f"{BASE_URL}/insights/enhanced")
insights = response.json()
print(f"\nGenerated {len(insights)} comprehensive insights:")
for insight in insights[:3]:  # Show first 3
    print(f"\n- Type: {insight['insight_type']}")
    print(f"  Summary: {insight['summary']}")
    print(f"  Confidence: {insight['confidence']}")

# 4. Ask natural language question
query = {
    "query": "Why did the activation rate drop by 3% last week?"
}
response = requests.post(f"{BASE_URL}/query", json=query)
result = response.json()
print("\n\nQuery Result:")
print(f"Answer: {result['answer']}")
print(f"\nEvidence:")
for evidence in result['supporting_evidence']:
    print(f"  - {evidence}")
print(f"\nRecommendations:")
for rec in result['recommendations']:
    print(f"  - {rec}")
```

## Frontend Integration

Update your React frontend to use the new endpoints:

```javascript
// src/api/insights.js
export const getEnhancedInsights = async () => {
  const response = await fetch(`${API_BASE_URL}/insights/enhanced`);
  return response.json();
};

export const queryData = async (query) => {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  return response.json();
};

export const getSummary = async () => {
  const response = await fetch(`${API_BASE_URL}/summary`);
  return response.json();
};

export const triggerInsightsGeneration = async () => {
  const response = await fetch(`${API_BASE_URL}/insights/generate`, {
    method: 'POST'
  });
  return response.json();
};
```

## Common Use Cases

### Use Case 1: Daily Metrics Check

```bash
# Morning routine: Check what changed overnight
curl http://localhost:8001/api/metrics | jq '.[] | select(.change_percent < -5)'

# Get AI explanation for top decline
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What caused the biggest metric decline today?"}'
```

### Use Case 2: Release Impact Analysis

```bash
# After deploying a release, upload Jira data
curl -X POST http://localhost:8001/api/upload/jira \
  -F "file=@new_release.csv"

# Wait and check release impact
sleep 30
curl http://localhost:8001/api/insights/enhanced | \
  jq '.[] | select(.insight_type == "release_impact")'
```

### Use Case 3: Campaign Performance

```bash
# After running campaigns, check effectiveness
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Which campaign performed best this week?"}'
```

### Use Case 4: Segment Analysis

```bash
# Compare user segments
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do tier1 users compare to tier2 in terms of retention?"}'
```

## Monitoring and Logs

### Check Server Health

```bash
curl http://localhost:8001/api/health
```

### View Logs

```bash
# Server logs (if running with uvicorn)
tail -f /path/to/server.log

# In the terminal where uvicorn is running, you'll see:
# INFO:     AI Analysis Engine: Starting comprehensive insights generation...
# INFO:     Generated and stored 12 new comprehensive insights
```

### MongoDB Inspection

```bash
# Connect to MongoDB
mongosh

# Switch to database
use growth_copilot_db

# Check collections
show collections

# View insights
db.enhanced_insights.find().pretty()

# Count documents
db.mixpanel_data.countDocuments()
db.enhanced_insights.countDocuments()
```

## Troubleshooting

### Issue: Import error for ai_engine

**Error:**
```
ModuleNotFoundError: No module named 'ai_engine'
```

**Solution:**
```bash
# Ensure ai_engine.py is in the backend/ directory
ls backend/ai_engine.py

# If missing, the file should have been created
# Make sure you're running from the correct directory
cd backend
python -c "import ai_engine; print('OK')"
```

### Issue: MongoDB connection failed

**Error:**
```
ServerSelectionTimeoutError: localhost:27017
```

**Solution:**
```bash
# Check if MongoDB is running
ps aux | grep mongod

# Start MongoDB
mongod --dbpath /path/to/data

# Or with Docker
docker start mongodb
```

### Issue: No insights generated

**Symptoms:**
- Upload succeeds
- `/api/summary` shows `generated_insights: 0`

**Solution:**
```bash
# Manually trigger insights
curl -X POST http://localhost:8001/api/insights/generate

# Check server logs for errors
# Wait 30 seconds and check again
curl http://localhost:8001/api/summary
```

### Issue: AI query returns error

**Error:**
```json
{
  "answer": "Unable to process query",
  "error": "API rate limit exceeded"
}
```

**Solution:**
- Check your Emergent API key is valid
- Wait a few minutes for rate limit reset
- Ensure `EMERGENT_LLM_KEY` is set correctly

## Performance Optimization

### For Large Datasets

```python
# Limit data to recent periods before upload
import pandas as pd

df = pd.read_csv('large_mixpanel_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Keep only last 30 days
cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=30)
df_recent = df[df['date'] >= cutoff_date]

df_recent.to_csv('filtered_mixpanel.csv', index=False)
```

### Caching Strategy

For production, consider implementing Redis caching:

```python
# Example caching for insights
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Cache insights for 1 hour
@api_router.get("/insights/enhanced")
async def get_enhanced_insights():
    cached = redis_client.get('enhanced_insights')
    if cached:
        return json.loads(cached)
    
    insights = await db.enhanced_insights.find({}, {"_id": 0}).to_list(1000)
    redis_client.setex('enhanced_insights', 3600, json.dumps(insights))
    return insights
```

## Next Steps

1. **Integrate with Frontend**
   - Add query interface component
   - Display enhanced insights
   - Show data summary dashboard

2. **Set Up Scheduled Jobs**
   - Daily insight generation
   - Weekly summary reports
   - Automated anomaly alerts

3. **Configure Monitoring**
   - Set up logging aggregation
   - Add performance metrics
   - Monitor AI API usage

4. **Production Deployment**
   - Set up environment variables securely
   - Configure CORS properly
   - Add authentication
   - Set up backup for MongoDB

## Resources

- **Backend Documentation**: See `BACKEND_DOCUMENTATION.md` for detailed API reference
- **Sample Data**: Check `sample_data/` directory
- **FastAPI Docs**: `http://localhost:8001/docs` (interactive API documentation)
- **MongoDB GUI**: Use MongoDB Compass for visual database inspection

## Getting Help

If you encounter issues:

1. Check server logs for detailed error messages
2. Verify all environment variables are set
3. Test MongoDB connection separately
4. Validate Emergent API key with a simple test
5. Review the comprehensive documentation

---

**You're all set!** 🚀 

The enhanced backend now provides:
- ✅ Automatic anomaly detection
- ✅ Comprehensive AI insights (6 types)
- ✅ Natural language queries
- ✅ Release impact analysis
- ✅ Campaign effectiveness tracking
- ✅ Segment performance comparison
- ✅ Background processing for fast uploads

Start uploading your data and let AI find insights you might have missed!
