# NorthStar AI - Growth Analytics Platform

An AI-powered growth analytics platform that automatically analyzes Mixpanel, MoEngage, and Jira data to provide comprehensive insights, answer natural language queries, and identify the root causes of metric changes.

## 🆕 What's New in v2.0

✨ **Comprehensive AI Analysis Engine** - Automatically generates 6 types of insights
✨ **Natural Language Queries** - Ask questions about your data in plain English
✨ **Background Processing** - Upload files instantly, insights generated asynchronously
✨ **Release Impact Analysis** - Automatically correlates product releases with metric changes
✨ **Campaign Effectiveness** - Measures and scores marketing campaign performance
✨ **Segment Performance** - Compares user cohorts and identifies opportunities

## Features

✅ **Data Integration**
- Upload Mixpanel CSV exports (date, metric, value, platform, cohort)
- Upload MoEngage JSON (campaign metadata)
- Upload Jira CSV (release notes and features)

✅ **Metric Change Detection**
- Automatic week-over-week % change calculation
- Flags metrics with changes > 5%
- Groups by metric, platform, and cohort

✅ **AI Analysis (Gemini 2.5 Pro)**
- Analyzes probable causes of metric changes
- Identifies affected user segments
- Generates actionable recommendations
- Correlates with release notes and campaigns

✅ **Action Triggers**
- Simulate MoEngage campaign creation
- Simulate Jira task creation
- Detailed action logging

✅ **Unified Dashboard**
- Clean, minimalist UI with card layout
- Metric cards with color-coded trends
- AI insights in chat-like format
- Action logs panel with detailed tracking

## Tech Stack

**Backend:**
- FastAPI (Python)
- MongoDB (database)
- Pandas (data processing)
- Emergentintegrations (Gemini 2.5 Pro integration)

**Frontend:**
- React 19
- Tailwind CSS
- Shadcn/UI components
- Axios (API calls)

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[Backend Documentation](BACKEND_DOCUMENTATION.md)** - Comprehensive API reference and features
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - What was built and how it works
- **[Test Script](test_backend.py)** - Automated testing suite

## Quick Start

### Prerequisites
- Python 3.8+ with pip
- MongoDB running on port 27017
- Valid Emergent API key

### Environment Variables

**Backend (.env):**
```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="growth_copilot_db"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY=sk-emergent-...
```

**Frontend (.env):**
```
REACT_APP_BACKEND_URL=https://saas-copilot.preview.emergentagent.com
```

## Usage

### 1. Upload Data Files

**Sample files are provided in `/app/sample_data/`:**
- `mixpanel_sample.csv` - Sample metrics data
- `moengage_sample.json` - Sample campaign data
- `jira_sample.csv` - Sample release notes

1. Navigate to the "Overview" tab
2. Click "Select File" for each data type
3. Choose the appropriate file
4. Click "Upload"

### 2. View Metric Anomalies

After uploading Mixpanel data:
- Anomalies are automatically detected
- Metric cards show current vs. previous values
- Color-coded indicators (green for increase, red for decrease)
- Platform and cohort badges

### 3. Generate AI Insights

1. Click "Analyze with AI" on any metric card
2. Wait for Gemini 2.5 Pro to generate insights
3. Navigate to "Insights" tab to view results
4. Insights include:
   - Probable cause of the metric change
   - Affected user segment
   - Recommended action

### 4. Trigger Actions

From the Insights tab:
- **Send Campaign**: Simulates MoEngage campaign creation
- **Create Jira Task**: Simulates Jira task creation
- View results in the "Actions" tab

### 5. Review Action Logs

1. Navigate to "Actions" tab
2. View detailed logs of all triggered actions
3. Each log includes:
   - Action type (MoEngage/Jira)
   - Status (success/failed)
   - Description
   - Detailed execution information

## API Endpoints

### Data Upload
- `POST /api/upload/mixpanel` - Upload Mixpanel CSV
- `POST /api/upload/moengage` - Upload MoEngage JSON
- `POST /api/upload/jira` - Upload Jira CSV

### Metrics & Insights
- `GET /api/metrics` - Get all detected anomalies
- `POST /api/analyze/{anomaly_id}` - Generate AI insight for metric
- `GET /api/insights` - Get all AI insights

### Actions
- `POST /api/action/trigger` - Trigger action (MoEngage/Jira)
- `GET /api/action-logs` - Get all action logs

### Utility
- `DELETE /api/reset` - Reset all data (for testing)

## Sample Data Format

### Mixpanel CSV
```csv
date,metric,value,platform,cohort
2025-09-30,activation_rate,0.42,android,tier2
2025-10-07,activation_rate,0.39,android,tier2
```

### MoEngage JSON
```json
[
  {
    "campaign_id": "c101",
    "name": "Welcome Campaign",
    "launch_date": "2025-10-01",
    "platform": "android",
    "target_segment": "tier2",
    "type": "push_notification",
    "status": "active"
  }
]
```

### Jira CSV
```csv
release_id,release_date,title,summary
1056,2025-10-02,Onboarding flow v2.4,Introduced new signup modal with phone verification
```

## Architecture

### Backend Flow
1. File upload → Parse CSV/JSON
2. Store in MongoDB collections
3. Detect anomalies (>5% change week-over-week)
4. On analysis request → Call Gemini 2.5 Pro
5. Generate structured insights
6. Store insights in database
7. Simulate action triggers with logging

### Frontend Flow
1. File upload component → POST to backend
2. Fetch metrics → Display metric cards
3. Click analyze → POST to backend
4. Fetch insights → Display in insight panel
5. Trigger action → POST to backend
6. View action logs → Display detailed logs

## Design Principles

✅ Minimalist dashboard with white background
✅ Card-based layout for better organization
✅ Color-coded indicators for quick insights
✅ Responsive design for all screen sizes
✅ Smooth transitions and micro-interactions
✅ Clear visual hierarchy with Space Grotesk and Inter fonts
✅ Accessible UI with proper ARIA labels and data-testids

## Testing

All interactive elements include `data-testid` attributes for testing:
- `dashboard-page` - Main dashboard container
- `upload-mixpanel` - Mixpanel upload component
- `metric-card-{metric_name}` - Individual metric cards
- `insight-panel-{metric}` - Insight panels
- `action-log-{index}` - Action log entries

## Notes

⚠️ **This is an MVP**: Actions are simulated (no actual API calls to MoEngage/Jira)
⚠️ **AI Analysis**: Uses Gemini 2.5 Pro via Emergent LLM key
⚠️ **Data Storage**: MongoDB collections are cleared on reset

## Future Enhancements

- Real MoEngage and Jira API integrations
- Slack webhook integration for daily summaries
- User authentication and multi-tenant support
- Historical trend visualization
- Scheduled analysis and alerts
- Export reports to PDF

## Support

For issues or questions, please refer to the Emergent platform documentation.

---

Built with ❤️ using Emergent AI Platform