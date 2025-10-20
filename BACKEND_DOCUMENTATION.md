# NorthStar AI - Enhanced Backend Documentation

## Overview

The NorthStar AI backend has been significantly enhanced with comprehensive AI-powered analytics capabilities. This document outlines all the new features and how to use them.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ REST API Calls
                            │
┌───────────────────────────┴──────────────────────────────────────┐
│                      FastAPI Server (server.py)                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ API Endpoints:                                            │   │
│  │ - /upload/* (with background insights generation)        │   │
│  │ - /insights/enhanced (comprehensive insights)             │   │
│  │ - /query (natural language queries)                       │   │
│  │ - /summary (data overview)                                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                       │
│  ┌──────────────────────────┴───────────────────────────────┐   │
│  │          AI Analysis Engine (ai_engine.py)               │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Capabilities:                                     │   │   │
│  │  │ 1. Metric Trend Analysis                         │   │   │
│  │  │ 2. Release Impact Correlation                    │   │   │
│  │  │ 3. Campaign Effectiveness Analysis               │   │   │
│  │  │ 4. Segment Performance Tracking                  │   │   │
│  │  │ 5. Platform Comparison                           │   │   │
│  │  │ 6. Natural Language Query Processing             │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬──────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
    ┌─────────┴────────┐      ┌──────────┴──────────┐
    │    MongoDB       │      │   Gemini 2.5 Pro    │
    │  (Data Storage)  │      │   (AI Analysis)     │
    └──────────────────┘      └─────────────────────┘
```

## Features

### 1. Automatic Insights Generation

When you upload data (Mixpanel, Jira, or MoEngage), the system automatically:

- **Detects Anomalies**: Identifies week-over-week changes > 5%
- **Triggers Background Analysis**: Generates comprehensive insights without blocking the upload
- **Correlates Data**: Links releases, campaigns, and metric changes

**Example Flow:**
```bash
# Upload Mixpanel data
POST /api/upload/mixpanel
→ Detects 4 anomalies
→ Starts background insight generation
→ Returns immediately with upload confirmation

# Check insights after a few seconds
GET /api/insights/enhanced
→ Returns comprehensive analysis of all detected patterns
```

### 2. Comprehensive Insight Types

The AI engine generates six types of insights:

#### a) **Trend Analysis**
- Analyzes metric changes over time
- Identifies patterns and trajectories
- Correlates with nearby releases and campaigns

Example insight:
```json
{
  "insight_type": "trend_analysis",
  "metric": "activation_rate",
  "summary": "Activation rate declined by 7.1% over the past week",
  "probable_causes": [
    "New signup modal with phone verification introduced",
    "Increased friction in onboarding flow"
  ],
  "affected_segments": ["tier2 android users"],
  "recommendations": [
    "A/B test optional phone verification",
    "Add progress indicator to signup flow"
  ],
  "confidence": "high"
}
```

#### b) **Release Impact Analysis**
- Evaluates how product releases affect metrics
- Measures before/after performance
- Identifies positive and negative impacts

Example insight:
```json
{
  "insight_type": "release_impact",
  "release_id": "1056",
  "summary": "Onboarding flow v2.4 caused 7% decline in activation",
  "positive_impacts": ["Improved security"],
  "negative_impacts": [
    "Activation rate decreased 7%",
    "Sign-up completion dropped 12%"
  ],
  "recommendations": [
    "Make phone verification optional",
    "Add contextual help during verification"
  ],
  "confidence": "high"
}
```

#### c) **Campaign Effectiveness**
- Measures impact of marketing campaigns
- Calculates effectiveness scores
- Provides learnings for future campaigns

Example insight:
```json
{
  "insight_type": "campaign_impact",
  "campaign_id": "c102",
  "summary": "Re-engagement email boosted retention by 10.3%",
  "effectiveness_score": 85,
  "key_learnings": [
    "Email campaigns highly effective for tier1 iOS users",
    "Timing (3 days after inactivity) optimal"
  ],
  "recommendations": [
    "Extend to tier2 segment",
    "Test similar timing for push notifications"
  ],
  "confidence": "high"
}
```

#### d) **Segment Performance**
- Compares user cohorts
- Identifies strengths and weaknesses
- Suggests targeted actions

Example insight:
```json
{
  "insight_type": "segment_analysis",
  "segment": "tier1",
  "summary": "Tier1 users outperforming tier2 by 15% on retention",
  "strengths": ["Higher retention", "Better conversion rates"],
  "weaknesses": ["Lower CTR on promotional content"],
  "recommendations": [
    "Apply tier1 onboarding patterns to tier2",
    "Test premium features with tier1 users"
  ],
  "confidence": "medium"
}
```

#### e) **Platform Comparison**
- Analyzes cross-platform performance
- Identifies platform-specific issues
- Recommends platform optimizations

Example insight:
```json
{
  "insight_type": "platform_comparison",
  "summary": "iOS users show 22% higher retention than Android",
  "best_performing_platform": "ios",
  "areas_for_improvement": {
    "android": "activation_rate",
    "web": "conversion_rate"
  },
  "recommendations": [
    "Investigate Android onboarding UX issues",
    "Optimize web checkout flow"
  ],
  "confidence": "high"
}
```

### 3. Natural Language Queries

Ask questions about your data in plain English:

**Endpoint:** `POST /api/query`

**Example Queries:**

```bash
# Query: Why did new user rate drop?
POST /api/query
{
  "query": "Why did the activation rate drop by 3% last week?"
}

Response:
{
  "answer": "The activation rate declined primarily due to the new signup modal with phone verification (Release 1056), which introduced friction for tier2 Android users. The requirement increased drop-off during onboarding.",
  "supporting_evidence": [
    "Release 1056 deployed on Oct 2, 2025",
    "Activation rate for tier2 Android: 0.42 → 0.39 (-7.1%)",
    "No campaigns targeted this segment during the period"
  ],
  "recommendations": [
    "Make phone verification optional",
    "A/B test verification requirement",
    "Add skip option with incentive to verify later"
  ],
  "confidence": "high"
}
```

```bash
# Query: Which offers retain clients?
POST /api/query
{
  "query": "Which campaign helped retain users the most?"
}

Response:
{
  "answer": "The Re-engagement Email campaign (c102) was most effective, boosting retention by 10.3% for tier1 iOS users.",
  "supporting_evidence": [
    "Campaign launched Oct 3, 2025",
    "Retention rate: 0.68 → 0.75 (+10.3%)",
    "Target segment showed highest engagement"
  ],
  "recommendations": [
    "Scale this campaign to tier2 users",
    "Test similar messaging via push notifications",
    "Implement automated trigger at 3-day inactivity"
  ],
  "confidence": "high"
}
```

```bash
# Query: Feature pain points
POST /api/query
{
  "query": "What feature from the last release is causing interaction decreases?"
}

Response:
{
  "answer": "The new phone verification modal from Release 1056 is the primary pain point, causing decreased interaction during signup.",
  "supporting_evidence": [
    "CTR decreased 16.7% after release",
    "Activation rate down 7.1% for tier2 Android",
    "User feedback indicates friction"
  ],
  "recommendations": [
    "Redesign modal with clearer value proposition",
    "Make verification optional",
    "Add alternative verification methods"
  ],
  "confidence": "high"
}
```

### 4. Manual Insight Generation

Trigger comprehensive analysis on demand:

```bash
POST /api/insights/generate

Response:
{
  "status": "success",
  "message": "Insights generation started in background"
}

# Wait 10-30 seconds, then fetch results
GET /api/insights/enhanced
```

### 5. Data Summary Endpoint

Get an overview of all uploaded data:

```bash
GET /api/summary

Response:
{
  "mixpanel_records": 8,
  "jira_records": 4,
  "moengage_records": 3,
  "detected_anomalies": 4,
  "generated_insights": 12,
  "action_logs": 2
}
```

## API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API info and features |
| `/api/health` | GET | Health check |
| `/api/summary` | GET | Data overview |
| `/api/upload/mixpanel` | POST | Upload Mixpanel CSV |
| `/api/upload/moengage` | POST | Upload MoEngage JSON |
| `/api/upload/jira` | POST | Upload Jira CSV |
| `/api/metrics` | GET | Get detected anomalies |
| `/api/analyze/{anomaly_id}` | POST | Analyze specific anomaly |
| `/api/insights` | GET | Get basic insights |
| `/api/insights/enhanced` | GET | Get comprehensive insights |
| `/api/insights/generate` | POST | Trigger manual analysis |
| `/api/query` | POST | Natural language query |
| `/api/action/trigger` | POST | Trigger action (campaign/task) |
| `/api/action-logs` | GET | Get action logs |
| `/api/reset` | DELETE | Clear all data |

## How It Works

### Data Upload Flow

1. **Upload CSV/JSON** → Data stored in MongoDB
2. **Anomaly Detection** → Week-over-week changes > 5% flagged
3. **Background Task** → AI engine starts comprehensive analysis
4. **Insight Generation** → Multiple analysis types run in parallel:
   - Trend analysis for each metric
   - Release impact correlation
   - Campaign effectiveness
   - Segment comparison
   - Platform comparison
5. **Storage** → Insights saved to `enhanced_insights` collection
6. **Retrieval** → Frontend fetches via `/api/insights/enhanced`

### AI Analysis Process

```python
# For each metric with anomaly:
1. Collect temporal context (7 days before/after)
2. Find related releases (within 7 days)
3. Find related campaigns (same platform/segment)
4. Send to Gemini 2.5 Pro with structured prompt
5. Parse JSON response
6. Store with metadata (confidence, type, timestamp)
```

### Query Processing Flow

```python
# Natural language query:
1. Fetch all available data (Mixpanel, Jira, MoEngage)
2. Fetch existing insights
3. Build context-rich prompt
4. Send to Gemini 2.5 Pro
5. Extract answer + evidence + recommendations
6. Return structured response
```

## Configuration

### Environment Variables

```bash
# .env file
MONGO_URL="mongodb://localhost:27017"
DB_NAME="growth_copilot_db"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY="sk-emergent-..."
```

### MongoDB Collections

- `mixpanel_data` - Metric time series
- `jira_data` - Release notes
- `moengage_data` - Campaign metadata
- `metric_anomalies` - Detected changes > 5%
- `ai_insights` - Basic AI insights (legacy)
- `enhanced_insights` - Comprehensive AI insights (new)
- `action_logs` - Triggered actions

## Performance Considerations

### Background Processing

- Insights generation runs asynchronously
- Upload endpoints return immediately (< 1s)
- Comprehensive analysis completes in 10-30 seconds
- No blocking or waiting required

### AI API Calls

- Each insight type makes 1 AI call
- Typical analysis generates 5-15 insights
- Total API calls: 5-15 per analysis run
- Rate limiting: Handled by Emergent platform

### Scalability

- MongoDB handles 1000+ records efficiently
- Pandas processing optimized for datasets < 10K rows
- For larger datasets, consider:
  - Sampling strategies
  - Chunked processing
  - Caching frequently accessed insights

## Best Practices

### 1. Upload Strategy

```bash
# Upload in this order for best insights:
1. Upload Mixpanel data (metrics)
2. Upload Jira data (releases)
3. Upload MoEngage data (campaigns)
4. Wait 30 seconds
5. Fetch enhanced insights
```

### 2. Query Formulation

**Good queries (specific, actionable):**
- "Why did activation rate drop for Android users?"
- "Which campaign had the best ROI for tier2 segment?"
- "What release caused the CTR decline?"

**Poor queries (too vague):**
- "Tell me about my data"
- "What happened?"
- "Give me insights"

### 3. Insight Interpretation

- **High confidence (> 80%)**: Strong correlation, act on recommendations
- **Medium confidence (50-80%)**: Investigate further before acting
- **Low confidence (< 50%)**: Use as hypothesis to test

## Troubleshooting

### Issue: No insights generated after upload

**Solution:**
```bash
# Check background task status
GET /api/summary

# If insights_generated = 0:
POST /api/insights/generate

# Wait 30 seconds
GET /api/insights/enhanced
```

### Issue: Query returns "Unable to process query"

**Causes:**
- No data uploaded yet
- Query too vague
- API rate limit hit

**Solution:**
```bash
# Check data availability
GET /api/summary

# Ensure all collections have data
# Reformulate query with more specifics
```

### Issue: Slow insight generation

**Optimization:**
- Reduce Mixpanel data to recent 30 days
- Limit Jira releases to last 3 months
- Filter MoEngage campaigns to active only

## Future Enhancements

Planned features:
1. **Predictive Analytics** - Forecast metric trends
2. **Automated Actions** - Real integration with MoEngage/Jira APIs
3. **Slack Integration** - Daily insight summaries
4. **Custom Anomaly Thresholds** - Configure sensitivity per metric
5. **Cohort Analysis** - Deep-dive into specific user segments
6. **Experiment Tracking** - A/B test impact analysis
7. **Cost Attribution** - CAC and LTV calculations

## Examples

See `sample_data/` directory for example files:
- `mixpanel_sample.csv` - Metric data format
- `jira_sample.csv` - Release notes format
- `moengage_sample.json` - Campaign data format

## Support

For issues or questions:
1. Check logs: `tail -f backend/logs/server.log`
2. Verify environment variables
3. Test MongoDB connection
4. Validate Emergent API key

---

Built with ❤️ using Gemini 2.5 Pro and FastAPI
