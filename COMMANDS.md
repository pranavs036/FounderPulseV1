# 🚀 Quick Command Reference

## Start Everything (Copy-Paste Ready)

```bash
# Terminal 1: Start MongoDB (if not running)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Terminal 2: Start Backend Server
cd /Users/Anirudh.Kanojia/NorthStar-AI/backend
uvicorn server:app --reload --port 8001

# Terminal 3: Run Interactive Test
cd /Users/Anirudh.Kanojia/NorthStar-AI
python play_with_backend.py
```

## Or Use the One-Liner

```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI && chmod +x start_backend.sh && ./start_backend.sh
```

Then in another terminal:
```bash
cd /Users/Anirudh.Kanojia/NorthStar-AI && python play_with_backend.py
```

## Quick Manual Test (5 commands)

```bash
# 1. Upload data
curl -X POST http://localhost:8001/api/upload/mixpanel -F "file=@sample_data/mixpanel_sample.csv"
curl -X POST http://localhost:8001/api/upload/jira -F "file=@sample_data/jira_sample.csv"
curl -X POST http://localhost:8001/api/upload/moengage -F "file=@sample_data/moengage_sample.json"

# 2. Wait for AI (30 seconds)
sleep 30

# 3. Get insights
curl http://localhost:8001/api/insights/enhanced | jq

# 4. Ask a question
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Why did activation rate drop?"}' | jq

# 5. Get summary
curl http://localhost:8001/api/summary | jq
```

## Important URLs

- **Server**: http://localhost:8001
- **Health Check**: http://localhost:8001/api/health
- **Interactive Docs**: http://localhost:8001/docs
- **API Base**: http://localhost:8001/api

## Sample Files Location

```
/Users/Anirudh.Kanojia/NorthStar-AI/sample_data/
├── mixpanel_sample.csv          # Basic metrics
├── jira_sample.csv              # Basic releases
├── moengage_sample.json         # Basic campaigns
├── mixpanel_extended.csv        # More metrics
├── jira_extended.csv            # More releases
└── moengage_extended.json       # More campaigns
```

## Troubleshooting One-Liners

```bash
# Check if MongoDB is running
ps aux | grep mongod

# Check if backend is running
curl http://localhost:8001/api/health

# Reset all data
curl -X DELETE http://localhost:8001/api/reset

# Manually trigger insights
curl -X POST http://localhost:8001/api/insights/generate

# View server logs (if running in background)
tail -f /path/to/server.log
```

## File You Need to Update

```bash
# Edit this file and add your Emergent API key:
nano /Users/Anirudh.Kanojia/NorthStar-AI/backend/.env

# Change this line:
EMERGENT_LLM_KEY=your-actual-key-here
```

## That's It!

Everything else is automated. Just run the commands above and watch the magic happen! ✨
