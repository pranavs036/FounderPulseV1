#!/usr/bin/env python3
"""
Interactive Backend Testing Script
Run this to play with all the AI features!
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8001/api"
SAMPLE_DATA_DIR = Path(__file__).parent / "sample_data"

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_success(text):
    print(f"✓ {text}")

def print_info(text):
    print(f"ℹ {text}")

def wait_for_input(prompt="Press Enter to continue..."):
    input(f"\n{prompt}")

# Test 1: Check if server is running
print_header("TEST 1: Health Check")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print_success(f"Server is healthy!")
        print_info(f"Database: {data['database']}")
        print_info(f"AI Engine: {data['ai_engine']}")
    else:
        print("❌ Server is not healthy")
        exit(1)
except Exception as e:
    print(f"❌ Cannot connect to server: {e}")
    print("\nMake sure you started the server:")
    print("  cd backend")
    print("  uvicorn server:app --reload --port 8001")
    exit(1)

wait_for_input()

# Test 2: Reset data to start fresh
print_header("TEST 2: Clear Previous Data")
response = requests.delete(f"{BASE_URL}/reset")
print_success("Database cleared - starting fresh!")
wait_for_input()

# Test 3: Upload Mixpanel data
print_header("TEST 3: Upload Mixpanel Data")
print_info("Uploading sample_data/mixpanel_sample.csv...")

file_path = SAMPLE_DATA_DIR / "mixpanel_sample.csv"
with open(file_path, 'rb') as f:
    response = requests.post(
        f"{BASE_URL}/upload/mixpanel",
        files={'file': ('mixpanel_sample.csv', f, 'text/csv')}
    )

if response.status_code == 200:
    data = response.json()
    print_success(f"Uploaded {data['record_count']} metric records")
    print_info(f"Detected {data['insights_generated']} anomalies (>5% change)")
    print_info("Background AI analysis started automatically!")
else:
    print(f"❌ Upload failed: {response.text}")

wait_for_input()

# Test 4: Upload Jira data
print_header("TEST 4: Upload Jira Data")
print_info("Uploading sample_data/jira_sample.csv...")

file_path = SAMPLE_DATA_DIR / "jira_sample.csv"
with open(file_path, 'rb') as f:
    response = requests.post(
        f"{BASE_URL}/upload/jira",
        files={'file': ('jira_sample.csv', f, 'text/csv')}
    )

if response.status_code == 200:
    data = response.json()
    print_success(f"Uploaded {data['record_count']} release records")
else:
    print(f"❌ Upload failed: {response.text}")

wait_for_input()

# Test 5: Upload MoEngage data
print_header("TEST 5: Upload MoEngage Data")
print_info("Uploading sample_data/moengage_sample.json...")

file_path = SAMPLE_DATA_DIR / "moengage_sample.json"
with open(file_path, 'rb') as f:
    response = requests.post(
        f"{BASE_URL}/upload/moengage",
        files={'file': ('moengage_sample.json', f, 'application/json')}
    )

if response.status_code == 200:
    data = response.json()
    print_success(f"Uploaded {data['record_count']} campaign records")
else:
    print(f"❌ Upload failed: {response.text}")

wait_for_input()

# Test 6: Get Summary
print_header("TEST 6: Data Summary")
response = requests.get(f"{BASE_URL}/summary")
if response.status_code == 200:
    data = response.json()
    print_success("Data Summary:")
    print(f"  📊 Mixpanel records: {data['mixpanel_records']}")
    print(f"  🎯 Jira releases: {data['jira_records']}")
    print(f"  📱 MoEngage campaigns: {data['moengage_records']}")
    print(f"  ⚠️  Detected anomalies: {data['detected_anomalies']}")
    print(f"  💡 Generated insights: {data['generated_insights']}")

wait_for_input()

# Test 7: View Detected Anomalies
print_header("TEST 7: View Detected Anomalies")
response = requests.get(f"{BASE_URL}/metrics")
if response.status_code == 200:
    metrics = response.json()
    print_success(f"Found {len(metrics)} metric anomalies:\n")
    
    for i, metric in enumerate(metrics, 1):
        change = metric['change_percent']
        emoji = "📉" if change < 0 else "📈"
        print(f"{emoji} Anomaly {i}:")
        print(f"   Metric: {metric['metric_name']}")
        print(f"   Change: {change:+.1f}%")
        print(f"   Previous: {metric['previous_value']:.3f}")
        print(f"   Current: {metric['current_value']:.3f}")
        print(f"   Platform: {metric['platform']}")
        print(f"   Segment: {metric['cohort']}")
        print()

wait_for_input()

# Test 8: Wait for AI Analysis
print_header("TEST 8: Wait for AI Analysis to Complete")
print_info("The AI engine is analyzing all your data in the background...")
print_info("This takes about 30 seconds...")

for i in range(30, 0, -5):
    print(f"  Waiting... {i} seconds remaining")
    time.sleep(5)

print_success("Analysis complete!")
wait_for_input()

# Test 9: Get Enhanced AI Insights
print_header("TEST 9: View AI-Generated Insights")
response = requests.get(f"{BASE_URL}/insights/enhanced")

if response.status_code == 200:
    insights = response.json()
    
    if len(insights) == 0:
        print("⚠️  No insights generated yet. Triggering manual generation...")
        requests.post(f"{BASE_URL}/insights/generate")
        print_info("Waiting another 30 seconds...")
        time.sleep(30)
        response = requests.get(f"{BASE_URL}/insights/enhanced")
        insights = response.json()
    
    if len(insights) > 0:
        print_success(f"Generated {len(insights)} comprehensive insights!\n")
        
        # Group by type
        insight_types = {}
        for insight in insights:
            itype = insight.get('insight_type', 'unknown')
            if itype not in insight_types:
                insight_types[itype] = []
            insight_types[itype].append(insight)
        
        print_info("Insight Breakdown:")
        for itype, items in insight_types.items():
            print(f"  • {itype}: {len(items)} insights")
        
        print("\n" + "-"*70)
        
        # Show each insight
        for i, insight in enumerate(insights, 1):
            print(f"\n💡 INSIGHT {i}: {insight.get('insight_type', 'unknown').upper()}")
            print(f"Summary: {insight.get('summary', 'N/A')}")
            print(f"Confidence: {insight.get('confidence', 'N/A')}")
            
            if insight.get('recommendations'):
                print("Recommendations:")
                for rec in insight['recommendations'][:3]:
                    print(f"  → {rec}")
            
            if i < len(insights):
                print("\n" + "-"*70)
    else:
        print("⚠️  No insights generated. Check server logs for errors.")

wait_for_input()

# Test 10: Natural Language Queries
print_header("TEST 10: Natural Language Queries")
print_info("Now let's ask some questions about the data!\n")

queries = [
    "Which platform (Android or iOS) have more users retained?"
    "Why did the activation rate drop for Android users?",
    "Which campaign performed best?",
    "What caused the biggest metric change?",
    "How do tier1 users compare to tier2 users?"
]

for i, query in enumerate(queries, 1):
    print(f"\n❓ QUESTION {i}: {query}")
    print("-" * 70)
    
    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": query},
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n💬 ANSWER:")
        print(f"{data['answer']}\n")
        
        if data.get('supporting_evidence'):
            print("📊 EVIDENCE:")
            for evidence in data['supporting_evidence'][:3]:
                print(f"  • {evidence}")
        
        if data.get('recommendations'):
            print("\n✨ RECOMMENDATIONS:")
            for rec in data['recommendations'][:3]:
                print(f"  → {rec}")
        
        print(f"\nConfidence: {data['confidence']}")
    else:
        print(f"❌ Query failed: {response.text}")
    
    if i < len(queries):
        wait_for_input("Press Enter for next question...")

# Final Summary
print_header("🎉 ALL TESTS COMPLETE!")
print("""
You've successfully tested:
  ✓ File uploads (Mixpanel, Jira, MoEngage)
  ✓ Automatic anomaly detection
  ✓ AI-powered insights generation
  ✓ Natural language queries

What to try next:
  1. Visit http://localhost:8001/docs for interactive API docs
  2. Create your own CSV/JSON files and upload them
  3. Ask more questions via the /api/query endpoint
  4. Integrate with your React frontend

Check the documentation:
  • QUICK_START.md - Quick reference
  • BACKEND_DOCUMENTATION.md - Complete API docs
  • IMPLEMENTATION_SUMMARY.md - What was built
""")

print("\n" + "="*70 + "\n")
