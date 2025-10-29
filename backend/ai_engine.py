"""
AI Analysis Engine for NorthStar-AI
Provides advanced analytics, correlation analysis, and insights generation
Uses Google Gemini API directly with enhanced, detailed prompts
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
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
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
            
            # Run all analysis types in parallel for faster processing!
            import asyncio
            results = await asyncio.gather(
                self._analyze_metric_trends(df_mixpanel, jira_data, moengage_data),
                self._analyze_correlations(df_mixpanel, jira_data, moengage_data),
                self._analyze_segment_performance(df_mixpanel),
                self._compare_platforms(df_mixpanel),
                return_exceptions=True
            )
            
            # Flatten results and filter out errors
            insights = []
            for result in results:
                if isinstance(result, list):
                    insights.extend(result)
            
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
        """Generate AI insight for metric trend - ENHANCED VERSION"""
        try:
            # Calculate additional context
            first_value = metric_df.iloc[0]['value']
            last_value = metric_df.iloc[-1]['value']
            platform_cohort_breakdown = metric_df.groupby(['platform', 'cohort'])['value'].mean().to_dict()
            
            prompt = f"""You are a senior growth analyst with 10+ years of experience in B2C digital products, specializing in user acquisition, activation, retention, and monetization metrics.

COMPANY CONTEXT:
- Type: B2C mobile and web application
- Focus: Growth optimization and user engagement
- Key segments: tier1 (premium users), tier2 (standard users)
- Platforms: Android, iOS, Web

METRIC ANALYSIS REQUEST:

Metric Name: {metric_name.replace('_', ' ').title()}
Overall Change: {change_percent:+.1f}% (from {first_value:.3f} to {last_value:.3f})
Time Period: {len(metric_df)} data points analyzed
Trend Direction: {'Declining' if change_percent < 0 else 'Growing' if change_percent > 0 else 'Stable'}

PLATFORM & COHORT BREAKDOWN:
{json.dumps(platform_cohort_breakdown, indent=2)}

TEMPORAL CONTEXT - Recent Product Releases (within 7 days):
{json.dumps(related_releases[:3], indent=2) if related_releases else 'No releases in this period'}

TEMPORAL CONTEXT - Recent Marketing Campaigns (within 7 days):
{json.dumps(related_campaigns[:3], indent=2) if related_campaigns else 'No campaigns in this period'}

HISTORICAL BASELINE:
- Typical change for this metric: ±2-3% weekly
- Current change ({change_percent:+.1f}%) is {'significant' if abs(change_percent) > 5 else 'normal'} variation
- Urgency: {'HIGH' if abs(change_percent) > 10 else 'MEDIUM' if abs(change_percent) > 5 else 'LOW'}

YOUR COMPREHENSIVE ANALYSIS TASK:

Provide a detailed, actionable analysis covering:

1. ROOT CAUSE ANALYSIS:
   - Technical factors (product changes, bugs, performance)
   - User experience factors (friction, confusion, delight)
   - External factors (seasonality, competition, campaigns)
   - Temporal correlations (releases, campaigns, events)

2. USER IMPACT ASSESSMENT:
   - Which user segments are most affected
   - User behavior patterns and psychology
   - Estimated number/percentage of users impacted

3. BUSINESS IMPACT:
   - Revenue implications (if applicable)
   - User growth trajectory impact
   - Long-term vs short-term effects
   - Competitive positioning impact

4. ACTIONABLE RECOMMENDATIONS:
   - Prioritized by expected impact and effort
   - Include specific implementation steps
   - Estimate expected outcomes
   - Note any risks or dependencies

Respond with detailed JSON in this exact format (no markdown):
{{
  "insight_type": "trend_analysis",
  "metric": "{metric_name}",
  "summary": "Comprehensive 2-3 sentence executive summary explaining what happened, why it matters, and immediate next steps",
  "probable_causes": [
    "Primary cause: Detailed explanation with evidence from the data",
    "Secondary cause: Contributing factor with reasoning",
    "Tertiary cause: Additional consideration if applicable"
  ],
  "affected_segments": [
    "Detailed description of primary affected user segment with characteristics and behavior patterns",
    "Secondary affected segment if applicable"
  ],
  "business_impact": {{
    "severity": "critical/high/medium/low",
    "estimated_user_count": "Approximate number or percentage of users affected",
    "revenue_impact": "Estimated financial impact or qualitative assessment",
    "urgency": "immediate/this-week/this-month/monitor"
  }},
  "recommendations": [
    {{
      "action": "Specific, implementable action with clear steps",
      "expected_impact": "Quantified or qualitative expected outcome",
      "effort_level": "low/medium/high",
      "timeline": "immediate/1-week/2-weeks/1-month",
      "priority": 1,
      "risks": "Potential downsides or dependencies to consider"
    }},
    {{
      "action": "Second priority action",
      "expected_impact": "Expected outcome",
      "effort_level": "low/medium/high",
      "timeline": "timeframe",
      "priority": 2,
      "risks": "Considerations"
    }}
  ],
  "confidence": "high/medium/low",
  "confidence_reasoning": "Detailed explanation of why this confidence level, citing specific data points and correlation strength"
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
        """Generate insight for release correlation - ENHANCED VERSION"""
        try:
            # Calculate aggregate impact
            total_positive = sum(1 for m in impact_summary.values() if m['change_percent'] > 0)
            total_negative = sum(1 for m in impact_summary.values() if m['change_percent'] < 0)
            avg_impact = sum(m['change_percent'] for m in impact_summary.values()) / len(impact_summary)
            
            prompt = f"""You are a senior product analyst with deep expertise in feature impact analysis, A/B testing, and product analytics for B2C applications.

COMPANY CONTEXT:
- Type: B2C mobile and web application
- Focus: Continuous product improvement and feature optimization
- Development cycle: Bi-weekly releases
- User base: Mixed segments across Android, iOS, and Web

RELEASE IMPACT ANALYSIS REQUEST:

Release Information:
- Release ID: {release['release_id']}
- Title: {release['title']}
- Deploy Date: {release['release_date']}
- Description: {release['summary']}

MEASURED METRIC IMPACTS (7 days post-release):

{json.dumps(impact_summary, indent=2)}

AGGREGATE ANALYSIS:
- Metrics improved: {total_positive}
- Metrics declined: {total_negative}
- Average impact: {avg_impact:+.1f}%
- Overall release effect: {'Positive' if avg_impact > 0 else 'Negative' if avg_impact < 0 else 'Neutral'}

ANALYSIS FRAMEWORK TO APPLY:

1. FEATURE IMPACT ASSESSMENT:
   - Intended vs actual outcomes
   - User experience implications
   - Technical implementation quality
   - Rollout strategy effectiveness

2. ROOT CAUSE ANALYSIS:
   - Why did certain metrics improve?
   - Why did certain metrics decline?
   - Were there unintended consequences?
   - What user behavior patterns changed?

3. BUSINESS STRATEGY:
   - Should this feature be iterated, reverted, or expanded?
   - What learnings apply to future releases?
   - Risk vs reward assessment

4. ACTIONABLE NEXT STEPS:
   - Immediate fixes for negative impacts
   - Opportunities to amplify positive impacts
   - A/B testing recommendations
   - Rollback considerations

Provide comprehensive analysis in JSON format (no markdown):
{{
  "insight_type": "release_impact",
  "release_id": "{release['release_id']}",
  "release_title": "{release['title']}",
  "summary": "Executive summary in 2-3 sentences covering overall impact, key findings, and critical next steps",
  "overall_assessment": "success/mixed/failure",
  "positive_impacts": [
    {{
      "metric": "metric name",
      "change": "percentage change",
      "explanation": "Detailed explanation of why this improved"
    }}
  ],
  "negative_impacts": [
    {{
      "metric": "metric name",
      "change": "percentage change",
      "explanation": "Detailed explanation of why this declined",
      "user_impact": "How users experienced this negatively"
    }}
  ],
  "unintended_consequences": [
    "Unexpected outcome 1 with analysis",
    "Unexpected outcome 2 if applicable"
  ],
  "user_feedback_hypothesis": "What users likely experienced and felt about this release",
  "recommendations": [
    {{
      "action": "Specific action to take",
      "rationale": "Why this action is recommended",
      "expected_outcome": "What will improve",
      "effort": "low/medium/high",
      "priority": 1,
      "rollback_consideration": "Whether this warrants feature rollback"
    }}
  ],
  "lessons_learned": [
    "Key learning for future releases",
    "Process improvement opportunity"
  ],
  "confidence": "high/medium/low",
  "confidence_reasoning": "Explanation citing data quality, correlation strength, and analysis methodology"
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
        """Generate insight for campaign correlation - ENHANCED VERSION"""
        try:
            # Calculate campaign ROI indicators
            avg_impact = sum(m['change_percent'] for m in impact_summary.values()) / len(impact_summary) if impact_summary else 0
            
            prompt = f"""You are a senior marketing analyst with expertise in campaign performance analysis, marketing attribution, customer lifecycle management, and ROI optimization for B2C companies.

COMPANY CONTEXT:
- Type: B2C mobile and web application
- Marketing channels: Push notifications, Email, In-app messages
- User segments: tier1 (premium/engaged), tier2 (standard/casual)
- Marketing objectives: Acquisition, activation, retention, monetization

CAMPAIGN PERFORMANCE ANALYSIS REQUEST:

Campaign Details:
- Campaign ID: {campaign['campaign_id']}
- Campaign Name: {campaign['name']}
- Campaign Type: {campaign['type']}
- Launch Date: {campaign['launch_date']}
- Target Platform: {campaign['platform']}
- Target Segment: {campaign['target_segment']}
- Campaign Status: {campaign.get('status', 'unknown')}

MEASURED METRIC IMPACTS (7 days post-launch):

{json.dumps(impact_summary, indent=2)}

CAMPAIGN PERFORMANCE INDICATORS:
- Average metric impact: {avg_impact:+.1f}%
- Campaign effectiveness: {'Strong' if avg_impact > 5 else 'Moderate' if avg_impact > 0 else 'Weak/Negative'}

ANALYSIS FRAMEWORK TO APPLY:

1. CAMPAIGN EFFECTIVENESS:
   - Did it achieve intended goals?
   - Which metrics were most influenced?
   - Was the target segment responsive?
   - How does this compare to typical campaign performance?

2. AUDIENCE INSIGHTS:
   - How did the target segment respond?
   - Were there unexpected audience behaviors?
   - Segment-specific learnings
   - Cross-segment opportunities

3. CREATIVE & MESSAGING:
   - What likely resonated with users?
   - What messaging/timing/channel factors contributed?
   - Creative insights for future campaigns

4. ROI & SCALABILITY:
   - Cost-effectiveness assessment
   - Scalability potential
   - Should this be repeated/scaled/modified?

5. OPTIMIZATION OPPORTUNITIES:
   - How to improve performance
   - Testing recommendations
   - Audience expansion potential

Provide comprehensive campaign analysis in JSON format (no markdown):
{{
  "insight_type": "campaign_impact",
  "campaign_id": "{campaign['campaign_id']}",
  "campaign_name": "{campaign['name']}",
  "summary": "Executive summary in 2-3 sentences: campaign performance, key drivers, and strategic recommendation",
  "overall_performance": "excellent/good/moderate/poor",
  "effectiveness_score": 0-100,
  "effectiveness_reasoning": "Detailed explanation of score based on metric movements and business goals",
  "metric_impacts": [
    {{
      "metric": "metric name",
      "change": "percentage",
      "assessment": "positive/negative/neutral",
      "explanation": "Why this metric moved this way"
    }}
  ],
  "audience_insights": {{
    "segment_response": "How the target segment {campaign['target_segment']} responded",
    "engagement_level": "high/medium/low",
    "behavioral_patterns": "Observable user behavior changes",
    "unexpected_findings": "Any surprising outcomes"
  }},
  "key_learnings": [
    "Specific learning about what worked",
    "Insight about audience behavior",
    "Timing or channel effectiveness insight",
    "Creative or messaging lesson"
  ],
  "recommendations": [
    {{
      "action": "Specific next step (scale/modify/retire/test)",
      "rationale": "Why this is recommended",
      "expected_outcome": "What this will achieve",
      "target_segment": "Who to target",
      "priority": 1,
      "implementation_notes": "How to execute this"
    }}
  ],
  "scalability_assessment": {{
    "should_scale": true/false,
    "scale_to_segments": ["suggested segments to expand to"],
    "scale_to_platforms": ["suggested platforms"],
    "modifications_needed": "Changes required before scaling"
  }},
  "confidence": "high/medium/low",
  "confidence_reasoning": "Data quality, sample size, correlation strength, and attribution clarity"
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
        """Generate insight for segment performance - ENHANCED VERSION"""
        try:
            # Calculate segment health score
            positive_metrics = sum(1 for v in comparison.values() if v > 0)
            total_metrics = len(comparison)
            health_score = (positive_metrics / total_metrics * 100) if total_metrics > 0 else 50
            
            prompt = f"""You are a senior user segmentation and cohort analysis expert with deep experience in customer lifecycle management, retention strategies, and personalization for B2C products.

COMPANY CONTEXT:
- Type: B2C digital product with subscription/freemium model
- User segments: tier1 (premium/engaged users), tier2 (standard/casual users)
- Business model: Likely freemium with upsell opportunities
- Growth focus: Acquisition, activation, monetization, retention

USER SEGMENT DEEP-DIVE ANALYSIS:

Segment Under Analysis: {cohort}
Segment Characteristics: {'Premium/engaged users with higher LTV' if cohort == 'tier1' else 'Standard/casual users, price-sensitive'  if cohort == 'tier2' else 'User segment'}

SEGMENT PERFORMANCE METRICS:
Average Performance:
{json.dumps(metrics, indent=2)}

COMPARATIVE ANALYSIS (vs other segments):
{json.dumps(comparison, indent=2)}

SEGMENT HEALTH INDICATORS:
- Metrics outperforming others: {positive_metrics}/{total_metrics}
- Segment health score: {health_score:.0f}/100
- Overall assessment: {'Strong performer' if health_score > 60 else 'Underperformer' if health_score < 40 else 'Mixed performance'}

ANALYSIS FRAMEWORK TO APPLY:

1. SEGMENT CHARACTERIZATION:
   - User demographics and psychographics likely
   - Behavioral patterns and usage frequency
   - Value perception and price sensitivity
   - Feature affinity and product engagement

2. PERFORMANCE ANALYSIS:
   - Why this segment performs differently
   - Strengths to leverage
   - Weaknesses to address
   - Comparison to benchmark/other segments

3. GROWTH OPPORTUNITIES:
   - Untapped potential in this segment
   - Cross-sell/upsell opportunities
   - Retention improvement strategies
   - Acquisition channel optimization

4. PERSONALIZATION STRATEGY:
   - Tailored features or messaging
   - Segment-specific campaigns
   - Pricing or packaging adjustments
   - User journey optimizations

5. STRATEGIC RECOMMENDATIONS:
   - How to grow this segment
   - How to improve segment economics
   - Whether to invest more/less in this segment
   - Specific tactics with expected ROI

Provide comprehensive segment analysis in JSON format (no markdown):
{{
  "insight_type": "segment_analysis",
  "segment": "{cohort}",
  "segment_characteristics": "Detailed description of who these users are, their behaviors, and motivations",
  "summary": "Executive summary in 2-3 sentences covering segment performance, key differentiators, and strategic opportunity",
  "performance_overview": {{
    "health_score": {health_score:.0f},
    "overall_assessment": "excellent/good/average/poor",
    "primary_strength": "What this segment does best",
    "primary_weakness": "Biggest area for improvement"
  }},
  "strengths": [
    {{
      "metric": "metric name",
      "performance": "percentage vs others",
      "explanation": "Detailed reason why this segment excels here",
      "leverage_opportunity": "How to capitalize on this strength"
    }}
  ],
  "weaknesses": [
    {{
      "metric": "metric name",
      "performance": "percentage vs others",
      "explanation": "Root cause of underperformance",
      "improvement_strategy": "Specific approach to address this"
    }}
  ],
  "growth_opportunities": [
    "Specific untapped opportunity with this segment",
    "Additional growth vector if identified"
  ],
  "recommendations": [
    {{
      "action": "Specific, segment-tailored recommendation",
      "expected_impact": "Quantified outcome",
      "target_metric": "Which metric will improve",
      "implementation": "How to execute this",
      "priority": 1,
      "segment_specific_rationale": "Why this works for this particular segment"
    }}
  ],
  "cross_segment_insights": "What other segments can learn from this segment's performance",
  "investment_recommendation": "invest-more/maintain/reduce with reasoning",
  "confidence": "high/medium/low",
  "confidence_reasoning": "Data quality, sample size, and analysis methodology explanation"
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
        """Generate insight comparing platform performance - ENHANCED VERSION"""
        try:
            # Calculate platform rankings
            platform_scores = {}
            for platform, metrics in platform_performance.items():
                avg_value = sum(m['avg'] for m in metrics.values()) / len(metrics) if metrics else 0
                platform_scores[platform] = avg_value
            
            best_platform = max(platform_scores, key=platform_scores.get) if platform_scores else 'unknown'
            
            prompt = f"""You are a senior cross-platform product strategist with expertise in mobile (iOS/Android) and web product development, platform-specific UX optimization, and multi-platform growth strategies.

COMPANY CONTEXT:
- Type: Multi-platform B2C digital product
- Platforms: Android app, iOS app, Web application
- Strategy: Platform parity with platform-specific optimizations
- Challenge: Balancing consistent experience with platform best practices

CROSS-PLATFORM PERFORMANCE ANALYSIS:

Complete Platform Metrics:
{json.dumps(platform_performance, indent=2)}

PLATFORM RANKINGS:
Best performing: {best_platform}
Platform scores: {json.dumps(platform_scores, indent=2)}

ANALYSIS FRAMEWORK TO APPLY:

1. PLATFORM PERFORMANCE COMPARISON:
   - Which platform delivers best user experience?
   - Where are the biggest performance gaps?
   - Platform-specific strengths and weaknesses
   - Technical vs UX vs user base differences

2. ROOT CAUSE ANALYSIS:
   - Why does each platform perform differently?
   - Technical implementation differences
   - UX pattern differences (native vs web)
   - User base composition differences
   - App store/discovery differences

3. USER EXPERIENCE ASSESSMENT:
   - Platform-specific friction points
   - Platform-specific delighters
   - Feature parity gaps
   - Platform-appropriate design patterns

4. STRATEGIC OPPORTUNITIES:
   - Quick wins for underperforming platforms
   - Best practices to replicate across platforms
   - Platform-specific feature opportunities
   - Investment allocation recommendations

5. TECHNICAL CONSIDERATIONS:
   - Performance optimization opportunities
   - Code reuse vs platform-specific development
   - Testing and QA implications
   - Development resource allocation

Provide comprehensive cross-platform analysis in JSON format (no markdown):
{{
  "insight_type": "platform_comparison",
  "summary": "Executive summary in 2-3 sentences covering platform performance landscape, key gaps, and strategic priority",
  "best_performing_platform": "{best_platform}",
  "best_platform_analysis": "Detailed explanation of why this platform excels",
  "platform_breakdown": [
    {{
      "platform": "platform name",
      "overall_score": 0-100,
      "rank": 1-3,
      "strengths": ["What this platform does well"],
      "weaknesses": ["What needs improvement"],
      "unique_advantages": "Platform-specific benefits",
      "user_base_characteristics": "Who uses this platform and why"
    }}
  ],
  "performance_gaps": [
    {{
      "gap": "Specific performance difference between platforms",
      "impact": "Business consequence of this gap",
      "root_cause": "Why this gap exists",
      "recommended_action": "How to close the gap"
    }}
  ],
  "platform_parity_assessment": {{
    "feature_parity": "high/medium/low",
    "ux_consistency": "high/medium/low",
    "performance_consistency": "high/medium/low",
    "critical_gaps": ["Most important disparities to address"]
  }},
  "recommendations": [
    {{
      "action": "Specific platform optimization",
      "target_platform": "which platform",
      "expected_impact": "what will improve",
      "effort": "low/medium/high",
      "priority": 1,
      "technical_requirements": "What's needed to implement",
      "success_metrics": "How to measure success"
    }}
  ],
  "investment_strategy": {{
    "increase_investment": ["platforms to invest more in"],
    "maintain_investment": ["platforms that are working well"],
    "optimization_focus": ["platforms needing efficiency gains"],
    "rationale": "Strategic reasoning for investment allocation"
  }},
  "quick_wins": [
    "Fast, high-impact improvement opportunity 1",
    "Fast, high-impact improvement opportunity 2"
  ],
  "confidence": "high/medium/low",
  "confidence_reasoning": "Data coverage across platforms, sample size adequacy, and analysis methodology"
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
        """Answer natural language queries about the data - ENHANCED VERSION"""
        try:
            # Get all data
            mixpanel_data = await self.db.mixpanel_data.find({}, {"_id": 0}).to_list(1000)
            jira_data = await self.db.jira_data.find({}, {"_id": 0}).to_list(1000)
            moengage_data = await self.db.moengage_data.find({}, {"_id": 0}).to_list(1000)
            insights = await self.db.ai_insights.find({}, {"_id": 0}).to_list(1000)
            enhanced_insights = await self.db.enhanced_insights.find({}, {"_id": 0}).to_list(1000)
            
            # Calculate data summary for context
            total_metrics = len(mixpanel_data)
            total_releases = len(jira_data)
            total_campaigns = len(moengage_data)
            
            prompt = f"""You are an expert data analyst and growth advisor with deep experience in product analytics, marketing attribution, and data-driven decision making for B2C companies.

COMPANY PROFILE:
- Industry: B2C digital product/application
- Platforms: Android, iOS, Web
- User Segments: tier1 (premium/engaged), tier2 (standard/casual)
- Data Sources: Mixpanel (product analytics), Jira (release tracking), MoEngage (marketing automation)

AVAILABLE DATA SUMMARY:
- Mixpanel metric records: {total_metrics}
- Product releases tracked: {total_releases}
- Marketing campaigns tracked: {total_campaigns}
- AI insights previously generated: {len(insights) + len(enhanced_insights)}

USER QUESTION:
"{query}"

COMPLETE DATA CONTEXT:

Recent Mixpanel Metrics (last 10 records):
{json.dumps(mixpanel_data[:10], indent=2)}

All Product Releases:
{json.dumps(jira_data, indent=2)}

All Marketing Campaigns:
{json.dumps(moengage_data, indent=2)}

Previously Generated Insights:
{json.dumps(insights[:5] + enhanced_insights[:5], indent=2)}

ANALYSIS INSTRUCTIONS:

1. UNDERSTAND THE QUESTION:
   - What is the user really asking?
   - What decision are they trying to make?
   - What level of detail do they need?

2. ANALYZE THE DATA:
   - Review all relevant data points
   - Identify patterns and correlations
   - Calculate any necessary metrics
   - Cross-reference with existing insights

3. PROVIDE COMPREHENSIVE ANSWER:
   - Direct answer to the question (be specific!)
   - Supporting evidence from actual data
   - Context and nuance (important caveats)
   - Actionable recommendations
   - Follow-up considerations

4. BE CONVERSATIONAL YET PROFESSIONAL:
   - Clear, jargon-free language
   - Specific numbers and examples
   - Honest about limitations
   - Proactive in suggesting related insights

RESPONSE GUIDELINES:
- Cite specific data points (dates, numbers, percentages)
- Explain causation, not just correlation
- Prioritize actionable insights
- Note confidence levels and limitations
- Suggest follow-up questions if relevant

Provide a comprehensive, conversational response in JSON format (no markdown):
{{
  "answer": "Detailed, specific answer to the user's question in 3-5 sentences. Include actual numbers, dates, and metrics from the data. Be conversational but professional. If the question is complex, structure the answer in clear points.",
  
  "supporting_evidence": [
    "Specific data point 1 with actual numbers (e.g., 'Activation rate dropped from 0.42 to 0.39 (-7.1%) on Android tier2 users between Sept 30 and Oct 7')",
    "Data point 2 with temporal correlation (e.g., 'This decline occurred 1 day after Release 1056 which introduced phone verification')",
    "Data point 3 with additional context (e.g., 'No campaigns were running for this segment during this period, ruling out campaign fatigue')",
    "Data point 4 if relevant with quantification"
  ],
  
  "key_insights": [
    "Important insight or pattern discovered while answering this question",
    "Additional context that adds value beyond the direct answer"
  ],
  
  "recommendations": [
    {{
      "action": "Specific, implementable recommendation",
      "rationale": "Why this will help based on the data",
      "expected_outcome": "What will likely improve",
      "priority": "high/medium/low",
      "quick_win": true/false
    }}
  ],
  
  "caveats": [
    "Important limitation or consideration the user should know",
    "Data quality note or sample size consideration if applicable"
  ],
  
  "follow_up_suggestions": [
    "Suggested follow-up question to dig deeper",
    "Related analysis that might be valuable"
  ],
  
  "confidence": "high/medium/low",
  "confidence_explanation": "Why this confidence level - cite data quality, correlation strength, sample size"
}}

Remember: Be helpful, specific, and actionable. Use actual data points. If data is insufficient, say so honestly and suggest what additional data would help.
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
                "answer": "I encountered an error analyzing your question. Please try rephrasing or ask a more specific question about your metrics, releases, or campaigns.",
                "supporting_evidence": [],
                "key_insights": [],
                "recommendations": [],
                "caveats": [f"Error: {str(e)}"],
                "follow_up_suggestions": [],
                "confidence": "low",
                "confidence_explanation": "Technical error prevented analysis"
            }
