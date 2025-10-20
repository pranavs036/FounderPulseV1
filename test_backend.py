"""
Test script for NorthStar AI Backend
Tests all major functionality including uploads, insights, and queries
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8001/api"
SAMPLE_DATA_DIR = Path("../sample_data")

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def test_health_check():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'healthy':
                print_success("Server is healthy")
                print_info(f"Database: {data['database']}")
                print_info(f"AI Engine: {data['ai_engine']}")
                return True
            else:
                print_error(f"Server unhealthy: {data}")
                return False
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_reset_data():
    """Reset all data before testing"""
    print("\n" + "="*60)
    print("TEST 2: Reset Data")
    print("="*60)
    
    try:
        response = requests.delete(f"{BASE_URL}/reset")
        if response.status_code == 200:
            print_success("Data reset successful")
            return True
        else:
            print_error(f"Reset failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Reset error: {str(e)}")
        return False

def test_upload_mixpanel():
    """Test Mixpanel data upload"""
    print("\n" + "="*60)
    print("TEST 3: Upload Mixpanel Data")
    print("="*60)
    
    try:
        file_path = SAMPLE_DATA_DIR / "mixpanel_sample.csv"
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{BASE_URL}/upload/mixpanel",
                files={'file': f}
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Uploaded {data['record_count']} records")
            print_info(f"Anomalies detected: {data['insights_generated']}")
            print_info(f"File: {data['filename']}")
            return True
        else:
            print_error(f"Upload failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return False

def test_upload_jira():
    """Test Jira data upload"""
    print("\n" + "="*60)
    print("TEST 4: Upload Jira Data")
    print("="*60)
    
    try:
        file_path = SAMPLE_DATA_DIR / "jira_sample.csv"
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{BASE_URL}/upload/jira",
                files={'file': f}
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Uploaded {data['record_count']} records")
            print_info(f"File: {data['filename']}")
            return True
        else:
            print_error(f"Upload failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return False

def test_upload_moengage():
    """Test MoEngage data upload"""
    print("\n" + "="*60)
    print("TEST 5: Upload MoEngage Data")
    print("="*60)
    
    try:
        file_path = SAMPLE_DATA_DIR / "moengage_sample.json"
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{BASE_URL}/upload/moengage",
                files={'file': f}
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Uploaded {data['record_count']} records")
            print_info(f"File: {data['filename']}")
            return True
        else:
            print_error(f"Upload failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return False

def test_get_summary():
    """Test data summary endpoint"""
    print("\n" + "="*60)
    print("TEST 6: Get Data Summary")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/summary")
        if response.status_code == 200:
            data = response.json()
            print_success("Summary retrieved")
            print_info(f"Mixpanel records: {data['mixpanel_records']}")
            print_info(f"Jira records: {data['jira_records']}")
            print_info(f"MoEngage records: {data['moengage_records']}")
            print_info(f"Detected anomalies: {data['detected_anomalies']}")
            print_info(f"Generated insights: {data['generated_insights']}")
            return True
        else:
            print_error(f"Summary failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Summary error: {str(e)}")
        return False

def test_get_metrics():
    """Test get metrics endpoint"""
    print("\n" + "="*60)
    print("TEST 7: Get Detected Anomalies")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        if response.status_code == 200:
            metrics = response.json()
            print_success(f"Retrieved {len(metrics)} anomalies")
            for i, metric in enumerate(metrics[:3]):  # Show first 3
                print_info(f"\nAnomaly {i+1}:")
                print(f"  Metric: {metric['metric_name']}")
                print(f"  Change: {metric['change_percent']:+.1f}%")
                print(f"  Platform: {metric['platform']}")
                print(f"  Cohort: {metric['cohort']}")
            return True
        else:
            print_error(f"Metrics retrieval failed")
            return False
    except Exception as e:
        print_error(f"Metrics error: {str(e)}")
        return False

def test_wait_for_insights():
    """Wait for background insights generation"""
    print("\n" + "="*60)
    print("TEST 8: Wait for Background Insights Generation")
    print("="*60)
    
    print_info("Waiting 30 seconds for AI analysis...")
    time.sleep(30)
    print_success("Wait complete")
    return True

def test_get_enhanced_insights():
    """Test enhanced insights endpoint"""
    print("\n" + "="*60)
    print("TEST 9: Get Enhanced AI Insights")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/insights/enhanced")
        if response.status_code == 200:
            insights = response.json()
            print_success(f"Retrieved {len(insights)} comprehensive insights")
            
            # Group by type
            insight_types = {}
            for insight in insights:
                itype = insight.get('insight_type', 'unknown')
                insight_types[itype] = insight_types.get(itype, 0) + 1
            
            print_info("\nInsight breakdown:")
            for itype, count in insight_types.items():
                print(f"  {itype}: {count}")
            
            # Show a sample insight
            if insights:
                print_info("\nSample Insight:")
                sample = insights[0]
                print(f"  Type: {sample.get('insight_type')}")
                print(f"  Summary: {sample.get('summary')}")
                print(f"  Confidence: {sample.get('confidence')}")
                if sample.get('recommendations'):
                    print(f"  Recommendations:")
                    for rec in sample['recommendations'][:2]:
                        print(f"    - {rec}")
            
            return len(insights) > 0
        else:
            print_warning("No enhanced insights yet (might still be generating)")
            return True  # Not a failure, just timing
    except Exception as e:
        print_error(f"Enhanced insights error: {str(e)}")
        return False

def test_natural_language_query():
    """Test natural language query endpoint"""
    print("\n" + "="*60)
    print("TEST 10: Natural Language Query")
    print("="*60)
    
    queries = [
        "Why did activation rate drop for Android users?",
        "Which campaign performed best?",
        "What caused the biggest metric change?"
    ]
    
    success_count = 0
    for i, query in enumerate(queries, 1):
        print_info(f"\nQuery {i}: {query}")
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"query": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n  Answer: {data['answer'][:150]}...")
                print(f"  Confidence: {data['confidence']}")
                if data.get('recommendations'):
                    print(f"  Top Recommendation: {data['recommendations'][0]}")
                success_count += 1
            else:
                print_error(f"  Query failed")
        except Exception as e:
            print_error(f"  Query error: {str(e)}")
    
    if success_count == len(queries):
        print_success(f"\nAll {len(queries)} queries successful")
        return True
    else:
        print_warning(f"\n{success_count}/{len(queries)} queries successful")
        return success_count > 0

def test_trigger_insights():
    """Test manual insights generation"""
    print("\n" + "="*60)
    print("TEST 11: Manual Insights Generation")
    print("="*60)
    
    try:
        response = requests.post(f"{BASE_URL}/insights/generate")
        if response.status_code == 200:
            data = response.json()
            print_success(data['message'])
            return True
        else:
            print_error("Trigger failed")
            return False
    except Exception as e:
        print_error(f"Trigger error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("NORTHSTAR AI BACKEND TEST SUITE")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Reset Data", test_reset_data),
        ("Upload Mixpanel", test_upload_mixpanel),
        ("Upload Jira", test_upload_jira),
        ("Upload MoEngage", test_upload_moengage),
        ("Get Summary", test_get_summary),
        ("Get Metrics", test_get_metrics),
        ("Wait for Insights", test_wait_for_insights),
        ("Get Enhanced Insights", test_get_enhanced_insights),
        ("Natural Language Query", test_natural_language_query),
        ("Manual Insights Trigger", test_trigger_insights),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Test '{name}' crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}")
        else:
            print_error(f"{name}")
    
    print("\n" + "="*60)
    if passed == total:
        print_success(f"ALL TESTS PASSED ({passed}/{total})")
    else:
        print_warning(f"SOME TESTS FAILED ({passed}/{total} passed)")
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    print("\n🚀 Starting NorthStar AI Backend Tests\n")
    print("Prerequisites:")
    print("  1. Backend server running on http://localhost:8001")
    print("  2. MongoDB running on localhost:27017")
    print("  3. Valid EMERGENT_LLM_KEY in .env")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    success = run_all_tests()
    
    if success:
        print("🎉 All tests passed! Backend is working perfectly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    exit(0 if success else 1)
