"""
AI Analysis Engine for NorthStar-AI
Provides advanced analytics, correlation analysis, and insights generation
Uses Google Gemini API directly
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import google.generativeai as genai
import json
import uuid
import os

logger = logging.getLogger(__name__)


class AIAnalysisEngine:
    """Advanced AI-powered analysis engine for growth metrics"""
    
    def __init__(self, db):
        self.db = db
        # Configure Gemini API
        api_key = os.environ.get('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            logger.warning("GOOGLE_API_KEY not found in environment variables")
            self.model = None
        
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API with retry logic"""
        try:
            if not self.model:
                return json.dumps({
                    "summary": "API key not configured",
                    "confidence": "low"
                })
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return json.dumps({
                "summary": f"Error: {str(e)}",
                "confidence": "low"
            })
        
    async def generate_comprehensive_insights(self) -> List[Dict]:
        """Generate comprehensive insights from all uploaded data"""
        try:
            # Get all data
            mixpanel_data = await self.db.mixpanel_data.find({}, {"_id": 0}).to_list(1000)
            jira_data = await self.db.jira_data.find({}, {"_id": 0}).to_list(1000)
            moengage_data = await self.db.moengage_data.find({}, {"_id": 0}).to_list(1000)
            
            if not mixpanel_data:
                return []
            
            # Convert to DataFrames
            df_mixpanel = pd.DataFrame(mixpanel_data)
            
            insights = []
            
            # 1. Metric Trend Analysis
            trend_insights = await self._analyze_metric_trends(df_mixpanel, jira_data, moengage_data)
            insights.extend(trend_insights)
            
            # 2. Correlation Analysis
            correlation_insights = await self._analyze_correlations(df_mixpanel, jira_data, moengage_data)
            insights.extend(correlation_insights)
            
            # 3. Segment Performance
            segment_insights = await self._analyze_segment_performance(df_mixpanel)
            insights.extend(segment_insights)
            
            # 4. Platform Comparison
            platform_insights = await self._compare_platforms(df_mixpanel)
            insights.extend(platform_insights)
            
            return insights
            
        except Exception as e:
            logger.error(f"Comprehensive insights generation error: {str(e)}")
            return []
    
    async def _analyze_metric_trends(self, df: pd.DataFrame, jira_data: List[Dict], moengage_data: List[Dict]) -> List[Dict]:
        """Analyze trends for each metric and correlate with releases/campaigns"""
        insights = []
        
        try:
            # Group by metric
            for metric_name in df['metric'].unique():
                metric_df = df[df['metric'] == metric_name].copy()
                metric_df['date'] = pd.to_datetime(metric_df['date'])
                metric_df = metric_df.sort_values('date')
                
                if len(metric_df) < 2:
                    continue
                
                # Calculate overall trend
                first_value = metric_df.iloc[0]['value']
                last_value = metric_df.iloc[-1]['value']
                change_percent = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
                
                # Find related releases and campaigns
                related_releases = self._find_temporal_correlations(
                    metric_df, jira_data, 'release_date'
                )
                related_campaigns = self._find_temporal_correlations(
                    metric_df, moengage_data, 'launch_date'
                )
                
                # Generate AI insight
                insight = await self._generate_trend_insight(
                    metric_name, change_percent, metric_df, 
                    related_releases, related_campaigns
                )
                
                if insight:
                    insights.append(insight)
        
        except Exception as e:
            logger.error(f"Trend analysis error: {str(e)}")
        
        return insights
    
    async def _analyze_correlations(self, df: pd.DataFrame, jira_data: List[Dict], moengage_data: List[Dict]) -> List[Dict]:
        """Find correlations between metrics, releases, and campaigns"""
        insights = []
        
        try:
            # Correlate releases with metric changes
            for release in jira_data:
                release_date = pd.to_datetime(release['release_date'])
                
                # Look for metric changes within 7 days after release
                after_release = df[
                    (pd.to_datetime(df['date']) >= release_date) & 
                    (pd.to_datetime(df['date']) <= release_date + timedelta(days=7))
                ]
                
                if len(after_release) > 0:
                    # Calculate impact
                    impact_summary = self._calculate_release_impact(df, release_date)
                    
                    if impact_summary:
                        insight = await self._generate_release_correlation_insight(
                            release, impact_summary
                        )
                        if insight:
                            insights.append(insight)
            
            # Correlate campaigns with metric changes
            for campaign in moengage_data:
                launch_date = pd.to_datetime(campaign['launch_date'])
                platform = campaign.get('platform')
                segment = campaign.get('target_segment')
                
                # Look for metric changes for this platform/segment
                campaign_impact = df[
                    (pd.to_datetime(df['date']) >= launch_date) & 
                    (pd.to_datetime(df['date']) <= launch_date + timedelta(days=7)) &
                    (df['platform'] == platform) &
                    (df['cohort'] == segment)
                ]
                
                if len(campaign_impact) > 0:
                    impact_summary = self._calculate_campaign_impact(df, campaign)
                    
                    if impact_summary:
                        insight = await self._generate_campaign_correlation_insight(
                            campaign, impact_summary
                        )
                        if insight:
                            insights.append(insight)
        
        except Exception as e:
            logger.error(f"Correlation analysis error: {str(e)}")
        
        return insights
    
    async def _analyze_segment_performance(self, df: pd.DataFrame) -> List[Dict]:
        """Analyze performance across different user segments"""
        insights = []
        
        try:
            # Group by cohort
            for cohort in df['cohort'].unique():
                cohort_df = df[df['cohort'] == cohort]
                
                # Calculate average performance
                avg_metrics = {}
                for metric in cohort_df['metric'].unique():
                    metric_values = cohort_df[cohort_df['metric'] == metric]['value']
                    avg_metrics[metric] = float(metric_values.mean())
                
                # Compare with other cohorts
                other_cohorts = df[df['cohort'] != cohort]
                comparison = {}
                
                for metric, avg_value in avg_metrics.items():
                    other_avg = other_cohorts[other_cohorts['metric'] == metric]['value'].mean()
                    if other_avg != 0:
                        diff_percent = ((avg_value - other_avg) / other_avg * 100)
                        comparison[metric] = float(diff_percent)
                
                if comparison:
                    insight = await self._generate_segment_insight(cohort, avg_metrics, comparison)
                    if insight:
                        insights.append(insight)
        
        except Exception as e:
            logger.error(f"Segment analysis error: {str(e)}")
        
        return insights
    
    async def _compare_platforms(self, df: pd.DataFrame) -> List[Dict]:
        """Compare performance across platforms"""
        insights = []
        
        try:
            # Group by platform
            platform_performance = {}
            
            for platform in df['platform'].unique():
                platform_df = df[df['platform'] == platform]
                metrics = {}
                
                for metric in platform_df['metric'].unique():
                    metric_values = platform_df[platform_df['metric'] == metric]['value']
                    metrics[metric] = {
                        'avg': float(metric_values.mean()),
                        'trend': self._calculate_trend(metric_values.tolist())
                    }
                
                platform_performance[platform] = metrics
            
            # Generate comparison insights
            insight = await self._generate_platform_comparison_insight(platform_performance)
            if insight:
                insights.append(insight)
        
        except Exception as e:
            logger.error(f"Platform comparison error: {str(e)}")
        
        return insights
    
    def _find_temporal_correlations(self, metric_df: pd.DataFrame, events: List[Dict], date_field: str) -> List[Dict]:
        """Find events that happened close to metric changes"""
        related = []
        
        for event in events:
            event_date = pd.to_datetime(event[date_field])
            
            # Check if any metric data point is within 7 days of this event
            close_dates = metric_df[
                (abs((metric_df['date'] - event_date).dt.days) <= 7)
            ]
            
            if len(close_dates) > 0:
                related.append(event)
        
        return related
    
    def _calculate_release_impact(self, df: pd.DataFrame, release_date: pd.Timestamp) -> Optional[Dict]:
        """Calculate the impact of a release on metrics"""
        try:
            before_release = df[pd.to_datetime(df['date']) < release_date]
            after_release = df[
                (pd.to_datetime(df['date']) >= release_date) & 
                (pd.to_datetime(df['date']) <= release_date + timedelta(days=7))
            ]
            
            if len(before_release) == 0 or len(after_release) == 0:
                return None
            
            impacts = {}
            for metric in df['metric'].unique():
                before_values = before_release[before_release['metric'] == metric]['value']
                after_values = after_release[after_release['metric'] == metric]['value']
                
                if len(before_values) > 0 and len(after_values) > 0:
                    before_avg = before_values.mean()
                    after_avg = after_values.mean()
                    
                    if before_avg != 0:
                        change = ((after_avg - before_avg) / before_avg * 100)
                        impacts[metric] = {
                            'change_percent': float(change),
                            'before': float(before_avg),
                            'after': float(after_avg)
                        }
            
            return impacts if impacts else None
            
        except Exception as e:
            logger.error(f"Release impact calculation error: {str(e)}")
            return None
    
    def _calculate_campaign_impact(self, df: pd.DataFrame, campaign: Dict) -> Optional[Dict]:
        """Calculate the impact of a campaign on metrics"""
        try:
            launch_date = pd.to_datetime(campaign['launch_date'])
            platform = campaign.get('platform')
            segment = campaign.get('target_segment')
            
            before_campaign = df[
                (pd.to_datetime(df['date']) < launch_date) &
                (df['platform'] == platform) &
                (df['cohort'] == segment)
            ]
            
            after_campaign = df[
                (pd.to_datetime(df['date']) >= launch_date) & 
                (pd.to_datetime(df['date']) <= launch_date + timedelta(days=7)) &
                (df['platform'] == platform) &
                (df['cohort'] == segment)
            ]
            
            if len(before_campaign) == 0 or len(after_campaign) == 0:
                return None
            
            impacts = {}
            for metric in df['metric'].unique():
                before_values = before_campaign[before_campaign['metric'] == metric]['value']
                after_values = after_campaign[after_campaign['metric'] == metric]['value']
                
                if len(before_values) > 0 and len(after_values) > 0:
                    before_avg = before_values.mean()
                    after_avg = after_values.mean()
                    
                    if before_avg != 0:
                        change = ((after_avg - before_avg) / before_avg * 100)
                        impacts[metric] = {
                            'change_percent': float(change),
                            'before': float(before_avg),
                            'after': float(after_avg)
                        }
            
            return impacts if impacts else None
            
        except Exception as e:
            logger.error(f"Campaign impact calculation error: {str(e)}")
            return None
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear regression slope
        x = list(range(len(values)))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.01:
            return "increasing"
        elif slope < -0.01:
            return "decreasing"
        else:
            return "stable"
    
    async def _generate_trend_insight(self, metric_name: str, change_percent: float, 
                                     metric_df: pd.DataFrame, related_releases: List[Dict], 
                                     related_campaigns: List[Dict]) -> Optional[Dict]:
        """Generate AI insight for metric trend"""
        try:
            prompt = f"""
Analyze this metric trend:

Metric: {metric_name}
Change: {change_percent:+.1f}%
Data points: {len(metric_df)}

Related releases (within 7 days):
{json.dumps(related_releases[:2], indent=2)}

Related campaigns (within 7 days):
{json.dumps(related_campaigns[:2], indent=2)}

Provide analysis in JSON format (no markdown, just JSON):
{{
  "insight_type": "trend_analysis",
  "metric": "{metric_name}",
  "summary": "brief summary of the trend",
  "probable_causes": ["cause 1", "cause 2"],
  "affected_segments": ["segment 1"],
  "recommendations": ["action 1", "action 2"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            
            # Parse response
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
                response_text = response_text.replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            
            return insight
            
        except Exception as e:
            logger.error(f"Trend insight generation error: {str(e)}")
            return None
    
    async def _generate_release_correlation_insight(self, release: Dict, impact_summary: Dict) -> Optional[Dict]:
        """Generate insight for release correlation"""
        try:
            prompt = f"""
Analyze the impact of this release:

Release: {release['title']}
Date: {release['release_date']}
Summary: {release['summary']}

Metric impacts (7 days after):
{json.dumps(impact_summary, indent=2)}

Provide analysis in JSON format (no markdown, just JSON):
{{
  "insight_type": "release_impact",
  "release_id": "{release['release_id']}",
  "summary": "overall impact summary",
  "positive_impacts": ["metric improvements"],
  "negative_impacts": ["metric declines"],
  "recommendations": ["actions to take"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
                response_text = response_text.replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            
            return insight
            
        except Exception as e:
            logger.error(f"Release correlation insight error: {str(e)}")
            return None
    
    async def _generate_campaign_correlation_insight(self, campaign: Dict, impact_summary: Dict) -> Optional[Dict]:
        """Generate insight for campaign correlation"""
        try:
            prompt = f"""
Analyze the impact of this campaign:

Campaign: {campaign['name']}
Type: {campaign['type']}
Launch Date: {campaign['launch_date']}
Platform: {campaign['platform']}
Target: {campaign['target_segment']}

Metric impacts (7 days after):
{json.dumps(impact_summary, indent=2)}

Provide analysis in JSON format (no markdown, just JSON):
{{
  "insight_type": "campaign_impact",
  "campaign_id": "{campaign['campaign_id']}",
  "summary": "campaign effectiveness summary",
  "effectiveness_score": 85,
  "key_learnings": ["learning 1", "learning 2"],
  "recommendations": ["future actions"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
                response_text = response_text.replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            
            return insight
            
        except Exception as e:
            logger.error(f"Campaign correlation insight error: {str(e)}")
            return None
    
    async def _generate_segment_insight(self, cohort: str, metrics: Dict, comparison: Dict) -> Optional[Dict]:
        """Generate insight for segment performance"""
        try:
            prompt = f"""
Analyze this user segment performance:

Segment: {cohort}
Average metrics: {json.dumps(metrics, indent=2)}
Comparison with other segments: {json.dumps(comparison, indent=2)}

Provide analysis in JSON format (no markdown, just JSON):
{{
  "insight_type": "segment_analysis",
  "segment": "{cohort}",
  "summary": "segment performance summary",
  "strengths": ["strong metric 1"],
  "weaknesses": ["weak metric 1"],
  "recommendations": ["targeted action 1"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
                response_text = response_text.replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            
            return insight
            
        except Exception as e:
            logger.error(f"Segment insight error: {str(e)}")
            return None
    
    async def _generate_platform_comparison_insight(self, platform_performance: Dict) -> Optional[Dict]:
        """Generate insight comparing platform performance"""
        try:
            prompt = f"""
Compare performance across platforms:

{json.dumps(platform_performance, indent=2)}

Provide analysis in JSON format (no markdown, just JSON):
{{
  "insight_type": "platform_comparison",
  "summary": "cross-platform performance summary",
  "best_performing_platform": "platform name",
  "areas_for_improvement": {{"platform": "metric"}},
  "recommendations": ["action 1", "action 2"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
                response_text = response_text.replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            
            return insight
            
        except Exception as e:
            logger.error(f"Platform comparison insight error: {str(e)}")
            return None
    
    async def query_insights(self, query: str) -> Dict:
        """Answer natural language queries about the data"""
        try:
            # Get all data
            mixpanel_data = await self.db.mixpanel_data.find({}, {"_id": 0}).to_list(1000)
            jira_data = await self.db.jira_data.find({}, {"_id": 0}).to_list(1000)
            moengage_data = await self.db.moengage_data.find({}, {"_id": 0}).to_list(1000)
            insights = await self.db.ai_insights.find({}, {"_id": 0}).to_list(1000)
            
            prompt = f"""
User question: {query}

Available data:
Mixpanel metrics: {json.dumps(mixpanel_data[:10], indent=2)}
Release notes: {json.dumps(jira_data, indent=2)}
Campaigns: {json.dumps(moengage_data, indent=2)}
Previous insights: {json.dumps(insights[:5], indent=2)}

Provide a comprehensive answer in JSON format (no markdown, just JSON):
{{
  "answer": "direct answer to the question",
  "supporting_evidence": ["data point 1", "data point 2"],
  "recommendations": ["action 1"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
                response_text = response_text.replace('json', '').strip()
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            logger.error(f"Query insights error: {str(e)}")
            return {
                "answer": "Unable to process query",
                "supporting_evidence": [],
                "recommendations": [],
                "confidence": "low",
                "error": str(e)
            }
