from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import pandas as pd
import json
import io
import google.generativeai as genai

# Import AI Engine
from ai_engine import AIAnalysisEngine

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize AI Engine
ai_engine = AIAnalysisEngine(db)

# Create the main app without a prefix
app = FastAPI(title="NorthStar AI - Growth Analytics Platform")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define Models
class FileUploadResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_type: str
    filename: str
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    record_count: int
    status: str = "success"
    insights_generated: int = 0

class MetricAnomaly(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metric_name: str
    current_value: float
    previous_value: float
    change_percent: float
    platform: Optional[str] = None
    cohort: Optional[str] = None
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIInsight(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metric: str
    change: str
    probable_cause: str
    affected_segment: str
    recommended_action: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ActionLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str
    metric: str
    description: str
    status: str
    details: Optional[Dict[str, Any]] = None
    triggered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TriggerActionRequest(BaseModel):
    metric: str
    action_type: str
    insight_id: str

class QueryRequest(BaseModel):
    """Natural language query request"""
    query: str

class QueryResponse(BaseModel):
    """Response for natural language queries"""
    answer: str
    supporting_evidence: List[str]
    recommendations: List[str]
    confidence: str

class DataSummary(BaseModel):
    """Summary of uploaded data"""
    mixpanel_records: int
    jira_records: int
    moengage_records: int
    detected_anomalies: int
    generated_insights: int
    action_logs: int

# Background task for generating comprehensive insights
async def generate_insights_background():
    """Background task to generate comprehensive insights"""
    try:
        logger.info("Starting comprehensive insights generation...")
        
        # Add timeout protection
        import asyncio
        try:
            insights = await asyncio.wait_for(
                ai_engine.generate_comprehensive_insights(),
                timeout=120.0  # 2 minute timeout
            )
        except asyncio.TimeoutError:
            logger.error("Insights generation timed out after 120 seconds")
            return
        
        # Store insights
        stored_count = 0
        for insight in insights:
            if insight:  # Skip None insights
                # Check if insight already exists
                existing = await db.enhanced_insights.find_one({"id": insight['id']})
                if not existing:
                    await db.enhanced_insights.insert_one(insight)
                    stored_count += 1
        
        logger.info(f"Generated and stored {stored_count} new comprehensive insights")
        
    except Exception as e:
        logger.error(f"Background insights generation error: {str(e)}")

# Helper Functions
async def analyze_with_ai(metric_data: Dict, release_notes: List[Dict], campaign_data: List[Dict]) -> Dict:
    """Use Gemini API to analyze metric changes"""
    try:
        # Configure Gemini
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            return {
                "probable_cause": "Google API key not configured",
                "affected_segment": "All users",
                "recommended_action": "Configure GOOGLE_API_KEY in .env file"
            }
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Prepare context
        prompt = f"""
You are a growth analyst for a B2C app.

Given:
- Metric trend: {json.dumps(metric_data)}
- Release notes: {json.dumps(release_notes[:3])}
- Campaign summary: {json.dumps(campaign_data[:3])}

Explain:
1. Why this metric changed
2. Which user cohort was affected
3. One actionable recommendation

Respond ONLY with a JSON object in this exact format (no markdown, no extra text):
{{
  "probable_cause": "clear explanation",
  "affected_segment": "user segment",
  "recommended_action": "specific action"
}}
"""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            response_text = response_text.split('\n', 1)[1]
            response_text = response_text.rsplit('```', 1)[0]
            response_text = response_text.replace('json', '').strip()
        
        insight = json.loads(response_text)
        return insight
    except Exception as e:
        logger.error(f"AI analysis error: {str(e)}")
        return {
            "probable_cause": "Unable to determine cause automatically",
            "affected_segment": "All users",
            "recommended_action": "Manual investigation recommended"
        }

def detect_anomalies(df: pd.DataFrame) -> List[Dict]:
    """Detect week-over-week metric changes > 5%"""
    anomalies = []
    
    # Group by metric, platform, cohort
    for (metric, platform, cohort), group in df.groupby(['metric', 'platform', 'cohort']):
        sorted_group = group.sort_values('date')
        if len(sorted_group) >= 2:
            current = sorted_group.iloc[-1]['value']
            previous = sorted_group.iloc[-2]['value']
            
            if previous != 0:
                change_percent = ((current - previous) / previous) * 100
                
                if abs(change_percent) > 5:
                    anomalies.append({
                        'metric_name': metric,
                        'current_value': float(current),
                        'previous_value': float(previous),
                        'change_percent': float(change_percent),
                        'platform': platform,
                        'cohort': cohort
                    })
    
    return anomalies

# API Routes
@api_router.get("/")
async def root():
    return {
        "message": "NorthStar AI - Growth Analytics Platform",
        "version": "2.0",
        "features": [
            "Automatic anomaly detection",
            "AI-powered insights generation",
            "Release impact analysis",
            "Campaign correlation",
            "Segment performance tracking",
            "Natural language queries"
        ]
    }

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        await db.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "ai_engine": "ready"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@api_router.get("/summary", response_model=DataSummary)
async def get_data_summary():
    """Get summary of all uploaded data"""
    try:
        mixpanel_count = await db.mixpanel_data.count_documents({})
        jira_count = await db.jira_data.count_documents({})
        moengage_count = await db.moengage_data.count_documents({})
        anomalies_count = await db.metric_anomalies.count_documents({})
        insights_count = await db.ai_insights.count_documents({}) + await db.enhanced_insights.count_documents({})
        actions_count = await db.action_logs.count_documents({})
        
        return DataSummary(
            mixpanel_records=mixpanel_count,
            jira_records=jira_count,
            moengage_records=moengage_count,
            detected_anomalies=anomalies_count,
            generated_insights=insights_count,
            action_logs=actions_count
        )
    except Exception as e:
        logger.error(f"Summary error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/upload/mixpanel", response_model=FileUploadResponse)
async def upload_mixpanel(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Upload Mixpanel CSV export and trigger automatic insights generation"""
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        required_cols = ['date', 'metric', 'value', 'platform', 'cohort']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(status_code=400, detail=f"CSV must contain columns: {required_cols}")
        
        records = df.to_dict('records')
        for record in records:
            record['uploaded_at'] = datetime.now(timezone.utc).isoformat()
        await db.mixpanel_data.insert_many(records)
        
        anomalies = detect_anomalies(df)
        for anomaly in anomalies:
            anomaly['id'] = str(uuid.uuid4())
            anomaly['detected_at'] = datetime.now(timezone.utc).isoformat()
            await db.metric_anomalies.insert_one(anomaly)
        
        # Temporarily disabled background task to avoid hanging
        # if background_tasks:
        #     background_tasks.add_task(generate_insights_background)
        
        logger.info(f"Uploaded {len(records)} Mixpanel records, detected {len(anomalies)} anomalies")
        
        return FileUploadResponse(
            file_type="mixpanel",
            filename=file.filename,
            record_count=len(records),
            insights_generated=len(anomalies)
        )
    except Exception as e:
        logger.error(f"Mixpanel upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/upload/moengage", response_model=FileUploadResponse)
async def upload_moengage(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Upload MoEngage JSON and trigger automatic insights generation"""
    try:
        contents = await file.read()
        data = json.loads(contents)
        
        if not isinstance(data, list):
            data = [data]
        
        for record in data:
            record['uploaded_at'] = datetime.now(timezone.utc).isoformat()
        await db.moengage_data.insert_many(data)
        
        # Temporarily disabled background task to avoid hanging
        # if background_tasks:
        #     background_tasks.add_task(generate_insights_background)
        
        logger.info(f"Uploaded {len(data)} MoEngage records")
        
        return FileUploadResponse(
            file_type="moengage",
            filename=file.filename,
            record_count=len(data)
        )
    except Exception as e:
        logger.error(f"MoEngage upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/upload/jira", response_model=FileUploadResponse)
async def upload_jira(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Upload Jira CSV and trigger automatic insights generation"""
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        records = df.to_dict('records')
        for record in records:
            record['uploaded_at'] = datetime.now(timezone.utc).isoformat()
        await db.jira_data.insert_many(records)
        
        # Temporarily disabled background task to avoid hanging
        # if background_tasks:
        #     background_tasks.add_task(generate_insights_background)
        
        logger.info(f"Uploaded {len(records)} Jira records")
        
        return FileUploadResponse(
            file_type="jira",
            filename=file.filename,
            record_count=len(records)
        )
    except Exception as e:
        logger.error(f"Jira upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/metrics", response_model=List[MetricAnomaly])
async def get_metrics():
    """Get all detected metric anomalies"""
    anomalies = await db.metric_anomalies.find({}, {"_id": 0}).to_list(1000)
    
    for anomaly in anomalies:
        if isinstance(anomaly.get('detected_at'), str):
            anomaly['detected_at'] = datetime.fromisoformat(anomaly['detected_at'])
    
    return anomalies

@api_router.post("/analyze/{anomaly_id}", response_model=AIInsight)
async def analyze_metric(anomaly_id: str):
    """Trigger AI analysis for a specific metric anomaly"""
    try:
        # Get anomaly
        anomaly = await db.metric_anomalies.find_one({"id": anomaly_id}, {"_id": 0})
        if not anomaly:
            raise HTTPException(status_code=404, detail="Anomaly not found")
        
        # Get related data
        release_notes = await db.jira_data.find({}, {"_id": 0}).to_list(100)
        campaign_data = await db.moengage_data.find({}, {"_id": 0}).to_list(100)
        
        # AI Analysis
        insight = await analyze_with_ai(anomaly, release_notes, campaign_data)
        
        # Create insight record
        insight_record = AIInsight(
            metric=anomaly['metric_name'],
            change=f"{anomaly['change_percent']:+.1f}%",
            probable_cause=insight['probable_cause'],
            affected_segment=insight['affected_segment'],
            recommended_action=insight['recommended_action']
        )
        
        # Store insight
        insight_dict = insight_record.model_dump()
        insight_dict['created_at'] = insight_dict['created_at'].isoformat()
        await db.ai_insights.insert_one(insight_dict)
        
        return insight_record
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/insights", response_model=List[AIInsight])
async def get_insights():
    """Get all AI insights"""
    insights = await db.ai_insights.find({}, {"_id": 0}).to_list(1000)
    
    for insight in insights:
        if isinstance(insight.get('created_at'), str):
            insight['created_at'] = datetime.fromisoformat(insight['created_at'])
    
    return insights

@api_router.post("/action/trigger", response_model=ActionLog)
async def trigger_action(request: TriggerActionRequest):
    """Simulate triggering an action (MoEngage campaign or Jira task)"""
    try:
        # Get the insight
        insight = await db.ai_insights.find_one({"id": request.insight_id}, {"_id": 0})
        if not insight:
            raise HTTPException(status_code=404, detail="Insight not found")
        
        # Simulate action execution
        if request.action_type == "moengage":
            description = f"Campaign triggered for {request.metric}: {insight['recommended_action']}"
            details = {
                "campaign_name": f"Recovery Campaign - {request.metric}",
                "target_segment": insight['affected_segment'],
                "message": insight['recommended_action'],
                "platform": "MoEngage",
                "simulated": True
            }
        elif request.action_type == "jira":
            description = f"Jira task created for {request.metric}: Investigate {insight['probable_cause']}"
            details = {
                "task_title": f"Investigate {request.metric} decline",
                "description": insight['probable_cause'],
                "priority": "High",
                "assignee": "Growth Team",
                "platform": "Jira",
                "simulated": True
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid action type")
        
        # Create action log
        action_log = ActionLog(
            action_type=request.action_type,
            metric=request.metric,
            description=description,
            status="success",
            details=details
        )
        
        # Store action log
        log_dict = action_log.model_dump()
        log_dict['triggered_at'] = log_dict['triggered_at'].isoformat()
        await db.action_logs.insert_one(log_dict)
        
        return action_log
    except Exception as e:
        logger.error(f"Action trigger error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/action-logs", response_model=List[ActionLog])
async def get_action_logs():
    """Get all action logs"""
    logs = await db.action_logs.find({}, {"_id": 0}).sort("triggered_at", -1).to_list(1000)
    
    for log in logs:
        if isinstance(log.get('triggered_at'), str):
            log['triggered_at'] = datetime.fromisoformat(log['triggered_at'])
    
    return logs

@api_router.get("/insights/enhanced")
async def get_enhanced_insights():
    """Get all comprehensive AI-generated insights"""
    try:
        insights = await db.enhanced_insights.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
        return insights
    except Exception as e:
        logger.error(f"Enhanced insights error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/insights/generate")
async def trigger_insights_generation(background_tasks: BackgroundTasks):
    """Manually trigger comprehensive insights generation"""
    try:
        background_tasks.add_task(generate_insights_background)
        return {
            "status": "success",
            "message": "Insights generation started in background"
        }
    except Exception as e:
        logger.error(f"Trigger insights error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/query", response_model=QueryResponse)
async def natural_language_query(request: QueryRequest):
    """Answer natural language queries about the data"""
    try:
        logger.info(f"Processing query: {request.query}")
        result = await ai_engine.query_insights(request.query)
        
        return QueryResponse(
            answer=result.get('answer', 'Unable to generate answer'),
            supporting_evidence=result.get('supporting_evidence', []),
            recommendations=result.get('recommendations', []),
            confidence=result.get('confidence', 'low')
        )
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/reset")
async def reset_data():
    """Reset all data (for testing)"""
    await db.mixpanel_data.delete_many({})
    await db.moengage_data.delete_many({})
    await db.jira_data.delete_many({})
    await db.metric_anomalies.delete_many({})
    await db.ai_insights.delete_many({})
    await db.enhanced_insights.delete_many({})
    await db.action_logs.delete_many({})
    
    logger.info("All data cleared")
    
    return {"status": "success", "message": "All data cleared"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("MongoDB connection closed")