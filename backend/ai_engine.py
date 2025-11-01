"""
AI Analysis Engine for NorthStar-AI  
Simple, fast prompts for quick insights generation
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
    """AI-powered analysis engine for growth metrics"""
    
    def __init__(self, db):
        self.db = db
        api_key = os.environ.get('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        else:
            logger.warning("Google API key not found in environment variables")
            self.model = None
        
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        try:
            if not self.model:
                return json.dumps({"summary": "API key not configured", "confidence": "low"})
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return json.dumps({"summary": f"Error: {str(e)}", "confidence": "low"})
        
    async def generate_comprehensive_insights(self) -> List[Dict]:
        """Generate insights from all uploaded data - MAXIMUM PARALLELIZATION"""
        try:
            logger.info("Fetching data from MongoDB...")
            mixpanel_data = await self.db.mixpanel_data.find({}, {"_id": 0}).to_list(1000)
            jira_data = await self.db.jira_data.find({}, {"_id": 0}).to_list(1000)
            moengage_data = await self.db.moengage_data.find({}, {"_id": 0}).to_list(1000)
            
            if not mixpanel_data:
                logger.warning("No Mixpanel data found")
                return []
            
            logger.info(f"Processing {len(mixpanel_data)} metrics, {len(jira_data)} releases, {len(moengage_data)} campaigns")
            df_mixpanel = pd.DataFrame(mixpanel_data)
            
            # Collect ALL tasks upfront (maximum parallelization)
            all_tasks = []
            
            # Add trend analysis tasks (MOST IMPORTANT)
            for metric_name in df_mixpanel['metric'].unique():
                metric_df = df_mixpanel[df_mixpanel['metric'] == metric_name].copy()
                metric_df['date'] = pd.to_datetime(metric_df['date'])
                metric_df = metric_df.sort_values('date')
                
                if len(metric_df) < 2:
                    continue
                
                first_value = metric_df.iloc[0]['value']
                last_value = metric_df.iloc[-1]['value']
                change_percent = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
                
                # Only analyze metrics with significant changes to save time
                if abs(change_percent) < 5:
                    continue
                
                related_releases = self._find_temporal_correlations(metric_df, jira_data, 'release_date')
                related_campaigns = self._find_temporal_correlations(metric_df, moengage_data, 'launch_date')
                
                all_tasks.append(self._generate_trend_insight(metric_name, change_percent, metric_df, related_releases, related_campaigns))
            
            # Add release correlation tasks (only significant impacts)
            for release in jira_data[:3]:  # Limit to 3 most recent releases
                release_date = pd.to_datetime(release['release_date'])
                impact_summary = self._calculate_release_impact(df_mixpanel, release_date)
                if impact_summary and len(impact_summary) > 0:
                    # Only if release had measurable impact
                    avg_impact = sum(m['change_percent'] for m in impact_summary.values()) / len(impact_summary)
                    if abs(avg_impact) > 3:  # Only significant releases
                        all_tasks.append(self._generate_release_correlation_insight(release, impact_summary))
            
            # Add campaign correlation tasks (only significant impacts)
            for campaign in moengage_data[:3]:  # Limit to 3 most recent campaigns
                impact_summary = self._calculate_campaign_impact(df_mixpanel, campaign)
                if impact_summary and len(impact_summary) > 0:
                    # Only if campaign had measurable impact
                    avg_impact = sum(m['change_percent'] for m in impact_summary.values()) / len(impact_summary)
                    if abs(avg_impact) > 3:  # Only significant campaigns
                        all_tasks.append(self._generate_campaign_correlation_insight(campaign, impact_summary))
            
            logger.info(f"Running {len(all_tasks)} AI analyses in parallel...")
            
            # Run EVERYTHING in parallel at once!
            import asyncio
            results = await asyncio.gather(*all_tasks, return_exceptions=True)
            
            # Filter successful insights
            insights = [r for r in results if r and not isinstance(r, Exception)]
            logger.info(f"Successfully generated {len(insights)} insights (failed: {len(all_tasks) - len(insights)})")
            
            return insights
            
        except Exception as e:
            logger.error(f"Insights generation error: {str(e)}")
            return []
    
    async def _analyze_metric_trends(self, df: pd.DataFrame, jira_data: List[Dict], moengage_data: List[Dict]) -> List[Dict]:
        """Analyze metric trends - with parallel Gemini calls"""
        insights = []
        
        try:
            # Collect all metrics that need analysis
            metric_tasks = []
            
            for metric_name in df['metric'].unique():
                metric_df = df[df['metric'] == metric_name].copy()
                metric_df['date'] = pd.to_datetime(metric_df['date'])
                metric_df = metric_df.sort_values('date')
                
                if len(metric_df) < 2:
                    continue
                
                first_value = metric_df.iloc[0]['value']
                last_value = metric_df.iloc[-1]['value']
                change_percent = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
                
                related_releases = self._find_temporal_correlations(metric_df, jira_data, 'release_date')
                related_campaigns = self._find_temporal_correlations(metric_df, moengage_data, 'launch_date')
                
                # Add to parallel tasks
                metric_tasks.append(
                    self._generate_trend_insight(metric_name, change_percent, metric_df, related_releases, related_campaigns)
                )
            
            # Run all metric analyses in parallel
            if metric_tasks:
                import asyncio
                results = await asyncio.gather(*metric_tasks, return_exceptions=True)
                insights = [r for r in results if r and not isinstance(r, Exception)]
                
        except Exception as e:
            logger.error(f"Trend analysis error: {str(e)}")
        
        return insights
    
    async def _analyze_correlations(self, df: pd.DataFrame, jira_data: List[Dict], moengage_data: List[Dict]) -> List[Dict]:
        """Find correlations - with parallel Gemini calls"""
        insights = []
        
        try:
            correlation_tasks = []
            
            # Correlate releases
            for release in jira_data:
                release_date = pd.to_datetime(release['release_date'])
                after_release = df[
                    (pd.to_datetime(df['date']) >= release_date) & 
                    (pd.to_datetime(df['date']) <= release_date + timedelta(days=7))
                ]
                
                if len(after_release) > 0:
                    impact_summary = self._calculate_release_impact(df, release_date)
                    if impact_summary:
                        correlation_tasks.append(
                            self._generate_release_correlation_insight(release, impact_summary)
                        )
            
            # Correlate campaigns
            for campaign in moengage_data:
                launch_date = pd.to_datetime(campaign['launch_date'])
                platform = campaign.get('platform')
                segment = campaign.get('target_segment')
                
                campaign_impact = df[
                    (pd.to_datetime(df['date']) >= launch_date) & 
                    (pd.to_datetime(df['date']) <= launch_date + timedelta(days=7)) &
                    (df['platform'] == platform) &
                    (df['cohort'] == segment)
                ]
                
                if len(campaign_impact) > 0:
                    impact_summary = self._calculate_campaign_impact(df, campaign)
                    if impact_summary:
                        correlation_tasks.append(
                            self._generate_campaign_correlation_insight(campaign, impact_summary)
                        )
            
            # Run all correlation analyses in parallel
            if correlation_tasks:
                import asyncio
                results = await asyncio.gather(*correlation_tasks, return_exceptions=True)
                insights = [r for r in results if r and not isinstance(r, Exception)]
                
        except Exception as e:
            logger.error(f"Correlation analysis error: {str(e)}")
        
        return insights
    
    async def _analyze_segment_performance(self, df: pd.DataFrame) -> List[Dict]:
        """Analyze segment performance"""
        insights = []
        
        try:
            for cohort in df['cohort'].unique():
                cohort_df = df[df['cohort'] == cohort]
                
                avg_metrics = {}
                for metric in cohort_df['metric'].unique():
                    metric_values = cohort_df[cohort_df['metric'] == metric]['value']
                    avg_metrics[metric] = float(metric_values.mean())
                
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
        """Compare platforms"""
        insights = []
        
        try:
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
            
            insight = await self._generate_platform_comparison_insight(platform_performance)
            if insight:
                insights.append(insight)
        except Exception as e:
            logger.error(f"Platform comparison error: {str(e)}")
        
        return insights
    
    def _find_temporal_correlations(self, metric_df: pd.DataFrame, events: List[Dict], date_field: str) -> List[Dict]:
        """Find events close to metric changes"""
        related = []
        for event in events:
            event_date = pd.to_datetime(event[date_field])
            close_dates = metric_df[(abs((metric_df['date'] - event_date).dt.days) <= 7)]
            if len(close_dates) > 0:
                related.append(event)
        return related
    
    def _calculate_release_impact(self, df: pd.DataFrame, release_date: pd.Timestamp) -> Optional[Dict]:
        """Calculate release impact"""
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
        """Calculate campaign impact"""
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
        """Calculate trend direction"""
        if len(values) < 2:
            return "stable"
        x = list(range(len(values)))
        slope = np.polyfit(x, values, 1)[0]
        return "increasing" if slope > 0.01 else "decreasing" if slope < -0.01 else "stable"
    
    async def _generate_trend_insight(self, metric_name: str, change_percent: float, metric_df: pd.DataFrame, related_releases: List[Dict], related_campaigns: List[Dict]) -> Optional[Dict]:
        """Generate trend insight - SIMPLE VERSION"""
        try:
            prompt = f"""Analyze this metric:

Metric: {metric_name}
Change: {change_percent:+.1f}%

Related releases: {json.dumps(related_releases[:2], indent=2)}
Related campaigns: {json.dumps(related_campaigns[:2], indent=2)}

Provide JSON (no markdown):
{{
  "insight_type": "trend_analysis",
  "metric": "{metric_name}",
  "summary": "brief summary",
  "probable_causes": ["cause 1", "cause 2"],
  "affected_segments": ["segment"],
  "recommendations": ["action 1", "action 2"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1].rsplit('```', 1)[0].replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            return insight
        except Exception as e:
            logger.error(f"Trend insight error: {str(e)}")
            return None
    
    async def _generate_release_correlation_insight(self, release: Dict, impact_summary: Dict) -> Optional[Dict]:
        """Generate release insight - SIMPLE VERSION"""
        try:
            prompt = f"""Analyze release impact:

Release: {release['title']}
Date: {release['release_date']}
Summary: {release['summary']}

Metric impacts: {json.dumps(impact_summary, indent=2)}

Provide JSON (no markdown):
{{
  "insight_type": "release_impact",
  "release_id": "{release['release_id']}",
  "summary": "impact summary",
  "positive_impacts": ["improvement 1"],
  "negative_impacts": ["decline 1"],
  "recommendations": ["action 1"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1].rsplit('```', 1)[0].replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            return insight
        except Exception as e:
            logger.error(f"Release insight error: {str(e)}")
            return None
    
    async def _generate_campaign_correlation_insight(self, campaign: Dict, impact_summary: Dict) -> Optional[Dict]:
        """Generate campaign insight - SIMPLE VERSION"""
        try:
            prompt = f"""Analyze campaign:

Campaign: {campaign['name']}
Type: {campaign['type']}
Platform: {campaign['platform']}
Target: {campaign['target_segment']}

Metric impacts: {json.dumps(impact_summary, indent=2)}

Provide JSON (no markdown):
{{
  "insight_type": "campaign_impact",
  "campaign_id": "{campaign['campaign_id']}",
  "summary": "campaign effectiveness",
  "effectiveness_score": 0-100,
  "key_learnings": ["learning 1"],
  "recommendations": ["action 1"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1].rsplit('```', 1)[0].replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            return insight
        except Exception as e:
            logger.error(f"Campaign insight error: {str(e)}")
            return None
    
    async def _generate_segment_insight(self, cohort: str, metrics: Dict, comparison: Dict) -> Optional[Dict]:
        """Generate segment insight - SIMPLE VERSION"""
        try:
            prompt = f"""Analyze segment:

Segment: {cohort}
Metrics: {json.dumps(metrics, indent=2)}
vs Others: {json.dumps(comparison, indent=2)}

Provide JSON (no markdown):
{{
  "insight_type": "segment_analysis",
  "segment": "{cohort}",
  "summary": "segment performance",
  "strengths": ["strength 1"],
  "weaknesses": ["weakness 1"],
  "recommendations": ["action 1"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1].rsplit('```', 1)[0].replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            return insight
        except Exception as e:
            logger.error(f"Segment insight error: {str(e)}")
            return None
    
    async def _generate_platform_comparison_insight(self, platform_performance: Dict) -> Optional[Dict]:
        """Generate platform insight - SIMPLE VERSION"""
        try:
            prompt = f"""Compare platforms:

{json.dumps(platform_performance, indent=2)}

Provide JSON (no markdown):
{{
  "insight_type": "platform_comparison",
  "summary": "platform comparison",
  "best_performing_platform": "platform name",
  "areas_for_improvement": {{"platform": "metric"}},
  "recommendations": ["action 1"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1].rsplit('```', 1)[0].replace('json', '').strip()
            
            insight = json.loads(response_text)
            insight['id'] = str(uuid.uuid4())
            insight['created_at'] = datetime.utcnow().isoformat()
            return insight
        except Exception as e:
            logger.error(f"Platform insight error: {str(e)}")
            return None
    
    async def query_insights(self, query: str) -> Dict:
        """Answer queries - SIMPLE VERSION"""
        try:
            mixpanel_data = await self.db.mixpanel_data.find({}, {"_id": 0}).to_list(1000)
            jira_data = await self.db.jira_data.find({}, {"_id": 0}).to_list(1000)
            moengage_data = await self.db.moengage_data.find({}, {"_id": 0}).to_list(1000)
            insights = await self.db.ai_insights.find({}, {"_id": 0}).to_list(1000)
            
            prompt = f"""User question: {query}

Data:
Metrics: {json.dumps(mixpanel_data[:10], indent=2)}
Releases: {json.dumps(jira_data, indent=2)}
Campaigns: {json.dumps(moengage_data, indent=2)}
Insights: {json.dumps(insights[:5], indent=2)}

Provide JSON (no markdown). Recommendations MUST be simple strings, not objects:
{{
  "answer": "direct answer with specifics",
  "supporting_evidence": ["data point 1", "data point 2"],
  "recommendations": ["action 1 as simple string", "action 2 as simple string"],
  "confidence": "high/medium/low"
}}
"""
            
            response_text = await self._call_gemini(prompt)
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1].rsplit('```', 1)[0].replace('json', '').strip()
            
            result = json.loads(response_text)
            
            # Ensure recommendations are strings
            if 'recommendations' in result and result['recommendations']:
                result['recommendations'] = [
                    rec if isinstance(rec, str) else rec.get('action', str(rec))
                    for rec in result['recommendations']
                ]
            
            return result
        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            return {
                "answer": "Unable to process query",
                "supporting_evidence": [],
                "recommendations": [],
                "confidence": "low",
                "error": str(e)
            }
